from dataclasses import dataclass
from enum import Enum
from typing import Optional

import flet as ft
from flet.controls.core.markdown import MarkdownCodeTheme, MarkdownCustomCodeTheme

__all__ = ["CodeLanguage", "CodeTheme", "CustomCodeTheme", "GutterStyle"]


class CodeLanguage(Enum):
    # 1-9
    ONE_C = "1c"
    """
    1C
    """

    # A
    ABNF = "abnf"
    """
    ABNF
    """
    ACCESSLOG = "accesslog"
    """
    Accesslog
    """
    ACTIONSCRIPT = "actionscript"
    """
    ActionScript
    """
    ADA = "ada"
    """
    Ada
    """
    ANGELSCRIPT = "angelscript"
    """
    Angelscript
    """
    APACHE = "apache"
    """
    Apache
    """
    APPLESCRIPT = "applescript"
    """
    AppleScript
    """
    ARCADE = "arcade"
    """
    Arcade
    """
    ARDUINO = "arduino"
    """
    Arduino
    """
    ARMASM = "armasm"
    """
    ARM Assembly
    """
    ASCIIDOC = "asciidoc"
    """
    AsciiDoc
    """
    ASPECTJ = "aspectj"
    """
    Aspectj
    """
    AUTOHOTKEY = "autohotkey"
    """
    AutoHotkey
    """
    AUTOIT = "autoit"
    """
    AutoIt
    """
    AVRASM = "avrasm"
    """
    AVR Assembly
    """
    AWK = "awk"
    """
    Awk
    """
    AXAPTA = "axapta"
    """
    Axapta
    """

    # B
    BASH = "bash"
    """
    Bash
    """
    BASIC = "basic"
    """
    Basic
    """
    BNF = "bnf"
    """
    BNF
    """
    BRAINFUCK = "brainfuck"
    """
    Brainfuck
    """

    # C
    CAL = "cal"
    """
    Cal
    """
    CAPNPROTO = "capnproto"
    """
    Cap'n Proto
    """
    CEYLON = "ceylon"
    """
    Ceylon
    """
    CLEAN = "clean"
    """
    Clean
    """
    CLOJURE = "clojure"
    """
    Clojure
    """
    CLOJURE_REPL = "clojure-repl"
    """
    Clojure REPL
    """
    CMAKE = "cmake"
    """
    CMake
    """
    COFFEESCRIPT = "coffeescript"
    """
    CoffeeScript
    """
    COQ = "coq"
    """
    Coq
    """
    COS = "cos"
    """
    Cos
    """
    CPP = "cpp"
    """
    C++
    """
    CRMSH = "crmsh"
    """
    Crmsh
    """
    CRYSTAL = "crystal"
    """
    Crystal
    """
    CS = "cs"
    """
    C#
    """
    CSP = "csp"
    """
    Csp
    """
    CSS = "css"
    """
    CSS
    """

    # D
    D = "d"
    """
    D
    """
    DART = "dart"
    """
    Dart
    """
    DELPHI = "delphi"
    """
    Delphi
    """
    DIFF = "diff"
    """
    Diff
    """
    DJANGO = "django"
    """
    Django
    """
    DNS = "dns"
    """
    DNS
    """
    DOCKERFILE = "dockerfile"
    """
    Dockerfile
    """
    DOS = "dos"
    """
    DOS
    """
    DSCONFIG = "dsconfig"
    """
    DSConfig
    """
    DTS = "dts"
    """
    DTS
    """
    DUST = "dust"
    """
    Dust
    """

    # E
    EBNF = "ebnf"
    """
    EBNF
    """
    ELIXIR = "elixir"
    """
    Elixir
    """
    ELM = "elm"
    """
    Elm
    """
    ERB = "erb"
    """
    Erb
    """
    ERLANG = "erlang"
    """
    Erlang
    """
    ERLANG_REPL = "erlang-repl"
    """
    Erlang REPL
    """
    EXCEL = "excel"
    """
    Excel
    """

    # F
    FIX = "fix"
    """
    Fix
    """
    FLIX = "flix"
    """
    Flix
    """
    FORTRAN = "fortran"
    """
    Fortran
    """
    FSHARP = "fsharp"
    """
    F#
    """

    # G
    GAMS = "gams"
    """
    Gams
    """
    GAUSS = "gauss"
    """
    Gauss
    """
    GCODE = "gcode"
    """
    G-code
    """
    GHERKIN = "gherkin"
    """
    Gherkin
    """
    GLSL = "glsl"
    """
    GLSL
    """
    GML = "gml"
    """
    GML
    """
    GN = "gn"
    """
    Gn
    """
    GO = "go"
    """
    Go
    """
    GOLO = "golo"
    """
    Golo
    """
    GRADLE = "gradle"
    """
    Gradle
    """
    GRAPHQL = "graphql"
    """
    GraphQL
    """
    GROOVY = "groovy"
    """
    Groovy
    """

    # H
    HAML = "haml"
    """
    Haml
    """
    HANDLEBARS = "handlebars"
    """
    Handlebars
    """
    HASKELL = "haskell"
    """
    Haskell
    """
    HAXE = "haxe"
    """
    Haxe
    """
    HSP = "hsp"
    """
    Hsp
    """
    HTMLBARS = "htmlbars"
    """
    HTMLBars
    """
    HTTP = "http"
    """
    HTTP
    """
    HY = "hy"
    """
    Hy
    """

    # I
    INFORM7 = "inform7"
    """
    INFORM7
    """
    INI = "ini"
    """
    INI
    """
    IRPF90 = "irpf90"
    """
    IRPF90
    """
    ISBL = "isbl"
    """
    ISBL
    """

    # J
    JAVA = "java"
    """
    Java
    """
    JAVASCRIPT = "javascript"
    """
    Javascript
    """
    JBOSS_CLI = "jboss-cli"
    """
    JBoss CLI
    """
    JSON = "json"
    """
    JSON
    """
    JULIA = "julia"
    """
    Julia
    """
    JULIA_REPL = "julia-repl"
    """
    Julia REPL
    """

    # K
    KOTLIN = "kotlin"
    """
    Kotlin
    """

    # L
    LASSO = "lasso"
    """
    Lasso
    """
    LDIF = "ldif"
    """
    LDIF
    """
    LEAF = "leaf"
    """
    Leaf
    """
    LESS = "less"
    """
    Less
    """
    LISP = "lisp"
    """
    Lisp
    """
    LIVECODESERVER = "livecodeserver"
    """
    LiveCode Server
    """
    LIVESCRIPT = "livescript"
    """
    Livescript
    """
    LLVM = "llvm"
    """
    LLVM
    """
    LSL = "lsl"
    """
    LSL
    """
    LUA = "lua"
    """
    Lua
    """

    # M
    MAKEFILE = "makefile"
    """
    Makefile
    """
    MARKDOWN = "markdown"
    """
    Markdown
    """
    MATHEMATICA = "mathematica"
    """
    Mathematica
    """
    MATLAB = "matlab"
    """
    Matlab
    """
    MAXIMA = "maxima"
    """
    Maxima
    """
    MEL = "mel"
    """
    Mel
    """
    MERCURY = "mercury"
    """
    Mercury
    """
    MIPSASM = "mipsasm"
    """
    MIPS Assembly
    """
    MIZAR = "mizar"
    """
    Mizar
    """
    MOJOLICIOUS = "mojolicious"
    """
    Mojolicious
    """
    MONKEY = "monkey"
    """
    Monkey
    """
    MOONSCRIPT = "moonscript"
    """
    MoonScript
    """

    # N
    N1QL = "n1ql"
    """
    N1QL
    """
    NGINX = "nginx"
    """
    Nginx
    """
    NIMROD = "nimrod"
    """
    Nimrod
    """
    NIX = "nix"
    """
    Nix
    """
    NSIS = "nsis"
    """
    NSIS
    """

    # O
    OBJECTIVEC = "objectivec"
    """
    Objective-C
    """
    OCAML = "ocaml"
    """
    OCaml
    """
    OPENSCAD = "openscad"
    """
    OpenSCAD
    """
    OXYGENE = "oxygene"
    """
    Oxygene
    """

    # P
    PARSER3 = "parser3"
    """
    PARSER3
    """
    PERL = "perl"
    """
    Perl
    """
    PF = "pf"
    """
    PF
    """
    PGSQL = "pgsql"
    """
    PostgreSQL
    """
    PHP = "php"
    """
    PHP
    """
    PLAINTEXT = "plaintext"
    """
    Plain text
    """
    PONY = "pony"
    """
    Pony
    """
    POWERSHELL = "powershell"
    """
    PowerShell
    """
    PROCESSING = "processing"
    """
    Processing
    """
    PROFILE = "profile"
    """
    Profile
    """
    PROLOG = "prolog"
    """
    Prolog
    """
    PROPERTIES = "properties"
    """
    Properties
    """
    PROTOBUF = "protobuf"
    """
    Protocol Buffers
    """
    PUPPET = "puppet"
    """
    Puppet
    """
    PUREBASIC = "purebasic"
    """
    PureBasic
    """
    PYTHON = "python"
    """
    Python
    """

    # Q
    Q = "q"
    """
    Q
    """
    QML = "qml"
    """
    QML
    """

    # R
    R = "r"
    """
    R
    """
    REASONML = "reasonml"
    """
    ReasonML
    """
    RIB = "rib"
    """
    Rib
    """
    ROBOCONF = "roboconf"
    """
    Roboconf
    """
    ROUTEROS = "routeros"
    """
    RouterOS
    """
    RSL = "rsl"
    """
    RSL
    """
    RUBY = "ruby"
    """
    Ruby
    """
    RULESLANGUAGE = "ruleslanguage"
    """
    Rules language
    """
    RUST = "rust"
    """
    Rust
    """

    # S
    SAS = "sas"
    """
    SAS
    """
    SCALA = "scala"
    """
    Scala
    """
    SCHEME = "scheme"
    """
    Scheme
    """
    SCILAB = "scilab"
    """
    Scilab
    """
    SCSS = "scss"
    """
    SCSS
    """
    SHELL = "shell"
    """
    Shell
    """
    SMALI = "smali"
    """
    Smali
    """
    SMALLTALK = "smalltalk"
    """
    Smalltalk
    """
    SML = "sml"
    """
    SML
    """
    SOLIDITY = "solidity"
    """
    Solidity
    """
    SQF = "sqf"
    """
    SQF
    """
    SQL = "sql"
    """
    SQL
    """
    STAN = "stan"
    """
    Stan
    """
    STATA = "stata"
    """
    Stata
    """
    STEP21 = "step21"
    """
    STEP21
    """
    STYLUS = "stylus"
    """
    Stylus
    """
    SUBUNIT = "subunit"
    """
    SubUnit
    """
    SWIFT = "swift"
    """
    Swift
    """

    # T
    TAGGERSCRIPT = "taggerscript"
    """
    Tagger Script
    """
    TAP = "tap"
    """
    Tap
    """
    TCL = "tcl"
    """
    Tcl
    """
    TEX = "tex"
    """
    TeX
    """
    THRIFT = "thrift"
    """
    Thrift
    """
    TP = "tp"
    """
    TP
    """
    TWIG = "twig"
    """
    Twig
    """
    TYPESCRIPT = "typescript"
    """
    TypeScript
    """

    # V
    VALA = "vala"
    """
    Vala
    """
    VBNET = "vbnet"
    """
    VB.NET
    """
    VBSCRIPT = "vbscript"
    """
    VBScript
    """
    VBSCRIPT_HTML = "vbscript-html"
    """
    VBScript HTML
    """
    VERILOG = "verilog"
    """
    Verilog
    """
    VHDL = "vhdl"
    """
    VHDL
    """
    VIM = "vim"
    """
    Vim script
    """
    VUE = "vue"
    """
    Vue
    """

    # X
    X86ASM = "x86asm"
    """
    x86 Assembly
    """
    XL = "xl"
    """
    Xl
    """
    XML = "xml"
    """
    XML
    """
    XQUERY = "xquery"
    """
    XQuery
    """

    # Y
    YAML = "yaml"
    """
    YAML
    """

    # Z
    ZEPHIR = "zephir"
    """
    Zephir
    """


CodeTheme = MarkdownCodeTheme
"""Alias for `flet.MarkdownCodeTheme`."""

CustomCodeTheme = MarkdownCustomCodeTheme
"""Alias for `flet.MarkdownCustomCodeTheme`."""


@dataclass
class GutterStyle:
    """Defines gutter appearance (line numbers) for the code editor."""

    text_style: Optional[ft.TextStyle] = None
    """Text style for line numbers."""

    background_color: Optional[ft.ColorValue] = None
    """Background color for the gutter."""

    width: Optional[ft.Number] = None
    """Fixed width of the gutter."""

    margin: Optional[ft.Number] = None
    """Margin outside the gutter."""

    show_errors: bool = True
    """Whether to show errors in the gutter."""

    show_folding_handles: bool = True
    """Whether to show folding handles in the gutter."""

    show_line_numbers: bool = True
    """Whether to show line numbers in the gutter."""
