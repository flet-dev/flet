package auth

import (
	"reflect"
	"testing"

	"github.com/flet-dev/flet/server/utils"
)

func TestSigninOptions(t *testing.T) {

	var signinOptionTests = []struct {
		permissions string         // input
		expected    *SigninOptions // expected result
	}{
		{"", nil},
		{"*", &SigninOptions{GitHubEnabled: true, AzureEnabled: true, GoogleEnabled: true}},
		{"john@smith.com, jack@bauer.com", &SigninOptions{GitHubEnabled: true, AzureEnabled: true, GoogleEnabled: true}},
		{"azure:john@smith.com", &SigninOptions{GitHubEnabled: false, GitHubGroupScope: false, AzureEnabled: true, AzureGroupScope: false}},
		{"*/*", &SigninOptions{GitHubEnabled: true, GitHubGroupScope: true, AzureEnabled: true, AzureGroupScope: true, GoogleEnabled: true, GoogleGroupScope: true}},
		{"github:*", &SigninOptions{GitHubEnabled: true, GitHubGroupScope: false, AzureEnabled: false, AzureGroupScope: false}},
		{"github:flet-dev/devops", &SigninOptions{GitHubEnabled: true, GitHubGroupScope: true, AzureEnabled: false, AzureGroupScope: false}},
		{"azure:*", &SigninOptions{GitHubEnabled: false, GitHubGroupScope: false, AzureEnabled: true, AzureGroupScope: false}},
		{"azure:*/*", &SigninOptions{GitHubEnabled: false, GitHubGroupScope: false, AzureEnabled: true, AzureGroupScope: true}},
		{"*, azure:*/*", &SigninOptions{GitHubEnabled: true, GitHubGroupScope: false, AzureEnabled: true, AzureGroupScope: true, GoogleEnabled: true}},
		{"azure:*, github:*/*", &SigninOptions{GitHubEnabled: true, GitHubGroupScope: true, AzureEnabled: true, AzureGroupScope: false}},
	}

	for _, tt := range signinOptionTests {
		actual := GetSigninOptions(tt.permissions)
		if !reflect.DeepEqual(actual, tt.expected) {
			t.Errorf("GetSigninOptions(%s): expected %v, actual %v", tt.permissions,
				utils.ToJSONIndent(tt.expected), utils.ToJSONIndent(actual))
		}
	}
}
