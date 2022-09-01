package server

import (
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
		c.JSON(500, gin.H{"message": "upload root directory (FLET_UPLOAD_ROOT_DIR) is not configured"})
		return
	}

	fileName := c.Query("f")
	expireStr := c.Query("e")
	signature := c.Query("s")

	if fileName == "" || expireStr == "" || signature == "" {
		c.JSON(400, gin.H{"message": "all parameters must be provided: f, e, s"})
		return
	}

	// verify signature
	queryString := page.GetUploadQueryString(fileName, expireStr)
	if page.GetUploadSignature(queryString) != signature {
		c.JSON(400, gin.H{"message": "invalid signature"})
		return
	}

	// check expiration date
	expires, err := time.Parse(time.RFC3339, expireStr)
	if err != nil {
		c.JSON(400, gin.H{"message": "invalid expiration time"})
		return
	}
	if !time.Now().UTC().Before(expires) {
		c.JSON(400, gin.H{"message": "upload URL has expired"})
		return
	}

	cleanUploadRoot := filepath.Clean(config.UploadRootDir())
	fileFullPath := filepath.Join(cleanUploadRoot, filepath.Clean(fileName))
	if err := utils.InTrustedRoot(fileFullPath, cleanUploadRoot); err != nil {
		c.JSON(409, gin.H{"message": err})
		return
	}

	// create directory if not exists
	os.MkdirAll(filepath.Dir(fileFullPath), os.ModePerm)

	// file to save request stream
	f, e := os.Create(fileFullPath)
	if e != nil {
		panic(e)
	}
	defer f.Close()
	_, err = f.ReadFrom(c.Request.Body)
	if err != nil {
		c.JSON(500, gin.H{"message": err})
		return
	}

	log.Debugf("Written %d", c.Request.ContentLength)

	c.String(http.StatusOK, "OK")
}
