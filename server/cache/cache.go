package cache

import (
	"fmt"
	"strconv"
	"time"

	"github.com/flet-dev/flet/server/config"
)

type cacher interface {
	exists(key string) bool
	getString(key string) string
	setString(key string, value string, expires time.Duration)
	inc(key string, by int, expires time.Duration) int
	remove(keys ...string)
	// hashes
	hashSet(key string, fields ...interface{})
	hashGet(key string, field string) string
	hashGetObject(key string, result interface{})
	hashGetAll(key string) map[string]string
	hashInc(key string, field string, by int) int
	hashRemove(key string, fields ...string)
	// sets
	setGet(key string) []string
	setAdd(key string, value string)
	setRemove(key string, value string) int
	// sorted sets
	sortedSetAdd(key string, value string, score int64)
	sortedSetPopRange(key string, min int64, max int64) []string
	sortedSetRemove(key string, value string)
	// pubsub
	subscribe(channel string) chan []byte
	unsubscribe(ch chan []byte)
	send(channel string, message []byte)
	// locks
	lock(key string) Unlocker
	// app specific
	setSessionControl(sessionKey string, sessionControlsKey string, controlID string, controlJSON string, maxSize int) bool
	removeSessionControl(sessionKey string, sessionControlsKey string, controlID string)
}

type Unlocker interface {
	Unlock()
}

var cache cacher

func Init() {
	if config.RedisAddr() != "" {
		cache = newRedisCache()
	} else {
		cache = newMemoryCache()
	}
}

func Exists(key string) bool {
	return cache.exists(key)
}

func GetString(key string) string {
	return cache.getString(key)
}

func SetString(key string, value string, expires time.Duration) {
	cache.setString(key, value, expires)
}

func Inc(key string, by int, expires time.Duration) int {
	return cache.inc(key, by, expires)
}

//
// Hashes
// =============================

func HashSet(key string, fields ...interface{}) {
	cache.hashSet(key, fields...)
}

func HashGet(key string, field string) string {
	return cache.hashGet(key, field)
}

func HashGetObject(key string, result interface{}) {
	cache.hashGetObject(key, result)
}

func HashGetAll(key string) map[string]string {
	return cache.hashGetAll(key)
}

func HashInc(key string, field string, by int) int {
	return cache.hashInc(key, field, by)
}

func HashRemove(key string, fields ...string) {
	cache.hashRemove(key, fields...)
}

//
// Sets
// =============================

func SetGet(key string) []string {
	return cache.setGet(key)
}

func SetAdd(key string, value string) {
	cache.setAdd(key, value)
}

func SetRemove(key string, value string) int {
	return cache.setRemove(key, value)
}

func Remove(keys ...string) {
	cache.remove(keys...)
}

//
// Sorted sets
// =============================

func SortedSetAdd(key string, value string, score int64) {
	cache.sortedSetAdd(key, value, score)
}

func SortedSetPopRange(key string, min int64, max int64) []string {
	return cache.sortedSetPopRange(key, min, max)
}

func SortedSetRemove(key string, value string) {
	cache.sortedSetRemove(key, value)
}

//
// PubSub
// =============================

func Subscribe(channel string) chan []byte {
	return cache.subscribe(channel)
}

func Unsubscribe(ch chan []byte) {
	cache.unsubscribe(ch)
}

func Send(channel string, message []byte) {
	cache.send(channel, message)
}

//
// Locks
// =============================
func Lock(key string) Unlocker {
	return cache.lock(key)
}

//
// App specific methods
// =============================
func SetSessionControl(sessionKey string, sessionControlsKey string, controlID string, controlJSON string, maxSize int) bool {
	return cache.setSessionControl(sessionKey, sessionControlsKey, controlID, controlJSON, maxSize)
}

func RemoveSessionControl(sessionKey string, sessionControlsKey string, controlID string) {
	cache.removeSessionControl(sessionKey, sessionControlsKey, controlID)
}

//
// Helper methods
// =============================
func toRedisString(value interface{}) string {
	switch value := value.(type) {
	case string:
		return value
	case int:
		return strconv.Itoa(value)
	case int64:
		return strconv.FormatInt(value, 10)
	case float64:
		return strconv.FormatFloat(value, 'E', -1, 32)
	case bool:
		if value {
			return "1"
		}
		return "0"
	case nil:
		return ""
	default:
		return fmt.Sprintf("%v", value)
	}
}
