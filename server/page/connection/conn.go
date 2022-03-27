package connection

type ReadMessageHandler func(message []byte) error

type Conn interface {
	Start(handler ReadMessageHandler) bool
	Send(message []byte)
}
