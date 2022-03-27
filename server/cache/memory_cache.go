package cache

import (
	"strconv"
	"sync"
	"time"

	"github.com/gomodule/redigo/redis"
	log "github.com/sirupsen/logrus"
	"github.com/wangjia184/sortedset"
)

type cacheEntry struct {
	expires time.Time
	data    interface{}
}

type lockEntry struct {
	m     *memoryCache // point back to M, so we can synchronize removing this mentry when cnt==0
	el    sync.Mutex   // entry-specific lock
	count int          // reference count
	key   interface{}  // key in ma
}

type memoryCache struct {
	sync.RWMutex
	entries       map[string]*cacheEntry
	expireEntries *sortedset.SortedSet
	// pubsub
	// subscriber is a channel
	pubsubLock         sync.RWMutex
	channelSubscribers map[string]map[chan []byte]bool
	subscribers        map[chan []byte]string
	// locks
	ml          sync.Mutex                 // lock for entry map
	lockEntries map[interface{}]*lockEntry // entry map
}

func newMemoryCache() cacher {
	log.Println("Using in-memory cache")
	mc := &memoryCache{
		entries:            make(map[string]*cacheEntry),
		expireEntries:      sortedset.New(),
		channelSubscribers: make(map[string]map[chan []byte]bool),
		subscribers:        make(map[chan []byte]string),
		lockEntries:        make(map[interface{}]*lockEntry),
	}
	go mc.cleanExpiredEntries()
	return mc
}

func (c *memoryCache) cleanExpiredEntries() {
	ticker := time.NewTicker(10 * time.Second)
	for {
		<-ticker.C

		c.Lock()
		entries := c.expireEntries.GetByScoreRange(0, sortedset.SCORE(time.Now().Unix()), &sortedset.GetByScoreRangeOptions{})
		log.Debugln("Expired entries:", len(entries))
		for _, entry := range entries {
			c.deleteEntry(entry.Key())
			c.expireEntries.Remove(entry.Key())
		}
		c.Unlock()
	}
}

func (c *memoryCache) exists(key string) bool {
	c.RLock()
	defer c.RUnlock()

	entry := c.getEntry(key)
	return entry != nil
}

func (c *memoryCache) getString(key string) string {
	c.RLock()
	defer c.RUnlock()

	entry := c.getEntry(key)
	if entry == nil {
		return ""
	}
	return entry.data.(string)
}

func (c *memoryCache) setString(key string, value string, expires time.Duration) {
	c.Lock()
	defer c.Unlock()

	entry := c.newEntry()
	entry.data = value
	c.setExpiration(key, entry, expires)
	c.entries[key] = entry
}

func (c *memoryCache) inc(key string, by int, expires time.Duration) int {
	c.Lock()
	defer c.Unlock()

	i := 0
	entry := c.getEntry(key)
	if entry == nil {
		entry = c.newEntry()
		c.entries[key] = entry
	} else {
		i = entry.data.(int)
	}

	c.setExpiration(key, entry, expires)

	i += by
	entry.data = i
	return i
}

//
// Hashes
// =============================

func (c *memoryCache) hashSet(key string, fields ...interface{}) {
	c.Lock()
	defer c.Unlock()
	c.hashSetInternal(key, fields...)
}

func (c *memoryCache) hashSetInternal(key string, fields ...interface{}) {
	var hash map[string]string
	entry := c.getEntry(key)
	if entry == nil {
		entry = c.newEntry()
		c.entries[key] = entry
		hash = make(map[string]string)
		entry.data = hash
	} else {
		hash = entry.data.(map[string]string)
	}

	var k string
	for i, f := range fields {
		if i%2 == 0 {
			k = f.(string)
		} else if i%2 == 1 {
			hash[k] = toRedisString(f)
		}
	}
}

func (c *memoryCache) hashGet(key string, field string) string {
	c.RLock()
	defer c.RUnlock()
	return c.hashGetInternal(key, field)
}

func (c *memoryCache) hashGetInternal(key string, field string) string {
	entry := c.getEntry(key)
	if entry == nil {
		return ""
	}
	hash := entry.data.(map[string]string)
	return hash[field]
}

