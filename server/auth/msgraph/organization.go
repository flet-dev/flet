package msgraph

type Organization struct {
	Id          string `json:"id"`
	DisplayName string `json:"displayName"`
}

type OrganizationsResponse struct {
	Values []Organization `json:"value"`
}
