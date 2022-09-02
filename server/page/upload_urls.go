package page

import (
	"crypto/sha256"
	"fmt"
	"net/url"
	"time"

	"github.com/flet-dev/flet/server/config"
)

func GetUploadUrl(fileName string, expiresInSeconds int) string {
	expireStr := time.Now().Add(time.Duration(expiresInSeconds) * time.Second).UTC().Format(time.RFC3339)
	queryString := GetUploadQueryString(fileName, expireStr)
	signature := GetUploadSignature(queryString)
	return fmt.Sprintf("/api/upload?%s&s=%s", queryString, signature)
}

func GetUploadQueryString(fileName string, expireStr string) string {
	v := url.Values{}
	v.Add("f", fileName)
	v.Add("e", expireStr)
	return v.Encode()
}

func GetUploadSignature(queryString string) string {
	h := sha256.New()
	h.Write([]byte(queryString))
	h.Write([]byte(config.MasterSecretKey()))
	return fmt.Sprintf("%x", h.Sum(nil))
}