func (c *memoryCache) hashGetObject(key string, result interface{}) {
	c.RLock()
	defer c.RUnlock()

	entry := c.getEntry(key)
	if entry == nil {
		return
	}
	hash := entry.data.(map[string]string)
	values := make([]interface{}, len(hash)*2)
	i := 0
	for k, v := range hash {
		values[i] = []byte(k)
		i++
		values[i] = []byte(v)
		i++
	}

	err := redis.ScanStruct(values, result)
	if err != nil {
		log.Fatalln("error scanning struct:", err)
	}
}

func (c *memoryCache) hashGetAll(key string) map[string]string {
	c.RLock()
	defer c.RUnlock()

	entry := c.getEntry(key)
	if entry == nil {
		return make(map[string]string)
	}
	return entry.data.(map[string]string)
}

func (c *memoryCache) hashInc(key string, field string, by int) int {
	c.Lock()
	defer c.Unlock()
	return c.hashIncInternal(key, field, by)
}

func (c *memoryCache) hashIncInternal(key string, field string, by int) int {
	var hash map[string]string
	entry := c.getEntry(key)
	if entry == nil {
		entry = c.newEntry()
		c.entries[key] = entry
		hash = make(map[string]string)
		entry.data = hash
	} else {
		hash = entry.data.(map[string]string)
	}

	i := 0
	if v, err := strconv.Atoi(hash[field]); err == nil {
		i = v
	}
	i += by
	hash[field] = strconv.Itoa(i)
	return i
}

func (c *memoryCache) hashRemove(key string, fields ...string) {
	c.Lock()
	defer c.Unlock()
	c.hashRemoveInternal(key, fields...)
}

func (c *memoryCache) hashRemoveInternal(key string, fields ...string) {
	entry := c.getEntry(key)
	if entry == nil {
		return
	}
	hash := entry.data.(map[string]string)
	for _, f := range fields {
		delete(hash, f)
	}
	if len(hash) == 0 {
		c.deleteEntry(key)
	}
}

//
// Sets
// =============================

func (c *memoryCache) setGet(key string) []string {
	c.RLock()
	defer c.RUnlock()

	entry := c.getEntry(key)
	if entry == nil {
		return make([]string, 0)
	}
	hash := entry.data.(map[string]bool)
	result := make([]string, len(hash))
	i := 0
	for k := range hash {
		result[i] = k
		i++
	}
	return result
}

func (c *memoryCache) setAdd(key string, value string) {
	c.Lock()
	defer c.Unlock()

	var hash map[string]bool
	entry := c.getEntry(key)
	if entry == nil {
		entry = c.newEntry()
		c.entries[key] = entry
		hash = make(map[string]bool)
		entry.data = hash
	} else {
		hash = entry.data.(map[string]bool)
	}

	hash[value] = true
}

func (c *memoryCache) setRemove(key string, value string) int {
	c.Lock()
	defer c.Unlock()

	entry := c.getEntry(key)
	if entry == nil {
		return 0
	}
	hash := entry.data.(map[string]bool)
	result := 0
	if _, exists := hash[value]; exists {
		delete(hash, value)
		result = 1
	}
	if len(hash) == 0 {
		c.deleteEntry(key)
	}
	return result
}

//
// Sorted Sets
// =============================

func (c *memoryCache) sortedSetAdd(key string, value string, score int64) {
	c.Lock()
	defer c.Unlock()

	var set *sortedset.SortedSet
	entry := c.getEntry(key)
	if entry == nil {
		entry = c.newEntry()
		c.entries[key] = entry
		set = sortedset.New()
		entry.data = set
	} else {
		set = entry.data.(*sortedset.SortedSet)
	}

	set.AddOrUpdate(value, sortedset.SCORE(score), nil)
}

func (c *memoryCache) sortedSetPopRange(key string, min int64, max int64) []string {
	c.Lock()
	defer c.Unlock()

	entry := c.getEntry(key)
	if entry == nil {
		return make([]string, 0)
	}
	set := entry.data.(*sortedset.SortedSet)
	nodes := set.GetByScoreRange(sortedset.SCORE(min), sortedset.SCORE(max), &sortedset.GetByScoreRangeOptions{})
	result := make([]string, len(nodes))
	for i, node := range nodes {
		result[i] = node.Key()
		set.Remove(result[i])
	}
	return result
}

func (c *memoryCache) sortedSetRemove(key string, value string) {
	c.Lock()
	defer c.Unlock()

	entry := c.getEntry(key)
	if entry == nil {
		return
	}
	set := entry.data.(*sortedset.SortedSet)
	set.Remove(value)
	if set.GetCount() == 0 {
		c.deleteEntry(key)
	}
}

