//go:build !windows

package utils

import (
	"os/exec"
	"syscall"
)

func GetDetachedCmd(name string, arg ...string) *exec.Cmd {
	cmd := exec.Command(name, arg...)
	cmd.SysProcAttr = &syscall.SysProcAttr{
		Setpgid: true,
		Pgid:    0,
	}
	return cmd
}
