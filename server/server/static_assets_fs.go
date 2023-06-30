package server

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/flet-dev/flet/server/utils"
	log "github.com/sirupsen/logrus"
)

type FileSystemAssetsSFS struct {
	rootWebDir string
	httpFS     http.FileSystem
}

func newFileSystemAssetsSFS(rootWebDir string) *FileSystemAssetsSFS {
	if rootWebDir == "" {
		log.Debugln("Directory with web content is not set.")
		return nil
	} else if _, err := os.Stat(rootWebDir); os.IsNotExist(err) {
		log.Warnf("Directory %s with web content does not exist.", rootWebDir)
		return nil
	}

	//log.Debugln("Static assets directory configured:", rootWebDir)

	return &FileSystemAssetsSFS{
		rootWebDir: rootWebDir,
		httpFS:     http.FS(os.DirFS(rootWebDir)),
	}
}

func (fs *FileSystemAssetsSFS) Exists(path string) bool {
	r := fs.findFullPath(path) != ""
	log.Debugln("FileSystemAssetsFS Exists:", r, fs.rootWebDir, path)
	return r
}

func (fs *FileSystemAssetsSFS) Open(name string) (http.File, error) {
	log.Debugln("FileSystemAssetsFS Open:", fs.rootWebDir, name)
	return fs.httpFS.Open(fs.findFullPath(name))
}

func (fs *FileSystemAssetsSFS) findFullPath(path string) string {
	pathParts := strings.Split(strings.TrimPrefix(path, "/"), "/")
	for i := 0; i < len(pathParts); i++ {
		partialPath := strings.Join(pathParts[i:], "/")
		fullPath := filepath.Clean(filepath.Join(fs.rootWebDir, partialPath))
		if err := utils.InTrustedRoot(fullPath, fs.rootWebDir); err != nil {
			return ""
		}
		if _, err := os.Stat(fullPath); err == nil {
			return partialPath
		}
	}
	return ""
}
