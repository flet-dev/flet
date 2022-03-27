package utils

import (
	"crypto/rand"
	"encoding/json"
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

// GenerateRandomString returns a crypto-strong random string of specified length.
func GenerateRandomString(n int) (string, error) {
	const alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"

	// generate a random slice of bytes
	bytes := make([]byte, n)
	_, err := rand.Read(bytes)
	if err != nil {
		return "", err
	}

	for i, b := range bytes {
		bytes[i] = alphabet[b%byte(len(alphabet))]
	}
	return string(bytes), nil
}

func ContainsString(arr []string, str string) bool {
	for _, a := range arr {
		if a == str {
			return true
		}
	}
	return false
}

// https://stackoverflow.com/questions/46128016/insert-a-value-in-a-slice-at-a-given-index
func SliceInsert(arr []interface{}, elem interface{}, index int) []interface{} {
	if index >= len(arr) { // nil or empty slice or after last element
		return append(arr, elem)
	}
	arr = append(arr[:index+1], arr[index:]...) // index < len(a)
	arr[index] = elem
	return arr
}

func SliceRemove(arr []interface{}, elem interface{}) []interface{} {
	for i, v := range arr {
		if v == elem {
			return append(arr[:i], arr[i+1:]...)
		}
	}
	return arr
}

func TrimQuotes(s string) string {
	if strings.HasPrefix(s, "\"") && strings.HasSuffix(s, "\"") {
		return strings.ReplaceAll(s[1:len(s)-1], "'", "\\'")
	} else if strings.HasPrefix(s, "'") && strings.HasSuffix(s, "'") {
		return strings.ReplaceAll(s[1:len(s)-1], "\"", "\\\"")
	}
	return s
}

func ReplaceEscapeSymbols(s string) string {
	//fmt.Println("ReplaceEscapeSymbols:", s)
	r, err := strconv.Unquote(fmt.Sprintf("\"%s\"",
		strings.ReplaceAll(s, "\\'", "'")))
	if err != nil {
		//fmt.Println("ERROR unescaping:", err, ":", s)
		return s
	}
	return r
}

func WhiteSpaceOnly(s string) bool {
	re := regexp.MustCompile(`[^\s]+`)
	return !re.Match([]byte(s))
}

func CountIndent(s string) int {
	re := regexp.MustCompile(`\s*`)
	r := string(re.Find([]byte(s)))
	r = strings.ReplaceAll(r, "\t", "    ")
	return len(r)
}

func CountRune(s string, r rune) int {
	count := 0
	for _, c := range s {
		if c == r {
			count++
		}
	}
	return count
}

func ToJSON(v interface{}) string {
	json, _ := json.Marshal(v)
	return string(json)
}

func FromJSON(src string, dst interface{}) {
	_ = json.Unmarshal([]byte(src), dst)
}

func ToJSONIndent(v interface{}) string {
	json, _ := json.MarshalIndent(v, "", "  ")
	return string(json)
}

func SplitAndTrim(str string, delim string) []string {
	items := strings.Split(str, delim)
	results := make([]string, 0)
	for _, item := range items {
		item = strings.TrimSpace(item)
		if item != "" {
			results = append(results, item)
		}
	}
	return results
}
