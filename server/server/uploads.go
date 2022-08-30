package server

import (
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	log "github.com/sirupsen/logrus"
)

func uploadFile(c *gin.Context) {

	log.Println(("UploadFile started"))

	// single file
	file, _ := c.FormFile("file")
	log.Println(file.Filename)

	// Upload the file to specific dst.
	c.SaveUploadedFile(file, "C:\\projects\\2\\"+file.Filename)

	c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
}

func uploadFiles(c *gin.Context) {
	// Multipart form
	form, _ := c.MultipartForm()
	files := form.File["upload[]"]

	for _, file := range files {
		log.Println(file.Filename)

		// Upload the file to specific dst.
		c.SaveUploadedFile(file, "C:\\projects\\2\\"+file.Filename)
	}
	c.String(http.StatusOK, fmt.Sprintf("%d files uploaded!", len(files)))
}

func uploadFilesStream(c *gin.Context) {

	log.Println("Upload started")

	time.Sleep(8 * time.Second)
	f, e := os.Create("C:\\projects\\2\\test.txt")
	if e != nil {
		panic(e)
	}
	defer f.Close()
	f.ReadFrom(c.Request.Body)

	log.Printf("Written %d", c.Request.ContentLength)

	c.String(http.StatusOK, "File uploaded!")
}
