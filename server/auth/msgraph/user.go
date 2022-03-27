package msgraph

type User struct {
	Id                string `json:"id"`
	UserPrincipalName string `json:"userPrincipalName"`
	DisplayName       string `json:"displayName"`
	Mail              string `json:"mail"`
}
