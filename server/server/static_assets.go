package server

import (
	"net/http"
	"strings"

	"github.com/flet-dev/flet/server/model"
	"github.com/flet-dev/flet/server/store"
	log "github.com/sirupsen/logrus"
)

type AssetsFS struct {
	staticContent *FileSystemAssetsSFS
}

func newAssetsFS(contentDir string) AssetsFS {
	return AssetsFS{
		staticContent: newFileSystemAssetsSFS(contentDir, true),
	}
}

func (fs AssetsFS) Exists(prefix string, path string) bool {
	//log.Debugln("AssetsSFS Exists:", prefix, path)
	assetsFS, assetPath, _ := fs.getAssetsSFS(path)
	if assetsFS != nil && assetsFS.Exists(assetPath) {
		return true
	}
	return fs.staticContent.Exists(path)
}

func (fs AssetsFS) Open(name string) (file http.File, err error) {
	//log.Debugln("AssetsSFS Open:", name)
	assetsFS, assetPath, _ := fs.getAssetsSFS(name)
	if assetsFS != nil && assetsFS.Exists(assetPath) {
		file, err = assetsFS.Open(name)
		if err == nil {
			return
		}
	}
	file, err = fs.staticContent.Open(name)
	return
}

func (fs AssetsFS) getAssetsSFS(path string) (afs *FileSystemAssetsSFS, assetPath string, err error) {
	afs = nil
	p := strings.Trim(path, "/")
	assetPath = path

	if p != "" {
		hrefParts := strings.Split(p, "/")
		if len(hrefParts) > 2 {
			p = strings.Join(hrefParts[:2], "/")
			assetPath = strings.Join(hrefParts[2:], "/")
		} else {
			p = ""
		}
	}

	log.Debugln("getAssetsSFS, path, assetPath:", path, assetPath)

	pageName, err := model.ParsePageName(p)
	if err != nil {
		return
	}

	page := store.GetPageByName(pageName.String())

	if page != nil && page.AssetsDir == "" {
		return
	} else if page == nil && p != "" {
		// fallback to index
		p = ""
		assetPath = path

		pageName, err = model.ParsePageName(p)
		if err != nil {
			return
		}

		page = store.GetPageByName(pageName.String())
		if page == nil || page.AssetsDir == "" {
			return
		}
	} else if page == nil {
		return
	}

	afs = newFileSystemAssetsSFS(page.AssetsDir, false)
	return
}
