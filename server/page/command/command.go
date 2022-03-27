package command

import (
	"fmt"
	"strings"
	"text/scanner"
	"unicode"

	"github.com/flet-dev/flet/server/utils"
)

const (
	Add       string = "add"
	Addf      string = "addf"
	Replace   string = "replace"
	Replacef  string = "replacef"
	Set       string = "set"
	Setf      string = "setf"
	Append    string = "append"
	Appendf   string = "appendf"
	Get       string = "get"
	Clean     string = "clean"
	Cleanf    string = "cleanf"
	Remove    string = "remove"
	Removef   string = "removef"
	Begin     string = "begin"
	End       string = "end"
	CanAccess string = "canaccess"
	Signout   string = "signout"
	Close     string = "close"
	Error     string = "error"
)

var (
	supportedCommands = map[string]*CommandMetadata{
		Add:       {Name: Add, ShouldReturn: true},
		Addf:      {Name: Addf, ShouldReturn: false},
		Replace:   {Name: Replace, ShouldReturn: true},
		Replacef:  {Name: Replacef, ShouldReturn: false},
		Set:       {Name: Set, ShouldReturn: true},
		Setf:      {Name: Setf, ShouldReturn: false},
		Append:    {Name: Set, ShouldReturn: true},
		Appendf:   {Name: Setf, ShouldReturn: false},
		Get:       {Name: Get, ShouldReturn: true},
		Clean:     {Name: Clean, ShouldReturn: true},
		Cleanf:    {Name: Cleanf, ShouldReturn: false},
		Remove:    {Name: Remove, ShouldReturn: true},
		Removef:   {Name: Removef, ShouldReturn: false},
		Begin:     {Name: Begin, ShouldReturn: false},
		End:       {Name: End, ShouldReturn: true},
		CanAccess: {Name: CanAccess, ShouldReturn: true},
		Signout:   {Name: Signout, ShouldReturn: true},
		Close:     {Name: Close, ShouldReturn: false},
		Error:     {Name: Error, ShouldReturn: false},
	}
)

type Command struct {
	Indent   int
	Name     string // mandatory command name
	Values   []string
	Attrs    map[string]string
	Lines    []string
	Commands []*Command
}

type CommandMetadata struct {
	Name         string
	ShouldReturn bool
}

func Parse(cmdText string, parseName bool) (*Command, error) {

	var command *Command = nil
	var err error

	lines := strings.Split(cmdText, "\n")
	for _, line := range lines {

		// 1st non-empty line contains command
		if command == nil {
			if !utils.WhiteSpaceOnly(line) {
				// parse command
				command, err = parseCommandLine(line, parseName)
				if err != nil {
					return nil, err
				}
			}
		} else {
			command.Lines = append(command.Lines, strings.Trim(line, "\r"))
		}
	}

	return command, nil
}

func parseCommandLine(line string, parseName bool) (*Command, error) {
	command := &Command{
		Attrs:  make(map[string]string),
		Values: make([]string, 0),
		Lines:  make([]string, 0),
	}

	command.Indent = utils.CountIndent(line)

	var err error
	var s scanner.Scanner
	s.Init(strings.NewReader(line))
	s.Filename = "command"
	s.Error = func(s *scanner.Scanner, msg string) {
		if msg != "invalid char literal" {
			err = fmt.Errorf("error parsing command at position %d: %s", s.Column, msg)
		}
	}

	// treat ':' as part of an identifier
	s.IsIdentRune = func(ch rune, i int) bool {
		return ch == ':' || ch == '_' || ch == '-' || ch == '.' || unicode.IsLetter(ch) || unicode.IsDigit(ch)
	}

	prevToken := ""
	prevLit := ""
	for r := s.Scan(); r != scanner.EOF; r = s.Scan() {

		if err != nil {
			return nil, err
		}

		tok := s.TokenText()

		//fmt.Printf("%s: %s\n", s.Position, tok)

		if tok == "=" {
			if prevLit == "" || prevToken == "=" {
				return nil, fmt.Errorf("unexpected '=' at position %d", s.Column)
			}
		} else if tok != "=" && prevToken == "=" && prevLit != "" {
			// name=value
			command.Attrs[strings.ToLower(utils.TrimQuotes(prevLit))] = utils.ReplaceEscapeSymbols(utils.TrimQuotes(tok))
			prevLit = ""
		} else if tok != "=" && prevToken != "=" && prevLit != "" {
			v := utils.TrimQuotes(prevLit)
			if command.Name == "" && parseName {
				command.Name = utils.ReplaceEscapeSymbols(v)
			} else {
				command.Values = append(command.Values, utils.ReplaceEscapeSymbols(utils.TrimQuotes(v)))
			}
			prevLit = tok
		} else {
			prevLit = tok
		}
		prevToken = tok
	}

	// consume last token collected
	if prevLit != "" {
		if command.Name == "" && parseName {
			command.Name = utils.ReplaceEscapeSymbols(prevLit)
		} else {
			command.Values = append(command.Values, utils.ReplaceEscapeSymbols(utils.TrimQuotes(prevLit)))
		}
	}

	if parseName && !command.IsSupported() {
		return nil, fmt.Errorf("unknown command: %s", command.Name)
	}

	return command, nil
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
	return fmt.Sprintf("%s %s %s\n%s", cmd.Name, strings.Join(cmd.Values, " "), strings.Join(attrs, " "), strings.Join(cmd.Lines, "\n"))
}
