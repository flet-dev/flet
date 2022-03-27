package utils

import (
	"reflect"
	"testing"
)

type Principal struct {
	UID          string   `json:"uid"`
	Username     string   `json:"username"`
	Email        string   `json:"email"`
	AuthProvider bool     `json:"authProvider"`
	Token        string   `json:"token"`
	Groups       []string `json:"groups"`
}

func TestJsonSerialization(t *testing.T) {
	actual := &Principal{
		UID:      "12345",
		Username: "test_user",
		Groups:   []string{"g1", "g2"},
	}
	encoded := ToJSON(actual)

	expected := &Principal{}
	FromJSON(encoded, &expected)

	if !reflect.DeepEqual(actual, expected) {
		t.Errorf("ToJSON/FromJSON: expected %v, actual %v", expected, actual)
	}
}

func TestGenerateRandomString(t *testing.T) {
	s, err := GenerateRandomString(32)
	if err != nil {
		t.Error("GenerateRandomString should not fail")
	}
	t.Log(s)
}
