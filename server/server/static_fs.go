package server

import (
	"net/http"
	"strings"
)

type StaticFS struct {
	files  map[string]bool
	prefix string
	httpFS http.FileSystem
}

func (pfs StaticFS) findFile(path string) string {
	pathParts := strings.Split(strings.TrimPrefix(path, "/"), "/")
	for i := 0; i < len(pathParts); i++ {
		partialPath := strings.Join(pathParts[i:], "/")
		if _, exists := pfs.files[partialPath]; exists {
			return partialPath
		}
	}
	return ""
}
