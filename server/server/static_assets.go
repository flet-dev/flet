package server

import (
	"net/http"

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
