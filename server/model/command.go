package model

import (
	"fmt"
	"strings"
)

const (
	AddCommand       string = "add"
	ReplaceCommand   string = "replace"
	SetCommand       string = "set"
	AppendCommand    string = "append"
	GetCommand       string = "get"
	CleanCommand     string = "clean"
	RemoveCommand    string = "remove"
	BeginCommand     string = "begin"
	EndCommand       string = "end"
	CanAccessCommand string = "canaccess"
	SignoutCommand   string = "signout"
	CloseCommand     string = "close"
	ErrorCommand     string = "error"
)

var (
	supportedCommands = map[string]*CommandMetadata{
		AddCommand:       {Name: AddCommand, ShouldReturn: true},
		ReplaceCommand:   {Name: ReplaceCommand, ShouldReturn: true},
		SetCommand:       {Name: SetCommand, ShouldReturn: true},
		AppendCommand:    {Name: SetCommand, ShouldReturn: true},
		GetCommand:       {Name: GetCommand, ShouldReturn: true},
		CleanCommand:     {Name: CleanCommand, ShouldReturn: true},
		RemoveCommand:    {Name: RemoveCommand, ShouldReturn: true},
		BeginCommand:     {Name: BeginCommand, ShouldReturn: false},
		EndCommand:       {Name: EndCommand, ShouldReturn: true},
		CanAccessCommand: {Name: CanAccessCommand, ShouldReturn: true},
		SignoutCommand:   {Name: SignoutCommand, ShouldReturn: true},
		CloseCommand:     {Name: CloseCommand, ShouldReturn: false},
		ErrorCommand:     {Name: ErrorCommand, ShouldReturn: false},
	}
)

type Command struct {
	Indent   int               `json:"i"`
	Name     string            `json:"n"`
	Values   []string          `json:"v"`
	Attrs    map[string]string `json:"a"`
	Commands []*Command        `json:"c"`
}

type CommandMetadata struct {
	Name         string
	ShouldReturn bool
}

func (cmd *Command) IsSupported() bool {
	name := strings.ToLower(cmd.Name)
	_, commandExists := supportedCommands[name]
	return commandExists
}

func (cmd *Command) ShouldReturn() bool {
	cmdMeta := supportedCommands[strings.ToLower(cmd.Name)]
	return cmdMeta.ShouldReturn
}

func (cmd *Command) String() string {
	attrs := make([]string, 0)
	for k, v := range cmd.Attrs {
		attrs = append(attrs, fmt.Sprintf("%s=\"%s\"", k, v))
	}
	return fmt.Sprintf("%s %s %s", cmd.Name, strings.Join(cmd.Values, " "), strings.Join(attrs, " "))
}
