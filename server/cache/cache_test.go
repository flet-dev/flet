package cache

import (
	"log"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/flet-dev/flet/server/model"
	"github.com/flet-dev/flet/server/utils"
	"github.com/gomodule/redigo/redis"
)

func TestMain(m *testing.M) {

	redisAddr := os.Getenv("FLET_REDIS_ADDR")

	// test in-memory
	os.Setenv("FLET_REDIS_ADDR", "")
	Init()
	retCode := m.Run()
	if retCode != 0 {
		os.Exit(retCode)
	}

	// test Redis
	if redisAddr != "" {
		os.Setenv("FLET_REDIS_ADDR", redisAddr)
		Init()
		retCode = m.Run()
		if retCode != 0 {
			os.Exit(retCode)
		}
	}
}

func TestGetString(t *testing.T) {

	a := GetString("inexistent key")
	if a != "" {
		t.Errorf("getString of inexistent key returned %s, want %s", a, "")
	}

	v := "111"
	SetString("aaa", v, 0)
	r := GetString("aaa")
	if r != v {
		t.Errorf("getString returned %s, want %s", r, v)
	}
}

func TestInc(t *testing.T) {

	Remove("inc1")

	if Exists("inc1") {
		t.Errorf("inc1 should not exist")
	}

	c := Inc("inc1", 1, 30*time.Second)
	if c != 1 {
		t.Errorf("inc returned %d, want %d", c, 1)
	}
	c = Inc("inc1", 2, 0)
	if c != 3 {
		t.Errorf("inc returned %d, want %d", c, 3)
	}
	c = Inc("inc1", -5, 0)
	if c != -2 {
		t.Errorf("inc returned %d, want %d", c, -2)
	}
}

func TestHashInc(t *testing.T) {

	Remove("hinc1")

	if Exists("hinc1") {
		t.Errorf("hinc1 should not exist")
	}

	c := HashInc("hinc1", "items", 1)
	if c != 1 {
		t.Errorf("hinc returned %d, want %d", c, 1)
	}
	c = HashInc("hinc1", "items", 2)
	if c != 3 {
		t.Errorf("hinc returned %d, want %d", c, 3)
	}
	c = HashInc("hinc1", "items", -5)
	if c != -2 {
		t.Errorf("hinc returned %d, want %d", c, -2)
	}
}

func TestRedisScanStruct(t *testing.T) {
	values := []interface{}{
		[]byte("id"), "1",
		[]byte("name"), "obj 1",
	}
	var o1 model.Page
	err := redis.ScanStruct(values, &o1)
	if err != nil {
		log.Fatalln(err)
	}
	log.Println(utils.ToJSON(o1))
}

func TestHashGetObject(t *testing.T) {

	o1 := model.Page{
		ID:    1,
		Name:  "obj 1",
		IsApp: true,
	}

	key := "hobj1"
	Remove(key)

	HashSet(key, "id", o1.ID, "name", o1.Name, "isApp", o1.IsApp)

	var o2 model.Page
	HashGetObject(key, &o2)
	if o2.ID != 1 {
		t.Errorf("ID is %d, want %d", o2.ID, 1)
	}
}

func TestHash(t *testing.T) {

	log.Println("-0-")

	Remove("hash1")

	n0 := HashGet("non-existent hash", "something")
	if n0 != "" {
		t.Errorf("HashGet of non-existent key returned %s, want %s", n0, "")
	}

	log.Println("-1-")

	HashSet("hash1", "aaa", "1", "bbb", "Test")
	aaa := HashGet("hash1", "aaa")
	if aaa != "1" {
		t.Errorf("HashGet returned %s, want %s", aaa, "1")
	}

	log.Println("-2-")

	bbb := HashGet("hash1", "bbb")
	if bbb != "Test" {
		t.Errorf("HashGet returned %s, want %s", bbb, "Test")
	}

	log.Println("-3-")

	n1 := HashGet("hash1", "something")
	if n1 != "" {
		t.Errorf("HashGet non-existent field returned %s, want %s", n1, "")
	}

	HashSet("hash1", "ccc", "Another test")

	log.Println("-4-")

	entries := HashGetAll("hash1")
	count := len(entries)
	if count != 3 {
		t.Errorf("HashGetAll returned %d entries, want %d", count, 3)
	}

	e1 := entries["aaa"]
	if e1 != "1" {
		t.Errorf("Checking all entries field 'aaa' returned %s, want %s", e1, "1")
	}
	e2 := entries["ccc"]
	if e2 != "Another test" {
		t.Errorf("Checking all entries field 'ccc' returned %s, want %s", e2, "Another test")
	}

	HashRemove("hash1", "aaa")
	HashRemove("hash1", "bbb")
	entries = HashGetAll("hash1")
	count = len(entries)
	if count != 1 {
		t.Errorf("HashGetAll after removing 2 elements returned %d entries, want %d", count, 1)
	}
	HashRemove("hash1", "ccc")
	if Exists("hash1") {
		t.Errorf("Hash should not exist after all its elements deleted")
	}
}

