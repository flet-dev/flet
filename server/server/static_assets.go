package server

import (
	"net/http"
	"strings"

	log "github.com/sirupsen/logrus"
)

type AssetsFS struct {
	embedAssets *EmbedAssetsSFS
	fsAssets    *FileSystemAssetsSFS
}

func newAssetsFS() AssetsFS {
	embedFs := newEmbedAssetsSFS()
	fileSystemFs := newFileSystemAssetsSFS()
	return AssetsFS{
		embedAssets: embedFs,
		fsAssets:    fileSystemFs,
	}
}

func (fs AssetsFS) Exists(prefix string, path string) bool {
	//log.Debugln("AssetsSFS Exists:", prefix, path)
	if fs.fsAssets != nil && fs.fsAssets.Exists(prefix, path) {
		return true
	}
	return fs.embedAssets.Exists(prefix, path)
}

func (fs AssetsFS) Open(name string) (file http.File, err error) {
	//log.Debugln("AssetsSFS Open:", name, fs.fsAssets)
	if fs.fsAssets != nil {
		file, err = fs.fsAssets.Open(name)
		if err == nil {
			return
		}
		log.Debugln("FileSystemSFS error:", err)
	}
	file, err = fs.embedAssets.Open(name)
	return
}

func findCachedFileName(files map[string]bool, path string) string {
	pathParts := strings.Split(strings.TrimPrefix(path, "/"), "/")
	for i := 0; i < len(pathParts); i++ {
		partialPath := strings.Join(pathParts[i:], "/")
		if _, exists := files[partialPath]; exists {
			return partialPath
		}
	}
	return ""
}
