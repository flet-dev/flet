package server

import (
	"context"
	"errors"
	"net/http"
	"time"

	"github.com/flet-dev/flet/server/auth"
	"github.com/flet-dev/flet/server/config"
	"github.com/flet-dev/flet/server/store"
	"github.com/flet-dev/flet/server/utils"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/securecookie"
	log "github.com/sirupsen/logrus"
)

const (
	redirectUrlParameter  = "redirect_url"
	groupsUrlParameter    = "groups"
	persistUrlParameter   = "persist"
	principalIdCookieName = "pid"
	principalLifetimeDays = 7
)

func githubAuthHandler(c *gin.Context) {
	oauthHandler(c, auth.GitHubAuth)
}

func azureAuthHandler(c *gin.Context) {
	oauthHandler(c, auth.AzureAuth)
}

func googleAuthHandler(c *gin.Context) {
	oauthHandler(c, auth.GoogleAuth)
}

func oauthHandler(c *gin.Context, authProvider string) {
	code := c.Query("code")
	stateID := c.Query("state")

	if code == "" {
		// initial flow
		redirectURL := c.Query(redirectUrlParameter)
		groupsEnabled := c.Query(groupsUrlParameter) == "1"
		persistAuthCookie := c.Query(persistUrlParameter) == "1"

		stateID, err := saveOAuthState(c.Writer, &auth.State{
			RedirectURL:       redirectURL,
			AuthProvider:      authProvider,
			GroupsEnabled:     groupsEnabled,
			PersistAuthCookie: persistAuthCookie,
		})

		if err != nil {
			c.AbortWithError(http.StatusBadRequest, err)
			return
		}

		// redirect to authorize page
		oauthConfig := auth.GetOauthConfig(authProvider, groupsEnabled)
		c.Redirect(302, oauthConfig.AuthCodeURL(stateID))
	} else {

		// load state from cookie
		if stateID == "" {
			c.AbortWithError(http.StatusBadRequest, errors.New("invalid state"))
			return
		}

		state, err := getOAuthState(c.Request, stateID)
		if err != nil {
			c.AbortWithError(http.StatusBadRequest, err)
			return
		}

		oauthConfig := auth.GetOauthConfig(authProvider, state.GroupsEnabled)

		// request token
		token, err := oauthConfig.Exchange(context.Background(), code)
		if err != nil {
			c.AbortWithError(http.StatusBadRequest, err)
			return
		}

		principalID, err := getPrincipalID(c.Request)
		if err != nil {
			c.AbortWithError(http.StatusInternalServerError, err)
			return
		}

		if principalID != "" {
			store.DeleteSecurityPrincipal(principalID)
		}

		// create new principal and update its details from API
		principal := auth.NewPrincipal(authProvider, c.ClientIP(), c.Request.UserAgent(), state.GroupsEnabled)
		principal.SetToken(token)
		err = principal.UpdateDetails()

		if err != nil {
			c.AbortWithError(http.StatusBadRequest, err)
			return
		}

		log.Debugln(utils.ToJSON(principal))

		deleteCookie(c.Writer, stateID)
		savePrincipalID(c.Writer, principal.UID, state.PersistAuthCookie)
		store.SetSecurityPrincipal(principal, time.Duration(principalLifetimeDays*24)*time.Hour)
		c.Redirect(302, state.RedirectURL)
	}
}

func signoutHandler(c *gin.Context) {
	redirectURL := c.Query(redirectUrlParameter)

	if redirectURL == "" {
		redirectURL = "/"
	}

	principalID, err := getPrincipalID(c.Request)
	if err != nil {
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	if principalID != "" {
		store.DeleteSecurityPrincipal(principalID)
	}
	deleteCookie(c.Writer, principalIdCookieName)
	c.Redirect(302, redirectURL)
}

func saveOAuthState(w http.ResponseWriter, state *auth.State) (string, error) {
	id, _ := utils.GenerateRandomString(32)
	state.Id = id

	sc := getSecureCookie()

	// serialize to a secure cookie
	encoded, err := sc.Encode(id, state)
	if err != nil {
		return "", err
	}

	cookie := &http.Cookie{
		Name:     id,
		Value:    encoded,
		Path:     "/",
		Secure:   true,
		HttpOnly: true,
	}
	http.SetCookie(w, cookie)
	return id, nil
}

func getOAuthState(r *http.Request, stateID string) (*auth.State, error) {
	sc := getSecureCookie()
	cookie, err := r.Cookie(stateID)

	if err != nil {
		return nil, err
	}

	state := &auth.State{}
	err = sc.Decode(stateID, cookie.Value, &state)
	if err != nil {
		return nil, err
	}
	return state, nil
}

func savePrincipalID(w http.ResponseWriter, principalID string, persistAuthCookie bool) error {
	sc := getSecureCookie()

	// serialize to a secure cookie
	encoded, err := sc.Encode(principalIdCookieName, principalID)
	if err != nil {
		return err
	}

	cookie := &http.Cookie{
		Name:     principalIdCookieName,
		Value:    encoded,
		Path:     "/",
		Secure:   true,
		HttpOnly: true,
	}

	if persistAuthCookie {
		cookie.MaxAge = principalLifetimeDays * 24 * 60 * 60
	}

	http.SetCookie(w, cookie)
	return nil
}

func getPrincipalID(r *http.Request) (string, error) {
	sc := getSecureCookie()
	cookie, err := r.Cookie(principalIdCookieName)

	if err == http.ErrNoCookie {
		return "", nil
	} else if err != nil {
		return "", err
	}

	principalID := ""
	err = sc.Decode(principalIdCookieName, cookie.Value, &principalID)
	if err != nil {
		return "", err
	}
	return principalID, nil
}

func getSecureCookie() *securecookie.SecureCookie {
	return securecookie.New(utils.GetCipherKey(config.CookieSecret()), utils.GetCipherKey(config.MasterSecretKey()))
}

func deleteCookie(w http.ResponseWriter, name string) {
	cookie := &http.Cookie{
		Name:     name,
		Path:     "/",
		Secure:   true,
		HttpOnly: true,
		MaxAge:   -1,
	}
	http.SetCookie(w, cookie)
}