func (c *memoryCache) remove(keys ...string) {
	c.Lock()
	defer c.Unlock()

	for _, key := range keys {
		c.deleteEntry(key)
	}
}

func (c *memoryCache) newEntry() *cacheEntry {
	entry := &cacheEntry{}
	return entry
}

func (c *memoryCache) getEntry(key string) *cacheEntry {
	entry := c.entries[key]
	if entry == nil {
		return nil
	}
	if !entry.expires.IsZero() && time.Now().After(entry.expires) {
		// remove expired entry
		delete(c.entries, key)
		return nil
	}
	return entry
}

func (c *memoryCache) setExpiration(key string, entry *cacheEntry, expires time.Duration) {
	if expires == 0 {
		return
	}
	entry.expires = time.Now().Add(expires)
	c.expireEntries.AddOrUpdate(key, sortedset.SCORE(entry.expires.Unix()), entry)
}

func (c *memoryCache) deleteEntry(key string) {
	delete(c.entries, key)
}

//
// PubSub
// =============================

func (c *memoryCache) subscribe(channel string) chan []byte {
	c.pubsubLock.Lock()
	defer c.pubsubLock.Unlock()

	subscribers := c.channelSubscribers[channel]
	if subscribers == nil {
		subscribers = make(map[chan []byte]bool)
		c.channelSubscribers[channel] = subscribers
	}

	ch := make(chan []byte)
	subscribers[ch] = true
	c.subscribers[ch] = channel
	return ch
}

func (c *memoryCache) unsubscribe(ch chan []byte) {
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
	}
}

func (c *memoryCache) send(channel string, message []byte) {
	c.pubsubLock.RLock()
	defer c.pubsubLock.RUnlock()

	subscribers := c.channelSubscribers[channel]
	if subscribers == nil {
		return
	}

	for ch := range subscribers {
		ch <- message
	}
}

//
// Locks
// Source: https://stackoverflow.com/questions/40931373/how-to-gc-a-map-of-mutexes-in-go
// =============================
func (c *memoryCache) lock(key string) Unlocker {

	// read or create entry for this key atomically
	c.ml.Lock()
	e, ok := c.lockEntries[key]
	if !ok {
		e = &lockEntry{m: c, key: key}
		c.lockEntries[key] = e
	}
	e.count++ // ref count
	c.ml.Unlock()

	// acquire lock, will block here until e.cnt==1
	e.el.Lock()

	return e
}

// Unlock releases the lock for this entry.
func (me *lockEntry) Unlock() {

	m := me.m

	// decrement and if needed remove entry atomically
	m.ml.Lock()
	e, ok := m.lockEntries[me.key]
	if !ok { // entry must exist
		m.ml.Unlock()
		log.Errorf("Unlock requested for key=%v but no entry found", me.key)
	}
	e.count--        // ref count
	if e.count < 1 { // if it hits zero then we own it and remove from map
		delete(m.lockEntries, me.key)
	}
	m.ml.Unlock()

	// now that map stuff is handled, we unlock and let
	// anything else waiting on this key through
	e.el.Unlock()
}

//
// App specific methods
// =============================

func (c *memoryCache) setSessionControl(sessionKey string, sessionControlsKey string, controlID string, controlJSON string, maxSize int) bool {
	c.Lock()
	defer c.Unlock()

	strSize := c.hashGetInternal(sessionKey, "size")
	if strSize == "" {
		strSize = "0"
	}
	size, _ := strconv.Atoi(strSize)
	currJSON := c.hashGetInternal(sessionControlsKey, controlID)
	size -= len(currJSON)
	size += len(controlJSON)

	if maxSize > 0 && size > maxSize {
		return false
	}

	c.hashSetInternal(sessionControlsKey, controlID, controlJSON)
	c.hashSetInternal(sessionKey, "size", size)

	return true
}

func (c *memoryCache) removeSessionControl(sessionKey string, sessionControlsKey string, controlID string) {
	c.Lock()
	defer c.Unlock()

	currJSON := c.hashGetInternal(sessionControlsKey, controlID)
	c.hashRemoveInternal(sessionControlsKey, controlID)
	c.hashIncInternal(sessionKey, "size", -len(currJSON))
}
