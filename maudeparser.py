# Copyright 2016 Andrew Lawrence
import pyparsing as pp
import ast as ast
from functools import partial

# Label identifier. Simple identifier
labelid = pp.Word(pp.alphanums)

# Natural numbers
nat = pp.Word(pp.nums).addParseAction(lambda x: int(x[0]))

# Token
token = pp.Word(pp.alphanums + '!"#$%&*+,-./:;<=>?@^_`{|}~').setName("token").addParseAction(lambda x: ast.Token(x.asList()[0]))

# Token string definition
# What about the empty token string?
tokenstring = pp.Forward()
tokenstring << pp.Group((token | pp.Group(pp.Literal("(").suppress() + tokenstring + pp.Literal(")").suppress())) + pp.ZeroOrMore(tokenstring)).setName("tokenstring").addParseAction(lambda x: ast.TokenString(x[0]))

# Term definition
term = pp.Forward()
term << pp.Group((token | pp.Group(pp.Literal("(").suppress() + term + pp.Literal(")").suppress())) + pp.ZeroOrMore(term)).setName("term").addParseAction(lambda x: x.asList()[0])

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
windowsfilename = pp.Word(pp.alphanums) + "." + pp.Word(pp.alphanums, max=3)
linuxfilename = pp.Word(pp.alphanums)
filename = pp.Word(pp.alphanums)

# path. OS dependent.
path = pp.Word(pp.alphanums + "./")

# LS flags. OS dependent.
lsflags = pp.Word(pp.alphanums)

# Auxilary Bracket Lists
bracketnatlist = pp.Literal("(").suppress() + pp.OneOrMore(nat) + pp.Literal(")").suppress()
brackettokenlist = pp.Literal("(").suppress() + pp.OneOrMore(token) + pp.Literal(")").suppress()
bracketgatherlist = pp.Literal("(").suppress() + pp.OneOrMore(pp.Literal("e") | pp.Literal("E") | pp.Literal("&")) + pp.Literal(")").suppress()
brackettokenstring = pp.Literal("(").suppress() + tokenstring + pp.Literal(")").suppress()

tokenbrackettokenstring = pp.Optional(token, [""]) + brackettokenstring

# Hook.
# In the Maude Grammar it says that only an id-hook has a following token.
# This seems to be wrong as there are examples of all hooks having following tokens.
# There also seems to be detail missing
hook = pp.Group(pp.Literal("id-hook").suppress() + pp.Optional(token) + brackettokenstring).addParseAction(lambda x: ast.IDHook(x[0] , x[0]))

#| \
#       pp.Group(pp.Literal("op-hook").suppress() + pp.Optional(term) + brackettokenstring).addParseAction(lambda x: ast.OPHook(x.asList())) | \
#       pp.Group(pp.Literal("term-hook").suppress() + brackettokenstring).addParseAction(lambda x: ast.TermHook(x.asList()))

brackethooklist = pp.Literal("(").suppress() + pp.OneOrMore(hook) + pp.Literal(")").suppress()

# Print Item.
printitem = stringid | varid | varandsortid

# Statement Attribute
statementattr = "[" + pp.OneOrMore(pp.Literal("nonexec") |
                                   pp.Literal("otherwise") |
                                   pp.Literal("variant") |
                                   pp.Group(pp.Literal("metadata") + stringid) |
                                   pp.Group(pp.Literal("label") + labelid) |
                                   pp.Group(pp.Literal("print") + pp.ZeroOrMore(printitem))) + "]"

def idparseaction(direction, term):
    if direction == "left":
        return ast.LeftID(term)
    elif direction == "right":
        return ast.RightID(term)
    else:
        raise pp.ParseException("invalid direction in ID attribute")

# Attributes
assocattr = pp.Literal("assoc").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.assoc))
commattr = pp.Literal("comm").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.comm))
idattr = pp.Group(pp.Optional(pp.Literal("left") | pp.Literal("right")) + pp.Literal("id:").suppress()
                  + term).addParseAction(lambda x: idparseaction(x[0][0], x.asList()[0][1]))
idemattr = pp.Literal("idem").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.idem))
iterattr = pp.Literal("iter").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.iter))
memoattr = pp.Literal("memo").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.memo))
dittoattr = pp.Literal("ditto").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.ditto))
configattr = pp.Literal("config").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.config))
objattr = pp.Literal("obj").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.obj))
msgattr = pp.Literal("msg").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.msg))
metadataattr = pp.Group(pp.Literal("metadata").suppress() + stringid).addParseAction(lambda x: ast.MetaData(x[0][0]))
stratattr = pp.Group(pp.Literal("strat").suppress() + bracketnatlist).addParseAction(lambda x: ast.Strat(x.asList()[0]))
polyattr = pp.Group(pp.Literal("poly").suppress() + bracketnatlist).addParseAction(lambda x: ast.Poly(x.asList()[0]))
frozenattr = pp.Group(pp.Literal("frozen").suppress() + pp.Optional(bracketnatlist)).addParseAction(lambda x: ast.Frozen(x.asList()[0]))
precattr = pp.Group(pp.Literal("prec").suppress() + nat).addParseAction(lambda x: ast.Prec(x.asList()[0]))
gatherattr = pp.Group(pp.Literal("gather").suppress() + bracketgatherlist).addParseAction(lambda x: ast.Gather(x[0][0]))
formatattr = pp.Group(pp.Literal("format").suppress() + brackettokenlist).addParseAction(lambda x: ast.Format(x[0][0]))
specialattr = pp.Group(pp.Literal("special").suppress() + brackethooklist).addParseAction(lambda x: ast.Special(x[0][0]))