func TestSet(t *testing.T) {
	if Exists("set1") {
		t.Errorf("Set should not exist in the first place")
	}

	SetAdd("set1", "v1")
	SetAdd("set1", "v1")
	items := SetGet("set1")
	count := len(items)
	if count != 1 {
		t.Errorf("SetGet returned %d entries, want %d", count, 1)
	}

	SetAdd("set1", "v2")
	items = SetGet("set1")
	count = len(items)
	if count != 2 {
		t.Errorf("SetGet returned %d entries, want %d", count, 2)
	}

	removed := SetRemove("set1", "v2")
	if removed != 1 {
		t.Errorf("SetGet remove result returned %d, want %d", removed, 1)
	}

	// delete again
	removed = SetRemove("set1", "v2")
	if removed != 0 {
		t.Errorf("Second SetGet remove result returned %d, want %d", removed, 0)
	}

	items = SetGet("set1")
	count = len(items)
	if count != 1 {
		t.Errorf("SetGet after removing v2 returned %d entries, want %d", count, 1)
	}

	SetRemove("set1", "v1")
	if Exists("set1") {
		t.Errorf("Set should not exist after removing all elements")
	}
}

func TestLock(t *testing.T) {
	l := Lock("a-1")
	l.Unlock()
}

func TestLocks(t *testing.T) {

	r := rand.New(rand.NewSource(42))

	keyCount := 200
	iCount := 100
	out := make(chan string, iCount*2)

	// run a bunch of concurrent requests for various keys,
	// the idea is to have a lot of lock contention
	var wg sync.WaitGroup
	wg.Add(iCount)
	for i := 0; i < iCount; i++ {
		go func(rn int) {
			defer wg.Done()
			key := strconv.Itoa(rn)

			// you can prove the test works by commenting the locking out and seeing it fail
			l := Lock(key)
			defer l.Unlock()

			out <- key + " A"
			time.Sleep(20 * time.Millisecond) // make 'em wait a mo'
			out <- key + " B"
		}(r.Intn(keyCount))
	}
	wg.Wait()
	close(out)

	// confirm that the output always produced the correct sequence
	outLists := make([][]string, keyCount)
	for s := range out {
		sParts := strings.Fields(s)
		kn, err := strconv.Atoi(sParts[0])
		if err != nil {
			t.Fatal(err)
		}
		outLists[kn] = append(outLists[kn], sParts[1])
	}
	for kn := 0; kn < keyCount; kn++ {
		l := outLists[kn] // list of output for this particular key
		for i := 0; i < len(l); i += 2 {
			if l[i] != "A" || l[i+1] != "B" {
				t.Errorf("For key=%v and i=%v got unexpected values %v and %v", kn, i, l[i], l[i+1])
				break
			}
		}
	}
	if t.Failed() {
		t.Logf("Failed, outLists: %#v", outLists)
	}

}

// func TestChannels(t *testing.T) {
// 	ch1 := make(chan int)
// 	log.Println(ch1)

// 	go func() {
// 		for {
// 			select {
// 			case msg, more := <-ch1:
// 				if !more {
// 					fmt.Println("Channel closed")
// 					return
// 				}
// 				log.Println(msg)
// 			}
// 		}
// 	}()

// 	ch1 <- 1
// 	ch1 <- 2
// 	ch1 <- 3
// 	close(ch1)
// 	time.Sleep(3 * time.Second)
// }
