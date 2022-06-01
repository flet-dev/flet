package server

import (
	"io/fs"
	"net/http"
	"os"
	"strings"

	"github.com/flet-dev/flet/server/config"
	log "github.com/sirupsen/logrus"
)

type FileSystemAssetsSFS struct {
	files  map[string]bool
	prefix string
	httpFS http.FileSystem
}

func newFileSystemAssetsSFS() *FileSystemAssetsSFS {
	files := make(map[string]bool)
	rootWebDir := config.StaticRootDir()

	if rootWebDir == "" {
		log.Debugln("Variable FLET_STATIC_ROOT_DIR with path to web static content is not set.")
		return nil
	} else if _, err := os.Stat(rootWebDir); os.IsNotExist(err) {
		log.Warnf("Directory %s with web static content does not exist.", rootWebDir)
		return nil
	}

	log.Debugln("Static assets directory configured:", rootWebDir)

	dirFs := os.DirFS(rootWebDir)
	fs.WalkDir(dirFs, ".", func(path string, d fs.DirEntry, err error) error {
		if !d.IsDir() {
			files[strings.TrimPrefix(path, rootWebDir)] = true
		}
		return nil
	})

	for k := range files {
		log.Debugln("FileSystemAssetsFS item:", k)
	}

	return &FileSystemAssetsSFS{
		files:  files,
		prefix: rootWebDir,
		httpFS: http.FS(dirFs),
	}
}

func (fs *FileSystemAssetsSFS) Exists(prefix string, path string) bool {
	//log.Debugln("FileSystemAssetsFS Exists: ", prefix, path)
	return findCachedFileName(fs.files, path) != ""
}

func (fs *FileSystemAssetsSFS) Open(name string) (http.File, error) {
	//log.Debugln("FileSystemAssetsFS Open: ", name)
	return fs.httpFS.Open(findCachedFileName(fs.files, name))
}
