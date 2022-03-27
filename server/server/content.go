//go:build release

package server

import "embed"

const (
	contentRootFolder string = "content/"
)

//go:embed content/*
var f embed.FS
