package cache

import (
	"errors"
	"sync"
	"time"

	"github.com/flet-dev/flet/server/config"
	"github.com/gomodule/redigo/redis"
	"github.com/google/uuid"
	log "github.com/sirupsen/logrus"
)

var errLockMismatch = errors.New("key is locked with a different secret")

const lockScript = `
local v = redis.call("GET", KEYS[1])
if v == false or v == ARGV[1]
then
	return redis.call("SET", KEYS[1], ARGV[1], "EX", ARGV[2]) and 1
else
	return 0
end
`

const unlockScript = `
local v = redis.call("GET",KEYS[1])
if v == false then
	return 1
elseif v == ARGV[1] then
	return redis.call("DEL",KEYS[1])
else
	return 0
end
`

const setControlScript = `
-- current size
local size = redis.call("HGET", KEYS[1], "size")
if not size then
    size = 0
end

-- curent element
local curr_json=redis.call("HGET", KEYS[2], ARGV[2])
if curr_json then
    size = size - string.len(curr_json)
end

-- new size
size = size + string.len(ARGV[3])
local maxSize = tonumber(ARGV[1])
if maxSize > 0 and size > maxSize then
    return 0
end

redis.call("HSET", KEYS[2], ARGV[2], ARGV[3])
redis.call("HSET", KEYS[1], "size", size)
return 1
`

const removeControlScript = `
local curr_json=redis.call("HGET", KEYS[2], ARGV[1])
if curr_json then
	redis.call("HDEL", KEYS[2], ARGV[1])
	redis.call("HINCRBY", KEYS[1], "size", -string.len(curr_json))
end
`

type redisCache struct {
	pool *redis.Pool
	// pubsub
	// subscriber is a channel
	psc                *redis.PubSubConn
	pubsubLock         sync.RWMutex
	channelSubscribers map[string]map[chan []byte]bool
	subscribers        map[chan []byte]string
}

func newRedisCache() cacher {

	redisAddr := config.RedisAddr()
	redisPassword := config.RedisPassword()

	log.Println("Connecting to Redis server", redisAddr)

	pool := &redis.Pool{
		MaxIdle:   config.RedisMaxIdle(),
		MaxActive: config.RedisMaxActive(),

		Dial: func() (redis.Conn, error) {
			conn, err := redis.Dial("tcp", redisAddr)
			if err != nil {
				return nil, err
			}

			if redisPassword != "" {
				if _, err := conn.Do("AUTH", redisPassword); err != nil {
					conn.Close()
					return nil, err
				}
			}
			return conn, nil
		},

		TestOnBorrow: func(c redis.Conn, t time.Time) error {
			if time.Since(t) < time.Minute {
				return nil
			}
			_, err := c.Do("PING")
			return err
		},
	}

	rc := &redisCache{
		pool:               pool,
		channelSubscribers: make(map[string]map[chan []byte]bool),
		subscribers:        make(map[chan []byte]string),
	}

	go rc.listenSubscriptions()

	return rc
}

func (c *redisCache) listenSubscriptions() {
	// start pubsub connection
	c.psc = &redis.PubSubConn{Conn: c.pool.Get()}

	for {
		switch v := c.psc.Receive().(type) {
		case redis.Message:
			c.pubsubLock.RLock()

			subscribers := c.channelSubscribers[v.Channel]
			if subscribers == nil {
				return
			}

			for ch := range subscribers {
				select {
				case ch <- v.Data:
					// Message sent to subscriber
				default:
					// No listeners
				}
			}

			c.pubsubLock.RUnlock()

		case redis.Subscription:
			log.Printf("%s: %s %d\n", v.Channel, v.Kind, v.Count)
		case error:
			log.Fatalln(v)
		}
	}
}

func (c *redisCache) exists(key string) bool {
	conn := c.pool.Get()
	defer conn.Close()

	exists, err := redis.Bool(conn.Do("EXISTS", key))
	if err != nil {
		log.Fatal(err)
	}
	return exists
}

func (c *redisCache) getString(key string) string {
	conn := c.pool.Get()
	defer conn.Close()

	value, err := redis.String(conn.Do("GET", key))
	if err == redis.ErrNil {
		return ""
	} else if err != nil {
		log.Fatal(err)
	}
	return value
}

