package commands

import (
	"os"
	"path/filepath"
	"runtime"

	"github.com/flet-dev/flet/server/config"
	"github.com/rifflock/lfshook"
	log "github.com/sirupsen/logrus"
)

func configLogging() {

	level := log.FatalLevel // default logging level

	envLogLevel := os.Getenv(config.LogLevelFlag)
	if envLogLevel != "" {
		LogLevel = envLogLevel
	}

	level, err := log.ParseLevel(LogLevel)

	if err != nil {
		log.Fatalln(err)
	}

	log.SetLevel(level)

	formatter := &log.TextFormatter{
		FullTimestamp: true,
	}

	if runtime.GOOS == "windows" {
		formatter.ForceColors = true
	}

	log.SetFormatter(formatter)

	if os.Getenv(config.LogToFileFlag) == "true" {
		logPath := "/tmp/pglet.log"
		if runtime.GOOS == "windows" {
			logPath = filepath.Join(os.TempDir(), "pglet.log")
		}
		pathMap := lfshook.PathMap{
			log.DebugLevel: logPath,
			log.InfoLevel:  logPath,
			log.ErrorLevel: logPath,
		}
		log.AddHook(lfshook.NewHook(
			pathMap,
			&log.TextFormatter{}))
	}
}
