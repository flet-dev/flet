package utils

import (
	"errors"
	"os"
	"path/filepath"
)

func InTrustedRoot(path string, trustedRoot string) error {
	root := filepath.VolumeName(trustedRoot) + string(os.PathSeparator)
	for path != root {
		path = filepath.Dir(path)
		if path == trustedRoot {
			return nil
		}
	}
	return errors.New("path is outside of trusted root")
}
