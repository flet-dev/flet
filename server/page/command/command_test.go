package command

import (
	"fmt"
	"log"
	"testing"

	"github.com/flet-dev/flet/server/utils"
)

func TestTrimQuotes(t *testing.T) {

	r := utils.TrimQuotes("\"Hello, world!\"")
	expR := "Hello, world!"

	if r != expR {
		t.Errorf("TestTrimQuotes returned %s, want %s", r, expR)
	}
}

func TestUnquote(t *testing.T) {

	r := utils.ReplaceEscapeSymbols("Hello, \\\"world!\\\"")
	fmt.Println("Original:", r)

	expR := "Hello, \"world!\""
	fmt.Println("Expected:", expR)

	if r != expR {
		t.Errorf("TestUnquote returned %s, want %s", r, expR)
	}
}

func TestUnquote2(t *testing.T) {

	cmdText := "add text markdown text='\"line 1\"' value='```powershell\\nInvoke-Flet \"clean page\"\\n```'"
	fmt.Println(cmdText)

	cmd, err := Parse(cmdText, true)
	if err != nil {
		t.Fatal("Error parsing command", err)
	}

	fmt.Println("TestUnquote2:", cmd)
}

func TestUnquote3(t *testing.T) {

	r := utils.ReplaceEscapeSymbols("line\\\"1")
	fmt.Println("Original:", r)

	expR := "line\"1"
	fmt.Println("Expected:", expR)

	if r != expR {
		t.Errorf("TestUnquote3 returned %s, want %s", r, expR)
	}
}

func TestParseQuotes(t *testing.T) {
	cmdText := `  Add v1='aaa\'bbb' v2="ccc\"ddd"`
	fmt.Println(cmdText)

	cmd, err := Parse(cmdText, true)

	if err != nil {
		t.Fatal("Error parsing command", err)
	}

	// visualize command
	log.Printf("%s", cmd)

	if cmd.Name != "Add" {
		t.Errorf("command name is %s, want %s", cmd.Name, "Add")
	}

	v1 := "aaa'bbb"
	if cmd.Attrs["v1"] != v1 {
		t.Errorf("command v1 attribute is %s, want %s", cmd.Attrs["v1"], v1)
	}
	v2 := "ccc\"ddd"
	if cmd.Attrs["v2"] != v2 {
		t.Errorf("command v2 attribute is %s, want %s", cmd.Attrs["v2"], v2)
	}
}

func TestParseQuotes2(t *testing.T) {
	cmdText := `add text id='txt1' value="Hello, \"world!\"" v`
	fmt.Println(cmdText)

	cmd, err := Parse(cmdText, true)

	if err != nil {
		t.Fatal("Error parsing command", err)
	}

	fmt.Println("TestParseQuotes2 results:", cmd.Attrs["value"])
}

func TestParse1(t *testing.T) {
	cmd, err := Parse(`  Add value:1 c=3.1 TextField Text=aaa value="Hello,\n 'wor\"ld!" aaa='bbb' cmd2=1`, true)

	if err != nil {
		t.Fatal("Error parsing command", err)
	}

	// visualize command
	log.Printf("%s", cmd)

	if cmd.Name != "Add" {
		t.Errorf("command name is %s, want %s", cmd.Name, "Add")
	}

	if cmd.Indent != 2 {
		t.Errorf("command indent is %d, want %d", cmd.Indent, 2)
	}
}

func TestParse2(t *testing.T) {
	cmd, err := Parse(`set body:form:fullName value='John Smith' another_prop=value`, true)

	if err != nil {
		t.Fatal(err)
	}

	// visualize command
	log.Printf("%s", cmd)

	if len(cmd.Values) != 1 {
		t.Errorf("the number of values is %d, want %d", len(cmd.Values), 1)
	}

	expValue := "body:form:fullName"
	if cmd.Values[0] != expValue {
		t.Errorf("command values[0] is %s, want %s", cmd.Values[0], expValue)
	}

	if cmd.Indent != 0 {
		t.Errorf("command indent is %d, want %d", cmd.Indent, 0)
	}
}

func TestParseSingleCommand(t *testing.T) {
	cmd, err := Parse(`set`, true)

	if err != nil {
		t.Fatal(err)
	}

	// visualize command
	log.Printf("%s", cmd)

	if cmd.Name != "set" {
		t.Errorf("command name is %s, want %s", cmd.Name, "set")
	}

	if len(cmd.Values) != 0 {
		t.Errorf("the number of values is %d, want %d", len(cmd.Values), 0)
	}
}

func TestParseClean(t *testing.T) {
	cmd, err := Parse(`clean page`, true)

	if err != nil {
		t.Fatal(err)
	}

	// visualize command
	log.Printf("%s", cmd)

	if len(cmd.Values) != 1 {
		t.Errorf("the number of values is %d, want %d", len(cmd.Values), 1)
	}

	expValue := "page"
	if cmd.Values[0] != expValue {
		t.Errorf("command values[0] is %s, want %s", cmd.Values[0], expValue)
	}
}

func TestParseSlashesAndNewLine(t *testing.T) {
	cmd, err := Parse(`  Add value="C:\\Program Files\\Node\\node.exe" aaa='bbb' cmd2=1`, true)

	if err != nil {
		t.Fatal("Error parsing command", err)
	}

	// visualize command
	log.Printf("%s", cmd)

	if cmd.Name != "Add" {
		t.Errorf("command name is %s, want %s", cmd.Name, "Add")
	}

	expAttr := "C:\\Program Files\\Node\\node.exe"
	if cmd.Attrs["value"] != expAttr {
		t.Errorf("command value attribute is %s, want %s", cmd.Attrs["value"], expAttr)
	}
}

func TestParseMultilineCommand(t *testing.T) {
	cmd, err := Parse(`

	  add to=footer
	    stack
	      text value="Hello, world!"
	    stack
		  textbox id=txt1
		  button id=ok`, true)

	if err != nil {
		t.Fatal(err)
	}

	// visualize command
	log.Printf("%s", cmd)

	expName := "add"
	if cmd.Name != expName {
		t.Errorf("command name is %s, want %s", cmd.Name, expName)
	}

	if len(cmd.Values) != 0 {
		t.Errorf("the number of values is %d, want %d", len(cmd.Values), 0)
	}

	if len(cmd.Lines) != 5 {
		t.Errorf("the number of lines is %d, want %d", len(cmd.Lines), 5)
	}

	if cmd.Indent != 6 {
		t.Errorf("command indent is %d, want %d", cmd.Indent, 6)
	}
}
