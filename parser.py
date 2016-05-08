# Copyright 2016 Andrew Lawrence
import pyparsing as pp
import ast as ast


# Label identifier. Simple identifier
labelid = pp.Word(pp.alphanums)

# Natural numbers
nat = pp.Word(pp.nums)

# Token
token = pp.Word('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&*+,-./:;<=>?@[\\]^_`{|}~')

# Token string definition
tokenstring = pp.Forward()
tokenstring << (token | pp.Group("(" + tokenstring + ")")) + pp.ZeroOrMore(tokenstring)

# Term definition
term = pp.Forward()
termbody = token | pp.Group("(" + term + ")")
term << termbody + termbody + pp.ZeroOrMore(termbody)

# Operation identifier. Simple identifier with possible underscores.
opid = pp.Word(pp.alphanums + "_")

# Operation formula
opform = pp.Forward()
opformbody = opid | pp.Group("(" + opform + ")")
opform << opformbody + opformbody + pp.ZeroOrMore(opformbody)

# Variable and Sort ID. An identifier consisting of a variable name
# followed by a colon followed by a sort name
varandsortid = pp.Word(pp.alphanums) + ":" + pp.Word(pp.alphanums)

# Variable ID. Simple identifier. Capitalised.
varid = pp.Word(pp.srange("[A-Z]"), pp.alphanums)

# Sort ID.
sortid = pp.Word(pp.srange("[A-Z]"), pp.alphanums)

# Parameter ID.
parameterid = pp.Word(pp.srange("[A-Z]"), exact=1)

# View ID
viewid = pp.Word(pp.srange("[A-Z]"), pp.alphanums)

# Module ID
modid = pp.Word(pp.srange("[A-Z0-9]"))

# String ID
stringid = pp.dblQuotedString

# File name. OS dependent
windowsfilename = pp.Word(pp.alphanums) + "." + pp.Word(pp.alphanums,max=3)
linuxfilename = pp.Word(pp.alphanums)
filename = windowsfilename | linuxfilename

# directory. OS dependent.
directory = pp.Word(pp.alphanums)

# LS flags. OS dependent.
lsflags = pp.Word(pp.alphanums)

# Hook.
hook = ("id-hook" + token + pp.Optional(pp.Group("(" + tokenstring + ")"))) | \
       ((pp.Literal("op-hook") | pp.Literal("term-hook")) + pp.Group("(" + tokenstring + ")"))

# Print Item.
printitem = stringid | varid | varandsortid

# Statement Attribute
statementattr = "[" + pp.OneOrMore(pp.Literal("nonexec") |
                                   pp.Literal("otherwise") |
                                   pp.Literal("variant") |
                                   pp.Group(pp.Literal("metadata") + stringid) |
                                   pp.Group(pp.Literal("label") + labelid) |
                                   pp.Group(pp.Literal("print") + pp.ZeroOrMore(printitem))) + "]"

# Attribute
attr = "[" + pp.OneOrMore(pp.Literal("assoc") |
                               pp.Literal("comm") |
                               pp.Group(pp.Optional(pp.Literal("left") | pp.Literal("right")) + "id:" + term )|
                               pp.Literal("idem") |
                               pp.Literal("iter") |
                               pp.Literal("memo") |
                               pp.Literal("ditto") |
                               pp.Literal("config") |
                               pp.Literal("obj") |
                               pp.Literal("msg") |
                               pp.Group(pp.Literal("metadata") + stringid) |
                               pp.Group(pp.Literal("strat") + "(" + pp.OneOrMore(nat) + ")") |
                               pp.Group(pp.Literal("poly")  + "(" + pp.OneOrMore(nat) + ")") |
                               pp.Literal("frozen") + pp.Optional("(" + pp.OneOrMore(nat) + ")") |
                               pp.Literal("prec") + nat |
                               pp.Literal("gather") + "(" +
                                    (pp.OneOrMore(pp.Literal("e") | pp.Literal("E") | pp.Literal("&"))) + ")" |
                               pp.Literal("format") + "(" + pp.OneOrMore(token) + ")" |
                               pp.Literal("special") + "(" + pp.OneOrMore(hook) + ")") + "]"

# Sort
sort = pp.Forward()
sort << sortid | sort + "{" + sort + pp.ZeroOrMore("," + sort) + "}"

