package server

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/flet-dev/flet/server/config"
	log "github.com/sirupsen/logrus"
)

type FileSystemAssetsSFS struct {
	rootWebDir string
	httpFS     http.FileSystem
}

func newFileSystemAssetsSFS() *FileSystemAssetsSFS {
	rootWebDir := config.StaticRootDir()

	if rootWebDir == "" {
		log.Debugln("Variable FLET_STATIC_ROOT_DIR with path to web static content is not set.")
		return nil
	} else if _, err := os.Stat(rootWebDir); os.IsNotExist(err) {
		log.Warnf("Directory %s with web static content does not exist.", rootWebDir)
		return nil
	}

	log.Debugln("Static assets directory configured:", rootWebDir)

	return &FileSystemAssetsSFS{
		rootWebDir: rootWebDir,
		httpFS:     http.FS(os.DirFS(rootWebDir)),
	}
}

func (fs *FileSystemAssetsSFS) Exists(prefix string, path string) bool {
	//log.Debugln("FileSystemAssetsFS Exists: ", prefix, path)
	return fs.findFullPath(path) != ""
}

func (fs *FileSystemAssetsSFS) Open(name string) (http.File, error) {
	//log.Debugln("FileSystemAssetsFS Open: ", name)
	return fs.httpFS.Open(fs.findFullPath(name))
}

func (fs *FileSystemAssetsSFS) findFullPath(path string) string {
	pathParts := strings.Split(strings.TrimPrefix(path, "/"), "/")
	for i := 0; i < len(pathParts); i++ {
		partialPath := strings.Join(pathParts[i:], "/")
		if _, err := os.Stat(filepath.Join(fs.rootWebDir, partialPath)); err == nil {
			return partialPath
		}
	}
	return ""
}
