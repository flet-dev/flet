//go:build !release

package server

import "embed"

const (
	contentRootFolder string = "content_dev/"
)

//go:embed content_dev/*
var f embed.FS
