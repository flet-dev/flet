package auth

import (
	"strings"

	"github.com/flet-dev/flet/server/utils"
)

type SigninOptions struct {
	GitHubEnabled    bool `json:"gitHubEnabled"`
	GitHubGroupScope bool `json:"gitHubGroupScope"`
	AzureEnabled     bool `json:"azureEnabled"`
	AzureGroupScope  bool `json:"azureGroupScope"`
	GoogleEnabled    bool `json:"googleEnabled"`
	GoogleGroupScope bool `json:"googleGroupScope"`
}

func GetSigninOptions(permissions string) *SigninOptions {

	if permissions == "" {
		return nil
	}

	opts := &SigninOptions{}

	// parse permissions
	permList := utils.SplitAndTrim(permissions, ",")

	for _, permission := range permList {
		// check permission's auth type
		authType := ""
		colonIdx := strings.Index(permission, ":")
		if colonIdx != -1 {
			authType = strings.ToLower(permission[:colonIdx])
			permission = permission[colonIdx+1:]
		}

		opts.GitHubEnabled = opts.GitHubEnabled || authType == "" || authType == GitHubAuth
		opts.AzureEnabled = opts.AzureEnabled || authType == "" || authType == AzureAuth
		opts.GoogleEnabled = opts.GoogleEnabled || authType == "" || authType == GoogleAuth

		// check if the requested permission is a group
		if strings.Contains(permission, "/") {
			opts.GitHubGroupScope = opts.GitHubGroupScope || (opts.GitHubEnabled && authType == "" || authType == GitHubAuth)
			opts.AzureGroupScope = opts.AzureGroupScope || (opts.AzureEnabled && authType == "" || authType == AzureAuth)
			opts.GoogleGroupScope = opts.GoogleGroupScope || (opts.GoogleEnabled && authType == "" || authType == GoogleAuth)
		}
	}

	return opts
}
