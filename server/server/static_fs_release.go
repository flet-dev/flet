//go:build release

package server

import (
	"embed"
	"io/fs"
	"net/http"
	"strings"
)

const (
	contentRootFolder string = "content/"
)

//go:embed content/*
var f embed.FS

func newStaticFS() StaticFS {
	files := make(map[string]bool)
	fs.WalkDir(f, ".", func(path string, d fs.DirEntry, err error) error {
		if !d.IsDir() {
			files[strings.TrimPrefix(path, contentRootFolder)] = true
		}
		return nil
	})

	// for k := range files {
	// 	log.Debugln("EFS item:", k)
	// }

	return StaticFS{
		files:  files,
		prefix: contentRootFolder,
		httpFS: http.FS(f),
	}
}

func (pfs StaticFS) Exists(prefix string, path string) bool {
	return pfs.findFile(path) != ""
}

func (pfs StaticFS) Open(name string) (http.File, error) {
	//log.Debugln("Static FS Open: ", name)
	return pfs.httpFS.Open(pfs.prefix + pfs.findFile(name))
}
