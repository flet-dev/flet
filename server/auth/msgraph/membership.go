package msgraph

type Membership struct {
	Id          string `json:"id"`
	DisplayName string `json:"displayName"`
}

type MembershipsResponse struct {
	Values []Membership `json:"value"`
}
