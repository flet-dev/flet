package commands

import (
	"context"
	"fmt"
	"net"
	"os"
	"os/exec"
	"strconv"
	"sync"

	"github.com/flet-dev/flet/server/cache"
	"github.com/flet-dev/flet/server/config"
	"github.com/flet-dev/flet/server/server"
	"github.com/flet-dev/flet/server/utils"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

func newServerCommand(cancel context.CancelFunc) *cobra.Command {

	var serverPort int
	var background bool
	var attachedProcess bool

	var cmd = &cobra.Command{
		Use:   "server",
		Short: "Start server service",
		Long:  `Server is for ...`,
		Run: func(cmd *cobra.Command, args []string) {

			if serverPort == 0 {
				var err error
				serverPort, err = getFreePort()
				if err != nil {
					log.Fatalf("Error finding a free TCP port: %s.", err)
				}
			}

			if background {
				startServerService(serverPort, attachedProcess)
				return
			}

			if attachedProcess {
				go monitorParentProcess(cancel)
			}

			// init cache
			cache.Init()

			waitGroup := sync.WaitGroup{}
			waitGroup.Add(1)
			go server.Start(cmd.Context(), &waitGroup, serverPort)
			waitGroup.Wait()
		},
	}

	cmd.Flags().IntVarP(&serverPort, "port", "p", config.ServerPort(), "port on which the server will listen")
	cmd.Flags().BoolVarP(&background, "background", "b", false, "run server in background")
	cmd.Flags().BoolVarP(&attachedProcess, "attached", "a", false, "attach background server process to the parent one")

	return cmd
}

func monitorParentProcess(cancel context.CancelFunc) {

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

func startServerService(serverPort int, attached bool) {
	log.Debugln("Starting Flet Server")

	// run server
	execPath, _ := os.Executable()

	var cmd *exec.Cmd
	args := []string{"server", "--port", strconv.Itoa(serverPort)}
	if attached {
		cmd = exec.Command(execPath, args...)
	} else {
		cmd = utils.GetDetachedCmd(execPath, args...)
	}
	cmd.Env = os.Environ()
	cmd.Env = append(cmd.Env, fmt.Sprintf("%s=true", config.LogToFileFlag))

	err := cmd.Start()

	if err != nil {
		log.Fatalln(err)
	}

	log.Debugln("Server process started with PID:", cmd.Process.Pid)
	fmt.Println(serverPort)
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
