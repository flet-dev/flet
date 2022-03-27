package auth

import (
	"testing"
)

func TestHasPermissions(t *testing.T) {

	var anonUser = &SecurityPrincipal{AuthProvider: ""}
	var githubUser = &SecurityPrincipal{AuthProvider: GitHubAuth, Login: "JohnSmith"}
	var githubUserWithGroups = &SecurityPrincipal{AuthProvider: GitHubAuth, Login: "JohnSmith", Groups: []string{"org/Developers", "org/Owners"}}
	var azureUser = &SecurityPrincipal{AuthProvider: AzureAuth, Login: "john@smith.com"}
	var azureUserWithGroups = &SecurityPrincipal{AuthProvider: AzureAuth, Login: "john@smith.com", Groups: []string{"tanant-1/Group1", "tenant-1/Group2"}}

	var permissionsTest = []struct {
		principal   *SecurityPrincipal // input
		permissions string             // arguments
		expected    bool               // expected result
	}{
		// anonymous user
		{anonUser, "", true},
		{anonUser, "*", false},

		// github user
		{githubUser, "*", true},
		{githubUserWithGroups, "github:*", true},
		{githubUserWithGroups, "org/*", true}, // if user belongs to any team in "org" org
		{githubUserWithGroups, "org/dev*", true},

		// azure user
		{azureUser, "*", true},
		{azureUserWithGroups, "azure:*", true},
		{azureUserWithGroups, "jack@bauer.com", false},
		{azureUserWithGroups, "*@smith.com", true}, // all users with @smith.com domain
		{azureUserWithGroups, "*@somedomain.com, */group1", true},
	}

	for _, tt := range permissionsTest {
		actual := tt.principal.HasPermissions(tt.permissions)
		if actual != tt.expected {
			t.Errorf("principal.HasPermissions(%s): expected %v, actual %v", tt.permissions,
				tt.expected, actual)
		}
	}
}
