package model

import (
	"encoding/json"
	"strconv"
	"strings"

	"github.com/flet-dev/flet/server/utils"
)

var (
	systemAttrs = []string{
		"id",
		"to",
		"from",
		"at",
		"t",
		"p",
		"i",
		"c",
	}
)

// Control is an element of a page.
type Control map[string]interface{}

// NewControl initializes a new control object.
func NewControl(controlType string, parentID string, id string) *Control {
	ctl := Control{}
	ctl["t"] = controlType
	ctl["p"] = parentID
	ctl["i"] = id
	ctl["c"] = make([]string, 0)
	return &ctl
}

// NewControlFromJSON initializes a new control instance from JSON.
func NewControlFromJSON(jsonCtrl string) (*Control, error) {
	ctrl := &Control{}
	err := json.Unmarshal([]byte(jsonCtrl), ctrl)
	if err != nil {
		return nil, err
	}
	return ctrl, nil
}

func (ctl *Control) GetAttr(name string) interface{} {
	return (*ctl)[strings.ToLower(name)]
}

func (ctl *Control) SetAttr(name string, value string) {
	lname := strings.ToLower(name)
	if value != "" {
		(*ctl)[lname] = value
	} else {
		delete((*ctl), lname)
	}
}

func (ctl *Control) AppendAttr(name string, value string) {
	lname := strings.ToLower(name)
	(*ctl)[lname] = (*ctl)[lname].(string) + value
}

func (ctl *Control) CleanAttrs() {
	for name := range *ctl {
		if !IsSystemAttr(name) {
			delete((*ctl), name)
		}
	}
}

// ID returns control's ID.
func (ctl *Control) ID() string {
	return (*ctl)["i"].(string)
}

func (ctl *Control) At() int {
	at, ok := (*ctl)["at"].(string)
	if ok && len(at) > 0 {
		if a, err := strconv.Atoi(at); err == nil {
			return a
		}
	}
	return -1
}

// ParentID returns the ID of parent control.
func (ctl *Control) ParentID() string {
	return (*ctl)["p"].(string)
}

// AddChildID appends the child to the parent control.
func (ctl *Control) AddChildID(childID string) {
	childIds, _ := (*ctl)["c"].([]interface{})
	(*ctl)["c"] = append(childIds, childID)
}

func (ctl *Control) InsertChildID(childID string, at int) {
	childIds, _ := (*ctl)["c"].([]interface{})
	(*ctl)["c"] = utils.SliceInsert(childIds, childID, at)
}

func (ctl *Control) RemoveChild(childID string) {
	childIds, _ := (*ctl)["c"].([]interface{})
	(*ctl)["c"] = utils.SliceRemove(childIds, childID)
}

func (ctl *Control) RemoveChildren() {
	(*ctl)["c"] = make([][]interface{}, 0)
}

func (ctl *Control) GetChildrenIds() []string {
	ids, _ := (*ctl)["c"].([]interface{})
	result := make([]string, len(ids))
	for i, id := range ids {
		result[i] = id.(string)
	}
	return result
}

func (ctl *Control) CopyChildren(srcCtl *Control) {
	ids, _ := (*srcCtl)["c"].([]interface{})
	copy := make([]string, len(ids))
	for i, id := range ids {
		copy[i] = id.(string)
	}
	(*ctl)["c"] = copy
}

func IsSystemAttr(name string) bool {
	return utils.ContainsString(systemAttrs, strings.ToLower(name))
}
