package server

import (
	"net/http"

	log "github.com/sirupsen/logrus"
)

type AssetsFS struct {
	staticContent *FileSystemAssetsSFS
	userAssets    *FileSystemAssetsSFS
}

func newAssetsFS(contentDir string, assetsDir string) AssetsFS {
	return AssetsFS{
		staticContent: newFileSystemAssetsSFS(contentDir),
		userAssets:    newFileSystemAssetsSFS(assetsDir),
	}
}

func (fs AssetsFS) Exists(prefix string, path string) bool {
	//log.Debugln("AssetsSFS Exists:", prefix, path)
	if fs.userAssets != nil && fs.userAssets.Exists(prefix, path) {
		return true
	}
	return fs.staticContent.Exists(prefix, path)
}

func (fs AssetsFS) Open(name string) (file http.File, err error) {
	//log.Debugln("AssetsSFS Open:", name, fs.fsAssets)
	if fs.userAssets != nil {
		file, err = fs.userAssets.Open(name)
		if err == nil {
			return
		}
		log.Debugln("FileSystemSFS error:", err)
	}
	file, err = fs.staticContent.Open(name)
	return
}
