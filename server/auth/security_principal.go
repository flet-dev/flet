package auth

import (
	"errors"
	"strings"
	"time"

	"github.com/flet-dev/flet/server/utils"
	"github.com/gobwas/glob"
	"golang.org/x/oauth2"
)

type SecurityPrincipal struct {
	UID           string    `json:"uid"`
	ID            string    `json:"id"`
	AuthProvider  string    `json:"authProvider"`
	Token         string    `json:"token"`
	Login         string    `json:"login"`
	Name          string    `json:"name"`
	Email         string    `json:"email"`
	Groups        []string  `json:"groups"`
	ClientIP      string    `json:"clientIP"`
	UserAgentHash string    `json:"userAgentHash"`
	Created       time.Time `json:"created,omitempty"`
}

func NewPrincipal(authProvider string, clientIP string, userAgent string, groupsEnabled bool) *SecurityPrincipal {

	uid, _ := utils.GenerateRandomString(32)

	p := &SecurityPrincipal{
		UID:           uid,
		AuthProvider:  authProvider,
		ClientIP:      clientIP,
		UserAgentHash: utils.SHA1(userAgent),
		Created:       time.Now().UTC(),
	}

	if groupsEnabled {
		p.Groups = make([]string, 0)
	}

	return p
}

func (p *SecurityPrincipal) SetToken(token *oauth2.Token) error {
	if token == nil {
		p.Token = ""
		return nil
	}

	j := utils.ToJSON(token)
	enc, err := utils.EncryptWithMasterKey([]byte(j))
	if err != nil {
		return err
	}
	p.Token = utils.EncodeBase64(enc)
	return nil
}

func (p *SecurityPrincipal) GetToken() (*oauth2.Token, error) {
	if p.Token == "" {
		return nil, nil
	}

	decoded, err := utils.DecodeBase64(p.Token)
	if err != nil {
		return nil, err
	}

	j, err := utils.DecryptWithMasterKey(decoded)
	if err != nil {
		return nil, err
	}

	token := &oauth2.Token{}
	utils.FromJSON(string(j), token)
	return token, nil
}

func (p *SecurityPrincipal) UpdateDetails() error {
	if p.AuthProvider == GitHubAuth {
		return p.updateFromGitHub()
	} else if p.AuthProvider == AzureAuth {
		return p.updateFromAzure()
	} else if p.AuthProvider == GoogleAuth {
		return p.updateFromGoogle()
	} else if p.AuthProvider == "" {
		return errors.New("auth provider is not set")
	} else {
		return errors.New("unknown auth provider")
	}
}

func (p *SecurityPrincipal) Signout() error {
	if p.AuthProvider == GitHubAuth {
		return p.signoutGitHub()
	} else if p.AuthProvider == AzureAuth {
		return p.signoutAzure()
	} else if p.AuthProvider == GoogleAuth {
		return p.signoutGoogle()
	}
	return nil
}

func (p *SecurityPrincipal) HasPermissions(permissions string) bool {

	if permissions == "" {
		return true
	}

	if p.AuthProvider == "" {
		return false
	}

	// parse permissions
	permList := utils.SplitAndTrim(permissions, ",")

	for _, permission := range permList {

		// check permission's auth type
		authType := ""
		colonIdx := strings.Index(permission, ":")
		if colonIdx != -1 {
			authType = strings.ToLower(strings.TrimSpace(permission[:colonIdx]))
			permission = strings.TrimSpace(permission[colonIdx+1:])
		}

		authTypeMatched := authType == "" || p.AuthProvider == authType
		identityMatched := false

		pg := glob.MustCompile(strings.ToLower(permission))

		if strings.Contains(permission, "/") && p.Groups != nil && len(p.Groups) > 0 {
			// check group
			for _, group := range p.Groups {
				if pg.Match(strings.ToLower(group)) {
					identityMatched = true
					break
				}
			}
		} else if (p.Login != "" && pg.Match(strings.ToLower(p.Login))) ||
			(p.Email != "" && pg.Match(strings.ToLower(p.Email))) {
			identityMatched = true
		}

		if authTypeMatched && identityMatched {
			return true
		}
	}
	return false
}