# Condition fragment
conditionfragment = pp.Forward()
conditionfragmentprime = conditionfragment | term + "=>" + term
conditionfragment << term + "=" + term | \
                     term + ":=" + term | \
                     term + ":" + sort

# Condition
condition = conditionfragment + pp.ZeroOrMore("/\\" + conditionfragment)
conditionprime = conditionfragmentprime + pp.ZeroOrMore("/\\" + conditionfragmentprime)

# Label
label = "[" + labelid + "]" + ":"

# Statement
statement = "mb" + pp.Optional(label) + term + ":" + sort | \
            pp.Literal("cmb") + pp.Optional(label) + term + ":" + sort + "if" + condition | \
            pp.Literal("eq") + pp.Optional(label) + term + "=" + term | \
            pp.Literal("ceq") + pp.Optional(label) + term + "=" + term + "if" + condition

statementprime = "rl" + pp.Optional(label) + term + "=>" + term | \
                 pp.Literal("crl") + pp.Optional(label) + term + "=>" + term + "if" + condition

# Mod elt
modelt = pp.Forward()
modeltprime = modelt | statementprime + pp.Optional(statementattr) + "."

# Kind
kind = "[" + sort + pp.ZeroOrMore("," + sort) + "]"

# Type
type = sort | kind

# Arrow
arrow = pp.Literal("->") | pp.Literal("~>")

# To part renaming item
topartrenamingitem = "to" + opform + pp.Optional(attr)

# Renaming Item
renamingitem = "sort" + sort + "to" + sort | \
                "label" + labelid + "to" + labelid | \
                "op" + opform + topartrenamingitem | \
                "op" + opform + ":" + pp.ZeroOrMore(type) + arrow + type + topartrenamingitem
# Renaming
renaming = "(" + renamingitem + pp.ZeroOrMore("," + renamingitem) + ")"

# Mod Exp
modexp = pp.Forward()
modexp << modid | \
         "(" + modexp + ")" | \
         modexp + "+" + modexp | \
         modexp + "*" + renaming | \
         modexp + "{" + viewid + pp.ZeroOrMore("," + viewid) + "}"

# View Elt
viewelt = "var" + pp.OneOrMore(varid) + ":" + type + "." | \
          "sort" + sort + "to" + sort + "." | \
          "label" + labelid + "to" + labelid + "." | \
          "op" + opform + "to" + opform + "." | \
          "op" + opform + ":" + pp.ZeroOrMore(type) + arrow + type + "to" + opform + "." | \
          "op" + term + "to" + term + "."

# Mod Elt
modelt = "including" + modexp + "." | \
         "extending" + modexp + "." | \
         "protecting" + modexp + "." | \
         "sorts" + pp.OneOrMore(sort) + "." | \
         "subsorts" + pp.OneOrMore(sort) + pp.OneOrMore("<" + pp.OneOrMore(sort)) + "." | \
         "op" + opform + ":" + pp.ZeroOrMore(type) + arrow + type + pp.Optional(attr)  + "." | \
         "ops" + pp.OneOrMore( opid | pp.Literal("(") + opform + pp.Literal(")")) + ":" \
                + pp.ZeroOrMore(type) + arrow + type + pp.Optional(attr) + "." | \
         "vars" + pp.OneOrMore(varid) + ":" + type + "." | \
         statement + pp.Optional(statementattr) + "."

# ParameterDecl
parameterdecl = parameterid + "::" + modexp

# Parameter List
parameterlist = "{" + parameterdecl + pp.ZeroOrMore("," + parameterdecl) + "}"

# View
view = "view" + viewid + "from" + modexp + "to" + modexp + "is" + pp.ZeroOrMore(viewelt) + "endv"

# Theory
theory = "fth" + modid + "is" + pp.ZeroOrMore(modelt) + "endfth" | \
         "th" + modid + "is" + pp.ZeroOrMore(modeltprime) + "endth"

# Module
module = "fmod" + modid + pp.Optional(parameterlist) + "is" + pp.ZeroOrMore(modelt) + "endfm" | \
         "mod" + modid + pp.Optional(parameterlist) + "is" + pp.ZeroOrMore(modeltprime) + "endfm"

# Debugger command
debuggercommand = pp.Literal("resume .") | pp.Literal("abort .") | pp.Literal("step .") | pp.Literal("where .")