attr = pp.Literal("[").suppress() + pp.OneOrMore( assocattr | commattr | idattr | idemattr | iterattr | memoattr
                                                | dittoattr | configattr | objattr | msgattr | metadataattr | stratattr
                                                | polyattr | frozenattr | precattr | gatherattr | formatattr
                                                | specialattr) + pp.Literal("]").suppress()

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
statement = pp.Literal("mb") + pp.Optional(label) + term + ":" + sort | \
            pp.Literal("cmb") + pp.Optional(label) + term + ":" + sort + "if" + condition | \
            pp.Literal("eq") + pp.Optional(label) + term + "=" + term | \
            pp.Literal("ceq") + pp.Optional(label) + term + "=" + term + "if" + condition

statementprime = pp.Literal("rl") + pp.Optional(label) + term + "=>" + term | \
                 pp.Literal("crl") + pp.Optional(label) + term + "=>" + term + "if" + condition

# Mod elt
modelt = pp.Forward()
modeltprime = modelt | statementprime + pp.Optional(statementattr) + "."

# Kind
kind = "[" + sort + pp.ZeroOrMore("," + sort) + "]"

# Type
maudetype = sort | kind

# Arrow
arrow = pp.Literal("->") | pp.Literal("~>")

# To part renaming item
topartrenamingitem = "to" + opform + pp.Optional(attr)

# Renaming Item
renamingitem = pp.Literal("sort") + sort + pp.Literal("to") + sort | \
               pp.Literal("label") + labelid + pp.Literal("to") + labelid | \
               pp.Literal("op") + opform + topartrenamingitem | \
               pp.Literal("op") + opform + ":" + pp.ZeroOrMore(maudetype) + arrow + maudetype + topartrenamingitem
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
viewelt = "var" + pp.OneOrMore(varid) + ":" + maudetype + "." | \
          "sort" + sort + "to" + sort + "." | \
          "label" + labelid + "to" + labelid + "." | \
          "op" + opform + "to" + opform + "." | \
          "op" + opform + ":" + pp.ZeroOrMore(maudetype) + arrow + maudetype + "to" + opform + "." | \
          "op" + term + "to" + term + "."

# Mod Elt
modelt = "including" + modexp + "." | \
         "extending" + modexp + "." | \
         "protecting" + modexp + "." | \
         "sorts" + pp.OneOrMore(sort) + "." | \
         "subsorts" + pp.OneOrMore(sort) + pp.OneOrMore("<" + pp.OneOrMore(sort)) + "." | \
         "op" + opform + ":" + pp.ZeroOrMore(maudetype) + arrow + maudetype + pp.Optional(attr) + "." | \
         "ops" + pp.OneOrMore(opid | pp.Literal("(") + opform + pp.Literal(")")) + ":" \
         + pp.ZeroOrMore(maudetype) + arrow + maudetype + pp.Optional(attr) + "." | \
         "vars" + pp.OneOrMore(varid) + ":" + maudetype + "." | \
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
traceoption = pp.Literal("condition") | pp.Literal("whole") | pp.Literal("substitution") | \
              pp.Literal("select") | pp.Literal("mbs") | pp.Literal("eqs") | \
              pp.Literal("rls") | pp.Literal("rewrite") | pp.Literal("body")

# Print option
printoption = pp.Literal("mixfix") | pp.Literal("flat") | pp.Literal("with parentheses") | \
              pp.Literal("with aliases") | pp.Literal("conceal") | pp.Literal("number") | pp.Literal("rat") | \
              pp.Literal("color") | pp.Literal("format") | pp.Literal("graph") | \
              pp.Literal("attribute") | pp.Literal("attribute newline")

# Show option
showoption = pp.Literal("advise") | pp.Literal("stats") | pp.Literal("loop stats") | \
             pp.Literal("timing") | pp.Literal("loop timing") | pp.Literal("breakdown") | \
             pp.Literal("command") | pp.Literal("gc")

# Set option
setoption = pp.Literal("show") + showoption | \
            pp.Literal("print") + printoption | \
            pp.Literal("trace") + traceoption | \
            pp.Literal("break") | pp.Literal("verbose") | pp.Literal("profile") | \
            pp.Literal("clear") + (pp.Literal("memo") | pp.Literal("rules") | pp.Literal("profile")) | \
            pp.Literal("protect") + modid | \
            pp.Literal("extend") + modid | \
            pp.Literal("include") + modid

