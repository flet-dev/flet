package utils

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/sha1"
	"encoding/base64"
	"errors"
	"fmt"
	"io"

	"github.com/flet-dev/flet/server/config"
)

// SHA1 returns SHA1 hash of the input string.
func SHA1(value string) string {
	h := sha1.New()
	io.WriteString(h, value)
	return fmt.Sprintf("%x", h.Sum(nil))
}

func EncryptWithMasterKey(data []byte) ([]byte, error) {
	return EncryptWithKey(data, config.MasterSecretKey())
}

func EncryptWithKey(data []byte, secretKey string) ([]byte, error) {
	block, err := aes.NewCipher(GetCipherKey(secretKey))
	if err != nil {
		return nil, err
	}

	aesgcm, err := cipher.NewGCM(block)
	if err != nil {
		panic(err.Error())
	}

	nonce := make([]byte, aesgcm.NonceSize())
	if _, err = io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, err
	}

	return aesgcm.Seal(nonce, nonce, data, nil), nil
}

func DecryptWithMasterKey(data []byte) ([]byte, error) {
	return DecryptWithKey(data, config.MasterSecretKey())
}

func DecryptWithKey(cipherData []byte, secretKey string) ([]byte, error) {
	block, err := aes.NewCipher(GetCipherKey(secretKey))
	if err != nil {
		return nil, err
	}

	aesgcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	nonceSize := aesgcm.NonceSize()
	nonce, ciphertext := cipherData[:nonceSize], cipherData[nonceSize:]

	plaintext, err := aesgcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return nil, err
	}

	return plaintext, nil
}

func GetCipherKey(secretKey string) []byte {
	key := make([]byte, 32)
	for i, b := range []byte(secretKey)[:32] {
		key[i] = b
	}
	return key
}

// source: https://github.com/gorilla/securecookie/blob/master/securecookie.go
func GenerateRandomKey(length int) []byte {
	k := make([]byte, length)
	if _, err := io.ReadFull(rand.Reader, k); err != nil {
		return nil
	}
	return k
}

func EncodeBase64(value []byte) string {
	encoded := make([]byte, base64.URLEncoding.EncodedLen(len(value)))
	base64.URLEncoding.Encode(encoded, value)
	return string(encoded)
}

func DecodeBase64(value string) ([]byte, error) {
	decoded := make([]byte, base64.URLEncoding.DecodedLen(len(value)))
	b, err := base64.URLEncoding.Decode(decoded, []byte(value))
	if err != nil {
		return nil, errors.New("base64 decode failed")
	}
	return decoded[:b], nil
}