func (c *redisCache) setString(key string, value string, expires time.Duration) {
	conn := c.pool.Get()
	defer conn.Close()

	args := []interface{}{key, value}
	if expires > 0 {
		args = append(args, "EX", expires.Seconds())
	}
	_, err := conn.Do("SET", args...)
	if err != nil {
		log.Fatal(err)
	}
}

func (c *redisCache) inc(key string, by int, expires time.Duration) int {
	conn := c.pool.Get()
	defer conn.Close()

	conn.Send("MULTI")
	conn.Send("INCRBY", key, by)
	if expires > 0 {
		conn.Send("EXPIRE", key, expires.Seconds())
	}
	value, err := redis.Values(conn.Do("EXEC"))
	if err != nil {
		log.Fatal(err)
	}
	return int(value[0].(int64))
}

func (c *redisCache) remove(keys ...string) {
	conn := c.pool.Get()
	defer conn.Close()

	args := make([]interface{}, len(keys))
	for i, f := range keys {
		args[i] = f
	}

	_, err := conn.Do("DEL", args...)
	if err != nil {
		log.Fatal(err)
	}
}

//
// Hashes
// =============================

func (c *redisCache) hashSet(key string, fields ...interface{}) {
	conn := c.pool.Get()
	defer conn.Close()

	args := make([]interface{}, len(fields)+1)
	args[0] = key
	for i, f := range fields {
		args[i+1] = f
	}

	_, err := conn.Do("HSET", args...)
	if err != nil {
		log.Fatal(err)
	}
}

func (c *redisCache) hashGet(key string, field string) string {
	conn := c.pool.Get()
	defer conn.Close()

	value, err := conn.Do("HGET", key, field)
	if err == redis.ErrNil {
		return ""
	} else if err != nil {
		log.Fatal(err)
	}

	if value == nil {
		return ""
	}

	return string(value.([]byte))
}

func (c *redisCache) hashGetObject(key string, result interface{}) {
	conn := c.pool.Get()
	defer conn.Close()

	values, err := redis.Values(conn.Do("HGETALL", key))
	if err == redis.ErrNil {
		return
	} else if err != nil {
		log.Fatal(err)
	}

	err = redis.ScanStruct(values, result)
	if err != nil {
		log.Fatalln("error scanning struct:", err)
	}
}

func (c *redisCache) hashGetAll(key string) map[string]string {
	conn := c.pool.Get()
	defer conn.Close()

	value, err := redis.StringMap(conn.Do("HGETALL", key))
	if err == redis.ErrNil {
		return make(map[string]string)
	} else if err != nil {
		log.Fatal(err)
	}
	return value
}

func (c *redisCache) hashInc(key string, field string, by int) int {
	conn := c.pool.Get()
	defer conn.Close()

	value, err := redis.Int(conn.Do("HINCRBY", key, field, by))
	if err != nil {
		log.Fatal(err)
	}
	return value
}

func (c *redisCache) hashRemove(key string, fields ...string) {
	conn := c.pool.Get()
	defer conn.Close()

	args := make([]interface{}, len(fields)+1)
	args[0] = key
	for i, f := range fields {
		args[i+1] = f
	}

	_, err := conn.Do("HDEL", args...)
	if err != nil {
		log.Fatal(err)
	}
}

//
// Sets
// =============================

func (c *redisCache) setGet(key string) []string {
	conn := c.pool.Get()
	defer conn.Close()

	value, err := redis.Strings(conn.Do("SMEMBERS", key))
	if err == redis.ErrNil {
		return make([]string, 0)
	} else if err != nil {
		log.Fatal(err)
	}
	return value
}

func (c *redisCache) setAdd(key string, value string) {
	conn := c.pool.Get()
	defer conn.Close()

	_, err := conn.Do("SADD", key, value)
	if err != nil {
		log.Fatal(err)
	}
}

func (c *redisCache) setRemove(key string, value string) int {
	conn := c.pool.Get()
	defer conn.Close()

	result, err := redis.Int(conn.Do("SREM", key, value))
	if err != nil {
		log.Fatal(err)
	}
	return result
}

//
// Sorted Sets
// =============================

func (c *redisCache) sortedSetAdd(key string, value string, score int64) {
	conn := c.pool.Get()
	defer conn.Close()

	_, err := conn.Do("ZADD", key, score, value)
	if err != nil {
		log.Fatal(err)
	}
}