# Show item
showitem = pp.Literal("module") | pp.Literal("all") | pp.Literal("sorts") | \
           pp.Literal("ops") | pp.Literal("vars") | pp.Literal("mbs") | pp.Literal("eqs") | \
           pp.Literal("rls") | pp.Literal("summary") | pp.Literal("kinds") | pp.Literal("profile")

# Unification Equation
unificationequation = term + "=?" + term

# Search type
searchtype = pp.Literal("=>!") | pp.Literal("=>+") | pp.Literal("=>*") | pp.Literal("=>1")

# Command
inmodid = pp.Optional("in" + modid + ":")
suchthatcondition = pp.Optional("such that" + condition)
optionaldebug = pp.Optional("debug")
optionalnat = pp.Optional("[" + nat + "]")
fullstop = pp.Literal(".")
show = pp.Literal("show")
opidformlist = pp.OneOrMore(opid | ("(" + opform + ")"))
command = pp.Literal("select") + modid + fullstop | \
          pp.Literal("parse") + inmodid + term + fullstop | \
          optionaldebug + pp.Literal("reduce") + inmodid + term + fullstop | \
          optionaldebug + pp.Literal("rewrite") + optionalnat + inmodid + term + fullstop | \
          optionaldebug + pp.Literal("frewrite") + pp.Optional(
              "[" + nat + pp.Optional("," + nat) + "]") + inmodid + term + fullstop | \
          optionaldebug + pp.Literal("erewrite") + pp.Optional(
              "[" + nat + pp.Optional("," + nat) + "]") + inmodid + term + fullstop | \
          (pp.Literal("match") | pp.Literal(
              "xmatch")) + optionalnat + inmodid + term + "<=?" + term + suchthatcondition + fullstop | \
          "unify" + optionalnat + inmodid + unificationequation + pp.ZeroOrMore(
              "/\\" + unificationequation) + fullstop | \
          optionaldebug + "variant unify" + optionalnat + inmodid + unificationequation + pp.ZeroOrMore(
              "/\\" + unificationequation) + fullstop | \
          optionaldebug + "get variants" + optionalnat + inmodid + term + fullstop | \
          "search" + optionalnat + inmodid + term + searchtype + term + suchthatcondition + fullstop | \
          optionaldebug + "continue" + nat + fullstop | \
          "loop" + inmodid + term + fullstop | \
          "(" + tokenstring + ")" | \
          "trace" + (pp.Literal("select") | pp.Literal("deselect") | pp.Literal("include") | pp.Literal(
              "exclude")) + opidformlist + fullstop | \
          "print" + (pp.Literal("conceal") | pp.Literal("reveal")) + opidformlist + fullstop | \
          "break" + (pp.Literal("select") | pp.Literal("deselect")) + opidformlist + fullstop | \
          show + showitem + pp.Optional(modid) + fullstop | \
          show + "view" + pp.Optional(viewid) + fullstop | \
          show + "modules" + fullstop | \
          show + "views" + fullstop | \
          show + "search" + "graph" + fullstop | \
          pp.Literal("show") + pp.Literal("path") + pp.Optional("labels") + nat + fullstop | \
          pp.Literal("do") + pp.Literal("clear") + pp.Literal("memo") + fullstop | \
          pp.Literal("set") + setoption + (pp.Literal("on") | pp.Literal("off")) + fullstop

space = pp.Literal(" ").leaveWhitespace().suppress()

# System command
systemcommand = pp.Group(pp.Literal("in").suppress() + space + filename).addParseAction(
    lambda x: ast.InCommand(x[0][0])) | \
                pp.Group(pp.Literal("load").suppress() + space + filename).addParseAction(
                    lambda x: ast.LoadCommand(x[0][0])) | \
                pp.Literal("quit").suppress().addParseAction(ast.QuitCommand) | \
                pp.Literal("eof").suppress().addParseAction(ast.EofCommand) | \
                pp.Literal("popd").suppress().addParseAction(ast.PopDCommand) | \
                pp.Literal("pwd").suppress().addParseAction(ast.PwdCommand) | \
                pp.Group(pp.Literal("cd").suppress() +
                         space + path).addParseAction(lambda x: ast.CdCommand(x[0][0])) | \
                pp.Group(pp.Literal("push").suppress() + space + path).addParseAction(
                    lambda x: ast.PushCommand(x[0][0])) | \
                pp.Group(pp.Literal("ls").suppress() + pp.Optional(space + lsflags, default="") +
                         pp.Optional(space + path, default="")).addParseAction(lambda x: ast.LsCommand(x[0][0],
                                                                                                       x[0][1]))

# Maude top
maudetop = pp.OneOrMore(systemcommand | command | debuggercommand | module | theory | view)

