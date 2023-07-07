package stats

import (
	"sync"
	"time"
)

var (
	mu               sync.Mutex
	connectedClients int
	lastDisconnected time.Time
)

func ClientConnected() {
	mu.Lock()
	defer mu.Unlock()
	connectedClients++
}

func ClientDisconnected() {
	mu.Lock()
	defer mu.Unlock()
	connectedClients--
	lastDisconnected = time.Now()
}

func LastClientDisconnected(seconds int) bool {
	mu.Lock()
	defer mu.Unlock()
	return connectedClients == 0 && !lastDisconnected.IsZero() && int(time.Now().Sub(lastDisconnected).Seconds()) >= seconds
}
