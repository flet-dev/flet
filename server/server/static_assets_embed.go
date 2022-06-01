package server

import (
	"embed"
	"io/fs"
	"net/http"
	"strings"

	log "github.com/sirupsen/logrus"
)

const (
	contentRootFolder string = "content/"
)

//go:embed content/*
var f embed.FS

type EmbedAssetsSFS struct {
	files  map[string]bool
	prefix string
	httpFS http.FileSystem
}

func newEmbedAssetsSFS() *EmbedAssetsSFS {
	files := make(map[string]bool)
	fs.WalkDir(f, ".", func(path string, d fs.DirEntry, err error) error {
		if !d.IsDir() {
			files[strings.TrimPrefix(path, contentRootFolder)] = true
		}
		return nil
	})

	for k := range files {
		log.Debugln("EmbedAssetsFS item:", k)
	}

	return &EmbedAssetsSFS{
		files:  files,
		prefix: contentRootFolder,
		httpFS: http.FS(f),
	}
}

func (fs *EmbedAssetsSFS) Exists(prefix string, path string) bool {
	//log.Debugln("EmbedAssetsSFS Exists: ", prefix, path)
	return findCachedFileName(fs.files, path) != ""
}

func (fs *EmbedAssetsSFS) Open(name string) (http.File, error) {
	//log.Debugln("EmbedAssetsFS Open: ", name)
	return fs.httpFS.Open(fs.prefix + findCachedFileName(fs.files, name))
}