# Trace option
traceoption = pp.Literal("condition") | pp.Literal("whole") | pp.Literal("substitution") |\
              pp.Literal("select") | pp.Literal("mbs") | pp.Literal("eqs") | \
              pp.Literal("rls") | pp.Literal("rewrite") | pp.Literal("body")

# Print option
printoption = "mixfix" | "flat" | "with parentheses" | "with aliases" | "conceal" | "number" | "rat" | "color" | \
              "format" | "graph" | "attribute" | "attribute newline"

# Show option
showoption = "advise" | "stats" | "loop stats" | "timing" | "loop timing" | "breakdown" | "command" | "gc"

# Set option
setoption = "show" + showoption | \
            "print" + printoption | \
            "trace" + traceoption | \
            "break" | "verbose" | "profile" | \
            "clear" + ("memo" | "rules" | "profile") | \
            "protect" + modid | \
            "extend" + modid | \
            "include" + modid

# Show item
showitem = "module" | "all" | "sorts" | "ops" | "vars" | "mbs" | "eqs" | "rls" | "summary" | "kinds" | "profile"

# Unification Equation
unificationequation = term + "=?" + term

# Search type
searchtype = "=>!" | "=>+" | "=>*" | "=>1"

# Command
inmodid = pp.Optional("in" + modid + ":")
suchthatcondition = pp.Optional("such that" + condition)
optionaldebug = pp.Optional("debug")
optionalnat = pp.Optional("[" + nat + "]")
opidformlist = pp.OneOrMore(opid | ("(" + opform + ")"))
command = "select" + modid + "." | \
          "parse" + inmodid + term + "." | \
          optionaldebug + "reduce" + inmodid + term + "." | \
          optionaldebug + "rewrite" + optionalnat + inmodid + term + "." |\
          optionaldebug + "frewrite " + pp.Optional("[" + nat + pp.Optional("," + nat) + "]") + inmodid + term + "." | \
          optionaldebug + "erewrite " + pp.Optional("[" + nat + pp.Optional("," + nat) + "]") + inmodid + term + "." | \
          ("match" | "xmatch") + optionalnat + inmodid + term + "<=?" + term + suchthatcondition + "." | \
          "unify" + optionalnat + inmodid + unificationequation + pp.ZeroOrMore("/\\" + unificationequation) + "." | \
          optionaldebug + "variant unify" + optionalnat + inmodid + unificationequation + pp.ZeroOrMore("/\\" + unificationequation) + "." | \
          optionaldebug + "get variants" + optionalnat + inmodid + term + "." | \
          "search" + optionalnat + inmodid + term + searchtype + term + suchthatcondition + "." | \
          optionaldebug + "continue" + nat + "." | \
          "loop" + inmodid + term + "." | \
          "(" + tokenstring + ")" | \
          "trace" + ("select" | "deselect" | "include" | "exclude") + opidformlist + "." | \
          "print" + ("conceal" | "reveal") + opidformlist + "." | \
          "break" + ("select" | "deselect") + opidformlist + "." | \
          "show" + showitem + pp.Optional(modid) + "." | \
          "show" + "view" + pp.Optional(viewid) + "." | \
          "show" + "modules" + "." | \
          "show" + "views" + "." | \
          "show" + "search" + "graph" + "." | \
          "show" + "path" + pp.Optional("labels") + nat + "." | \
          "do" + "clear" + "memo" + "." | \
          "set" + setoption + ("on" | "off") + "."

# System command
systemcommand = pp.Group("in" + filename).addParseAction(lambda x: ast.InCommand(x[1])) | \
                pp.Group("load" + filename).addParseAction(lambda x: ast.LoadCommand(x[1])) | \
                pp.Literal("quit").addParseAction(ast.QuitCommand) | \
                pp.Literal("eof").addParseAction(ast.EofCommand) | \
                pp.Literal("popd").addParseAction(ast.PopDCommand) | \
                pp.Literal("pwd").addParseAction(ast.PwdCommand) | \
                pp.Group("cd" + directory).addParseAction(lambda x: ast.CdCommand(x[1])) |\
                pp.Group("push" + directory).addParseAction(lambda x: ast.PushCommand(x[1])) | \
                pp.Group("ls" + pp.Optional(lsflags) + pp.Optional(directory)).addParseAction(lambda x: ast.LsCommand(x[1], x[2]))

# Maude top
maudetop = pp.OneOrMore(systemcommand | command | debuggercommand | module | theory | view)


test = "load meh.txt"
print (test, "->", systemcommand.parseString(test))