package server

import (
	"context"
	"embed"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"sync"
	"time"

	"github.com/gorilla/websocket"
	log "github.com/sirupsen/logrus"

	"github.com/flet-dev/flet/server/auth"
	"github.com/flet-dev/flet/server/config"
	"github.com/flet-dev/flet/server/page"
	page_connection "github.com/flet-dev/flet/server/page/connection"
	"github.com/flet-dev/flet/server/store"
	"github.com/flet-dev/flet/server/utils"
	"github.com/gin-gonic/contrib/secure"
	"github.com/gin-gonic/contrib/static"
	"github.com/gin-gonic/gin"
)

const (
	apiRoutePrefix      string = "/api"
	siteDefaultDocument string = "index.html"
)

var (
	Port int = 8550
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

type fletFS struct {
	prefix string
	httpFS http.FileSystem
}

func newFletFS(prefix string, efs embed.FS) fletFS {
	return fletFS{
		prefix: prefix,
		httpFS: http.FS(efs),
	}
}

func (pfs fletFS) Exists(prefix string, path string) bool {
	f, err := pfs.httpFS.Open(pfs.fileName(path))
	if f != nil {
		f.Close()
	}
	return err == nil
}

func (pfs fletFS) Open(name string) (http.File, error) {
	return pfs.httpFS.Open(pfs.fileName(name))
}

func (pfs fletFS) fileName(name string) string {
	return pfs.prefix + strings.TrimLeft(name, "/")
}

func Start(ctx context.Context, wg *sync.WaitGroup, serverPort int) {
	defer wg.Done()

	Port = serverPort

	// Set the router as the default one shipped with Gin
	router := gin.Default()

	if config.TrustedProxies() != nil && len(config.TrustedProxies()) > 0 {
		log.Println("Trusted proxies:", config.TrustedProxies())
		router.SetTrustedProxies(config.TrustedProxies())
	}

	// force SSL
	if config.ForceSSL() {
		router.Use(secure.Secure(secure.Options{
			AllowedHosts:          []string{},
			SSLRedirect:           true,
			SSLHost:               "", // use the same host
			SSLProxyHeaders:       map[string]string{"X-Forwarded-Proto": "https"},
			STSSeconds:            315360000,
			STSIncludeSubdomains:  true,
			FrameDeny:             true,
			ContentTypeNosniff:    true,
			BrowserXssFilter:      true,
			ContentSecurityPolicy: "",
		}))
	}

	// Serve frontend static files
	router.Use(static.Serve("/", newFletFS(contentRootFolder, f)))

	// WebSockets
	router.GET("/ws", func(c *gin.Context) {
		websocketHandler(c)
	})

	// Setup route group for the API
	api := router.Group(apiRoutePrefix)
	{
		api.GET("/", func(c *gin.Context) {
			time.Sleep(4 * time.Second)
			c.JSON(http.StatusOK, gin.H{
				"message": "pong",
			})
		})
	}

	api.GET("/oauth/github", githubAuthHandler)
	api.GET("/oauth/azure", azureAuthHandler)
	api.GET("/oauth/google", googleAuthHandler)
	api.GET("/auth/signout", signoutHandler)

	// unknown API routes - 404, all the rest - index.html
	router.NoRoute(func(c *gin.Context) {
		if !strings.HasPrefix(c.Request.RequestURI, apiRoutePrefix+"/") {
			// SPA index.html
			index, _ := f.Open(contentRootFolder + siteDefaultDocument)
			indexData, _ := ioutil.ReadAll(index)
			c.Data(http.StatusOK, "text/html", indexData)
		} else {
			// API not found
			c.JSON(http.StatusNotFound, gin.H{
				"message": "API endpoint not found",
			})
		}
	})

	log.Println("Starting server on port", serverPort)

	// Start and run the server
	srv := &http.Server{
		Addr:    fmt.Sprintf(":%d", serverPort),
		Handler: router,
	}

	// Initializing the server in a goroutine so that
	// it won't block the graceful shutdown handling below
	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %s\n", err)
		}
	}()

	go func() {
		page.RunBackgroundTasks(ctx)
	}()

	<-ctx.Done()

	log.Println("Shutting down server...")

	// The context is used to inform the server it has 5 seconds to finish
	// the request it is currently handling
	ctxShutDown, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctxShutDown); err != nil {
		log.Fatal("Server forced to shutdown:", err)
	}

	log.Println("Server exited")
}

func websocketHandler(c *gin.Context) {

	// load current security principal
	principal, err := getSecurityPrincipal(c)
	if err != nil {
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	upgrader.CheckOrigin = func(r *http.Request) bool {
		return true
	}

	conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		log.Errorln("Error upgrading WebSocket connection:", err)
		return
	}

	wsc := page_connection.NewWebSocket(conn)
	page.NewClient(wsc, c.ClientIP(), principal)
}

func getSecurityPrincipal(c *gin.Context) (*auth.SecurityPrincipal, error) {
	principalID, err := getPrincipalID(c.Request)
	if err != nil {
		return nil, err
	}

	var principal *auth.SecurityPrincipal
	if principalID != "" {
		principal = store.GetSecurityPrincipal(principalID)
		if principal == nil {
			return nil, nil
		} else if principal.ClientIP != c.ClientIP() || principal.UserAgentHash != utils.SHA1(c.Request.UserAgent()) {
			log.Errorln("Principal not found or its IP address or User Agent do not match")
			store.DeleteSecurityPrincipal(principalID)
		} else {
			err := principal.UpdateDetails()
			if err != nil {
				log.Errorln("Error updating principal details:", err)
				store.DeleteSecurityPrincipal(principalID)
				return nil, nil
			}
			store.SetSecurityPrincipal(principal, time.Duration(principalLifetimeDays*24)*time.Hour)
		}
	}
	return principal, nil
}
