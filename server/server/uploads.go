package server

import (
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"time"

	"github.com/flet-dev/flet/server/config"
	"github.com/flet-dev/flet/server/page"
	"github.com/flet-dev/flet/server/utils"
	"github.com/gin-gonic/gin"
	log "github.com/sirupsen/logrus"
)

func uploadFileAsStream(c *gin.Context) {

	log.Debugln("Upload started")

	if config.UploadRootDir() == "" {
		c.AbortWithError(500, fmt.Errorf("upload root directory (FLET_UPLOAD_ROOT_DIR) is not configured"))
	}

	fileName := c.Query("f")
	expireStr := c.Query("e")
	signature := c.Query("s")

	if fileName == "" || expireStr == "" || signature == "" {
		c.AbortWithError(400, fmt.Errorf("all parameters must be provided: f, e, s"))
	}

	// verify signature
	queryString := page.GetUploadQueryString(fileName, expireStr)
	if page.GetUploadSignature(queryString) != signature {
		c.AbortWithError(400, fmt.Errorf("invalid signature"))
	}

	// check expiration date
	expires, err := time.Parse(time.RFC3339, expireStr)
	if err != nil {
		c.AbortWithError(400, fmt.Errorf("invalid expiration time"))
	}
	if !time.Now().UTC().Before(expires) {
		c.AbortWithError(400, fmt.Errorf("upload URL has expired"))
	}

	cleanUploadRoot := filepath.Clean(config.UploadRootDir())
	fileFullPath := filepath.Join(cleanUploadRoot, filepath.Clean(fileName))
	if err := utils.InTrustedRoot(fileFullPath, cleanUploadRoot); err != nil {
		c.AbortWithError(409, err)
	}

	f, e := os.Create(fileFullPath)
	if e != nil {
		panic(e)
	}
	defer f.Close()
	f.ReadFrom(c.Request.Body)

	log.Debugf("Written %d", c.Request.ContentLength)

	c.String(http.StatusOK, "OK")
}
