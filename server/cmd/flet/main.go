package main

import (
	"context"
	"os"
	"os/signal"

	"github.com/flet-dev/flet/server/commands"
)

func main() {

	interruptCh := make(chan os.Signal, 1)
	signal.Notify(interruptCh, os.Interrupt, os.Kill)

	ctx, cancel := context.WithCancel(context.Background())

	go func() {
		select {
		case <-ctx.Done():
			return
		case <-interruptCh:
			cancel()
		}
	}()

	if err := commands.NewRootCmd().ExecuteContext(ctx); err != nil {
		os.Exit(1)
	}
}
