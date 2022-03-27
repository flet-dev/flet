package model

import (
	"errors"
	"fmt"
	"strings"

	"github.com/flet-dev/flet/server/config"
	"github.com/flet-dev/flet/server/utils"
	"github.com/gosimple/slug"
)

const (
	publicAccount = "p"
	maxSlugSize   = 60
)

type PageName struct {
	Account string
	Name    string
}

func ParsePageName(pageName string) (*PageName, error) {

	p := &PageName{}
	p.Name = strings.ToLower(strings.Trim(strings.ReplaceAll(pageName, "\\", "/"), "/"))

	if strings.Count(p.Name, "/") > 1 {
		return nil, errors.New("Page name must be in format {page} or {namespace}/{page}")
	}

	if strings.Count(p.Name, "/") == 1 {
		// namespace specified
		parts := strings.Split(p.Name, "/")
		p.Account = parts[0]
		p.Name = parts[1]
	} else {
		p.Account = publicAccount
	}

	rndText, err := utils.GenerateRandomString(16)
	if err != nil {
		return nil, err
	}

	p.Name = strings.ReplaceAll(p.Name, "*", rndText)

	p.Account = slug.Make(p.Account)
	if len(p.Account) > maxSlugSize {
		return nil, fmt.Errorf("account name exceeds the maximum allowed size of %d symbols", maxSlugSize)
	}
	p.Name = slug.Make(p.Name)
	if len(p.Name) > maxSlugSize {
		return nil, fmt.Errorf("page name exceeds the maximum allowed size of %d symbols", maxSlugSize)
	}

	return p, nil
}

func (pn *PageName) IsReserved() bool {
	if utils.ContainsString(config.ReservedAccountNames(), pn.Account) {
		return true
	}
	if utils.ContainsString(config.ReservedPageNames(), pn.String()) {
		return true
	}
	return false
}

func (pn *PageName) String() string {
	return fmt.Sprintf("%s/%s", pn.Account, pn.Name)
}
