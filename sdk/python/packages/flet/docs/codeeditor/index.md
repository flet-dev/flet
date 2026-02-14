---
class_name: flet_code_editor.CodeEditor
examples: ../../examples/controls/code_editor
---

# CodeEditor

Edit and highlight source code inside your [Flet](https://flet.dev) app using the `flet-code-editor` extension, which wraps Flutter's [`flutter_code_editor`](https://pub.dev/packages/flutter_code_editor) package.

## Usage

Add `flet-code-editor` to your project dependencies:

/// tab | uv
```bash
uv add flet-code-editor
```

///
/// tab | pip
```bash
pip install flet-code-editor  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Description

{{ class_all_options(class_name) }}

## Supported languages

`CodeEditor.language` supports these values (from `highlight`):

<details>
<summary>Show supported languages (189)</summary>

`1c`, `abnf`, `accesslog`, `actionscript`, `ada`, `angelscript`, `apache`, `applescript`, `arcade`, `arduino`, `armasm`, `asciidoc`, `aspectj`, `autohotkey`, `autoit`, `avrasm`, `awk`, `axapta`, `bash`, `basic`, `bnf`, `brainfuck`, `cal`, `capnproto`, `ceylon`, `clean`, `clojure`, `clojure-repl`, `cmake`, `coffeescript`, `coq`, `cos`, `cpp`, `crmsh`, `crystal`, `cs`, `csp`, `css`, `d`, `dart`, `delphi`, `diff`, `django`, `dns`, `dockerfile`, `dos`, `dsconfig`, `dts`, `dust`, `ebnf`, `elixir`, `elm`, `erb`, `erlang`, `erlang-repl`, `excel`, `fix`, `flix`, `fortran`, `fsharp`, `gams`, `gauss`, `gcode`, `gherkin`, `glsl`, `gml`, `gn`, `go`, `golo`, `gradle`, `graphql`, `groovy`, `haml`, `handlebars`, `haskell`, `haxe`, `hsp`, `htmlbars`, `http`, `hy`, `inform7`, `ini`, `irpf90`, `isbl`, `java`, `javascript`, `jboss-cli`, `json`, `julia`, `julia-repl`, `kotlin`, `lasso`, `ldif`, `leaf`, `less`, `lisp`, `livecodeserver`, `livescript`, `llvm`, `lsl`, `lua`, `makefile`, `markdown`, `mathematica`, `matlab`, `maxima`, `mel`, `mercury`, `mipsasm`, `mizar`, `mojolicious`, `monkey`, `moonscript`, `n1ql`, `nginx`, `nimrod`, `nix`, `nsis`, `objectivec`, `ocaml`, `openscad`, `oxygene`, `parser3`, `perl`, `pf`, `pgsql`, `php`, `plaintext`, `pony`, `powershell`, `processing`, `profile`, `prolog`, `properties`, `protobuf`, `puppet`, `purebasic`, `python`, `q`, `qml`, `r`, `reasonml`, `rib`, `roboconf`, `routeros`, `rsl`, `ruby`, `ruleslanguage`, `rust`, `sas`, `scala`, `scheme`, `scilab`, `scss`, `shell`, `smali`, `smalltalk`, `sml`, `solidity`, `sqf`, `sql`, `stan`, `stata`, `step21`, `stylus`, `subunit`, `swift`, `taggerscript`, `tap`, `tcl`, `tex`, `thrift`, `tp`, `twig`, `typescript`, `vala`, `vbnet`, `vbscript`, `vbscript-html`, `verilog`, `vhdl`, `vim`, `vue`, `x86asm`, `xl`, `xml`, `xquery`, `yaml`, `zephir`.

</details>

## Supported named themes

`CodeEditor.code_theme` accepts either a `CodeTheme` object or one of these string theme names (from `flutter_highlight`):

<details>
<summary>Show supported named themes (90)</summary>

`a11y-dark`, `a11y-light`, `agate`, `an-old-hope`, `androidstudio`, `arduino-light`, `arta`, `ascetic`, `atelier-cave-dark`, `atelier-cave-light`, `atelier-dune-dark`, `atelier-dune-light`, `atelier-estuary-dark`, `atelier-estuary-light`, `atelier-forest-dark`, `atelier-forest-light`, `atelier-heath-dark`, `atelier-heath-light`, `atelier-lakeside-dark`, `atelier-lakeside-light`, `atelier-plateau-dark`, `atelier-plateau-light`, `atelier-savanna-dark`, `atelier-savanna-light`, `atelier-seaside-dark`, `atelier-seaside-light`, `atelier-sulphurpool-dark`, `atelier-sulphurpool-light`, `atom-one-dark`, `atom-one-dark-reasonable`, `atom-one-light`, `brown-paper`, `codepen-embed`, `color-brewer`, `darcula`, `dark`, `default`, `docco`, `dracula`, `far`, `foundation`, `github`, `github-gist`, `gml`, `googlecode`, `gradient-dark`, `grayscale`, `gruvbox-dark`, `gruvbox-light`, `hopscotch`, `hybrid`, `idea`, `ir-black`, `isbl-editor-dark`, `isbl-editor-light`, `kimbie.dark`, `kimbie.light`, `lightfair`, `magula`, `mono-blue`, `monokai`, `monokai-sublime`, `night-owl`, `nord`, `obsidian`, `ocean`, `paraiso-dark`, `paraiso-light`, `pojoaque`, `purebasic`, `qtcreator_dark`, `qtcreator_light`, `railscasts`, `rainbow`, `routeros`, `school-book`, `shades-of-purple`, `solarized-dark`, `solarized-light`, `sunburst`, `tomorrow`, `tomorrow-night`, `tomorrow-night-blue`, `tomorrow-night-bright`, `tomorrow-night-eighties`, `vs`, `vs2015`, `xcode`, `xt256`, `zenburn`.

</details>

See also types:
- [`CodeTheme`](types/codetheme.md)
- [`GutterStyle`](types/gutterstyle.md)
