package commands

import (
	"context"
	"net"
	"os"
	"runtime"
	"sync"
	"time"

	"github.com/flet-dev/flet/server/cache"
	"github.com/flet-dev/flet/server/config"
	"github.com/flet-dev/flet/server/server"
	"github.com/flet-dev/flet/server/stats"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

const (
	DefaultShutdownTimeoutSeconds = 60
)

var (
	version                = "unknown"
	LogLevel               string
	shutdownTimeoutSeconds int
)

func NewServerCommand(cancel context.CancelFunc) *cobra.Command {

	var serverPort int
	var contentDir string
	var assetsDir string
	var attachedProcess bool

	var cmd = &cobra.Command{
		Use:     "fletd",
		Short:   "Flet Server",
		Version: version,
		PersistentPreRun: func(cmd *cobra.Command, args []string) {
			configureLogging()
		},
		Run: func(cmd *cobra.Command, args []string) {

			if serverPort == 0 {
				var err error
				serverPort, err = getFreePort()
				if err != nil {
					log.Fatalf("Error finding a free TCP port: %s.", err)
				}
			}

			if attachedProcess {
				go monitorParentProcess(cancel)
			} else if shutdownTimeoutSeconds > 0 {
				go monitorConnectedClients(cancel)
			}

			// init cache
			cache.Init()

			waitGroup := sync.WaitGroup{}
			waitGroup.Add(1)
			go server.Start(cmd.Context(), &waitGroup, serverPort, contentDir, assetsDir)
			waitGroup.Wait()
		},
	}

	cmd.SetVersionTemplate("{{.Version}}")

	cmd.PersistentFlags().StringVarP(&LogLevel, "log-level", "l", "info", "verbosity level for logs")

	cmd.Flags().IntVarP(&serverPort, "port", "p", config.ServerPort(), "port on which the server will listen")
	cmd.Flags().IntVarP(&shutdownTimeoutSeconds, "shutdown", "", DefaultShutdownTimeoutSeconds, "shutdown server in N seconds after the last client disconnected")
	cmd.Flags().StringVarP(&contentDir, "content-dir", "", "", "path to web content directory")
	cmd.MarkFlagRequired("content-dir")
	cmd.Flags().StringVarP(&assetsDir, "assets-dir", "", "", "path to user assets directory")
	cmd.Flags().BoolVarP(&attachedProcess, "attached", "a", false, "attach background server process to the parent one")

	return cmd
}

func monitorConnectedClients(cancel context.CancelFunc) {
	defer cancel()
	for {
		if stats.LastClientDisconnected(shutdownTimeoutSeconds) {
			log.Debugln("No more clients connected. Shutting down server...")
			return
		}
		time.Sleep(1 * time.Second)
	}
}

func monitorParentProcess(cancel context.CancelFunc) {
	if runtime.GOOS == "windows" {
		monitorParentProcessWindows(cancel)
	} else {
		monitorParentProcessUnix(cancel)
	}
}

func monitorParentProcessUnix(cancel context.CancelFunc) {
	defer cancel()
	ppid := os.Getppid()
	for {
		//log.Debugln("Parent process ID", ppid, os.Getppid())
		if ppid != os.Getppid() {
			log.Debugln("Parent process has been closed. Exiting...")
			return
		}
		time.Sleep(1 * time.Second)
	}
}

func monitorParentProcessWindows(cancel context.CancelFunc) {

	ppid := os.Getppid()
	pp, err := os.FindProcess(ppid)
	if err != nil {
		log.Fatalf("Cannot find parent process with PID %d: %s", ppid, err)
	}

	ps, err := pp.Wait()
	if err != nil {
		log.Fatalf("Error waiting parent process to exit: %s", err)
	}

	log.Println("Parent process exited with code", ps.ExitCode())

	cancel()
}

func getFreePort() (int, error) {
	addr, err := net.ResolveTCPAddr("tcp", "localhost:0")
	if err != nil {
		return 0, err
	}

	l, err := net.ListenTCP("tcp", addr)
	if err != nil {
		return 0, err
	}
	defer l.Close()
	return l.Addr().(*net.TCPAddr).Port, nil
}
