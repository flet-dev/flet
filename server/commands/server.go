package commands

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sync"

	"github.com/alexflint/go-filemutex"
	"github.com/flet-dev/flet/server/cache"
	"github.com/flet-dev/flet/server/config"
	"github.com/flet-dev/flet/server/server"
	"github.com/flet-dev/flet/server/utils"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

func newServerCommand() *cobra.Command {

	var serverPort int
	var background bool
	var attachedProcess bool

	var cmd = &cobra.Command{
		Use:   "server",
		Short: "Start server service",
		Long:  `Server is for ...`,
		Run: func(cmd *cobra.Command, args []string) {

			if background {
				startServerService(attachedProcess)
				return
			}

			// ensure one executable instance is running
			m, err := filemutex.New(getLockFilename(serverPort))
			if err != nil {
				log.Fatalln("Cannot create mutex - directory did not exist or file could not be created")
			}

			err = m.TryLock()
			if err != nil {
				log.Fatalf("Another instance of Flet Server is already listening on port %d", serverPort)
			}

			defer m.Unlock()

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

func startServerService(attached bool) {
	log.Traceln("Starting Flet Server")

	// run server
	execPath, _ := os.Executable()

	var cmd *exec.Cmd
	if attached {
		cmd = exec.Command(execPath, "server")
	} else {
		cmd = utils.GetDetachedCmd(execPath, "server")
	}
	cmd.Env = os.Environ()
	cmd.Env = append(cmd.Env, fmt.Sprintf("%s=true", config.LogToFileFlag))

	err := cmd.Start()

	if err != nil {
		log.Fatalln(err)
	}

	log.Traceln("Server process started with PID:", cmd.Process.Pid)
}

func getLockFilename(serverPort int) string {
	return filepath.Join(os.TempDir(), fmt.Sprintf("flet-%d.lock", serverPort))
}