func (c *redisCache) sortedSetPopRange(key string, min int64, max int64) []string {
	conn := c.pool.Get()
	defer conn.Close()

	conn.Send("MULTI")
	conn.Send("ZRANGEBYSCORE", key, min, max)
	conn.Send("ZREMRANGEBYSCORE", key, min, max)
	value, err := conn.Do("EXEC")
	if err != nil {
		log.Fatal(err)
	}

	result, _ := redis.Strings(value.([]interface{})[0], nil)
	return result
}

func (c *redisCache) sortedSetRemove(key string, value string) {
	conn := c.pool.Get()
	defer conn.Close()

	_, err := conn.Do("ZREM", key, value)
	if err != nil {
		log.Fatal(err)
	}
}

//
// PubSub
// =============================

func (c *redisCache) subscribe(channel string) chan []byte {
	c.pubsubLock.Lock()
	defer c.pubsubLock.Unlock()

	subscribers := c.channelSubscribers[channel]
	if subscribers == nil {

		// subscribe in Redis
		err := c.psc.Subscribe(channel)
		if err != nil {
			log.Fatalln(err)
		}

		subscribers = make(map[chan []byte]bool)
		c.channelSubscribers[channel] = subscribers
	}

	ch := make(chan []byte)
	subscribers[ch] = true
	c.subscribers[ch] = channel

	return ch
}

func (c *redisCache) unsubscribe(ch chan []byte) {
	c.pubsubLock.Lock()
	defer c.pubsubLock.Unlock()

	channel := c.subscribers[ch]
	if channel == "" {
		return
	}

	subscribers := c.channelSubscribers[channel]
	if subscribers == nil {
		return
	}

	close(ch)
	delete(subscribers, ch)

	if len(subscribers) == 0 {
		delete(c.channelSubscribers, channel)

		// unsubscribe in Redis
		err := c.psc.Unsubscribe(channel)
		if err != nil {
			log.Fatalln(err)
		}
	}
}

func (c *redisCache) send(channel string, message []byte) {

	conn := c.pool.Get()
	defer conn.Close()

	_, err := conn.Do("PUBLISH", channel, message)
	if err != nil {
		log.Fatal(err)
	}
}

//
// Locks
// Source: https://gist.github.com/bgentry/6105288
// =============================
func (c *redisCache) lock(key string) Unlocker {
	attempts := 100
	lockTimeout := 10 * time.Second
	retryTimeout := 100 * time.Millisecond
	secret := uuid.New().String()

	for i := 0; i < attempts; i++ {
		conn := c.pool.Get()
		if c.writeLock(conn, key, secret, int64(lockTimeout)) {
			return &redisLock{
				conn:   conn,
				name:   key,
				secret: secret,
			}
		}
		time.Sleep(retryTimeout)
	}
	log.Fatalf("Cannot aquire lock %s in 10 seconds", key)
	return nil
}

// writeLock attempts to grab a redis lock. The error returned is safe to ignore
// if all you care about is whether or not the lock was acquired successfully.
func (c *redisCache) writeLock(conn redis.Conn, name, secret string, ttl int64) bool {

	script := redis.NewScript(1, lockScript)
	resp, err := redis.Int(script.Do(conn, name, secret, ttl))
	if err != nil || resp == 0 {
		conn.Close()
		return false
	}
	return true
}

type redisLock struct {
	conn   redis.Conn
	name   string
	secret string
}

func (rl *redisLock) Unlock() {
	defer rl.conn.Close()

	script := redis.NewScript(1, unlockScript)
	resp, err := redis.Int(script.Do(rl.conn, rl.name, rl.secret))
	if err != nil {
		log.Fatal(err)
	}
	if resp == 0 {
		log.Fatal(errLockMismatch)
	}
}

//
// App specific methods
// =============================

func (c *redisCache) setSessionControl(sessionKey string, sessionControlsKey string, controlID string, controlJSON string, maxSize int) bool {
	conn := c.pool.Get()
	defer conn.Close()

	script := redis.NewScript(2, setControlScript)
	result, err := redis.Bool(script.Do(conn, sessionKey, sessionControlsKey, maxSize, controlID, controlJSON))
	if err != nil {
		log.Fatal(err)
	}
	return result
}

func (c *redisCache) removeSessionControl(sessionKey string, sessionControlsKey string, controlID string) {
	conn := c.pool.Get()
	defer conn.Close()

	script := redis.NewScript(2, removeControlScript)
	_, err := script.Do(conn, sessionKey, sessionControlsKey, controlID)
	if err != nil {
		log.Fatal(err)
	}
}
