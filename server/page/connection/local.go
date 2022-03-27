package connection

import log "github.com/sirupsen/logrus"

type Local struct {
	readCh  chan []byte
	writeCh chan []byte
	done    chan bool
}

func NewLocal(readCh chan []byte, writeCh chan []byte) *Local {
	cws := &Local{
		readCh:  readCh,
		writeCh: writeCh,
		done:    make(chan bool),
	}
	return cws
}

func (c *Local) Start(handler ReadMessageHandler) bool {
	// start read loop
	go c.readLoop(handler)
	return <-c.done
}

func (c *Local) readLoop(readHandler ReadMessageHandler) {
	for {
		message := <-c.readCh
		err := readHandler(message)
		if err != nil {
			log.Errorf("error processing message: %v", err)
			break
		}
	}
}

func (c *Local) Send(message []byte) {
	c.writeCh <- message
}
