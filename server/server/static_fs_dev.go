//go:build !release

package server

import (
	"io/fs"
	"net/http"
	"os"
	"strings"

	"github.com/flet-dev/flet/server/config"
	log "github.com/sirupsen/logrus"
)

func newStaticFS() StaticFS {
	files := make(map[string]bool)
	rootWebDir := config.StaticRootDir()

	if rootWebDir == "" {
		log.Panicf("Variable FLET_STATIC_ROOT_DIR with path to web static content is not set.")
	} else if _, err := os.Stat(rootWebDir); os.IsNotExist(err) {
		log.Panicf("Directory %s with web static content does not exist.", rootWebDir)
	}

	dirFs := os.DirFS(rootWebDir)
	fs.WalkDir(dirFs, ".", func(path string, d fs.DirEntry, err error) error {
		if !d.IsDir() {
			files[strings.TrimPrefix(path, rootWebDir)] = true
		}
		return nil
	})

	for k := range files {
		log.Debugln("EFS item:", k)
	}

	return StaticFS{
		files:  files,
		prefix: rootWebDir,
		httpFS: http.FS(dirFs),
	}
}

func (pfs StaticFS) Exists(prefix string, path string) bool {
	return pfs.findFile(path) != ""
}

func (pfs StaticFS) Open(name string) (http.File, error) {
	log.Debugln("Static FS Open: ", name)
	return pfs.httpFS.Open(pfs.findFile(name))
}
