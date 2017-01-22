# Copyright 2016 Andrew Lawrence
import pyparsing as pp
import ast as ast
from functools import partial

# Label identifier. Simple identifier
labelid = pp.Word(pp.alphanums)

# Natural numbers
nat = pp.Word(pp.nums).addParseAction(lambda x: int(x[0]))

# Token
# TODO I removed the eq symbol from tokens. Should it be allowed?
token = pp.Word(pp.alphanums + '!"#$%&*+,-./;<>?@^_`{|}~').setResultsName("token").addParseAction(lambda x: ast.Token(x.asList()[0]))

# Special Symbols
LPAREN,RPAREN,LCBRACK,RCBRACK,LSBRACK,RSBRACK,COMMA,FULLSTOP,EQUAL, = map(pp.Suppress, "(){}[],.=")
COLON,LESSTHAN = map(pp.Suppress, ":<")

# Key words
IF,OP,OPS,TO,IS,SHOW,IN,AND = map(pp.Suppress, map(pp.Literal, ["if", "op", "ops", "to", "is", "show", "in", "/\\"]))
RIGHTARROW,ASSIGN = map(pp.Suppress, map(pp.Literal, ["=>", ":="]))
FMOD,MOD,ENDFM = map(pp.Suppress, map(pp.Literal, ["fmod", "mod", "endfm"]))
VAR,VARS,SORT,SORTS,SUBSORTS,LABEL = map(pp.Suppress, map(pp.Literal, ["var", "vars", "sort", "sorts", "subsorts", "label"]))
INCLUDING,EXTENDING,PROTECTING = map(pp.Suppress, map(pp.Literal, ["including", "extending", "protecting"]))
VIEW,FROM,ENDV = map(pp.Suppress, map(pp.Literal, ["view", "from", "endv"]))
FTH,TH,ENDFTH,ENDTH = map(pp.Suppress, map(pp.Literal, ["fth", "th", "endfth", "endth"]))
MB,CMB,EQ,CEQ,RL,CRL = map(pp.Suppress, map(pp.Literal, ["mb", "cmb", "eq", "ceq", "rl", "crl"]))


# Token string
# What about the empty token string?
tokenstring = pp.Forward()
ts_list = LPAREN + pp.ZeroOrMore(tokenstring) + RPAREN
tokenstring << pp.OneOrMore(token | ts_list).addParseAction(lambda x: ast.TokenString(x.asList()))

# Term definition
term = pp.Forward()
t_list = LPAREN + pp.ZeroOrMore(term) + RPAREN
term << pp.OneOrMore(token | t_list).addParseAction(lambda x: ast.Term(x.asList()))

# Operation identifier. Simple identifier with possible underscores.
opid = pp.Word(pp.alphanums + "_")

# Operation formula
opform = pp.Forward()
opformbody = opid | pp.Group(LPAREN + opform + RPAREN)
opform << opformbody + opformbody + pp.ZeroOrMore(opformbody)

# Variable and Sort ID. An identifier consisting of a variable name
# followed by a colon followed by a sort name
varandsortid = pp.Word(pp.alphanums) + COLON + pp.Word(pp.alphanums)

# Variable ID. Simple identifier. Capitalised.
varid = pp.Word(pp.srange("[A-Z]"), pp.alphanums)

# Sort ID.
sortid = pp.Word(pp.srange("[A-Z]"), pp.alphanums).addParseAction(lambda x: ast.Ident(x[0]))

# Parameter ID.
parameterid = pp.Word(pp.srange("[A-Z]"), exact=1)

# View ID
viewid = pp.Word(pp.srange("[A-Z]"), pp.alphanums)

# Module ID
modid = pp.Word(pp.srange("[A-Z0-9]")).addParseAction(lambda x: ast.Ident(x[0]))

# String ID
stringid = pp.dblQuotedString

# File name. OS dependent
windowsfilename = pp.Word(pp.alphanums) + FULLSTOP + pp.Word(pp.alphanums, max=3)
linuxfilename = pp.Word(pp.alphanums)
filename = pp.Word(pp.alphanums)

# path. OS dependent.
path = pp.Word(pp.alphanums + "./")

# LS flags. OS dependent.
lsflags = pp.Word(pp.alphanums)

# Auxilary Bracket Lists
bracketnatlist = LPAREN + pp.OneOrMore(nat) + RPAREN
brackettokenlist = LPAREN + pp.OneOrMore(token) + RPAREN
bracketgatherlist = LPAREN + pp.OneOrMore(pp.Literal("e") | pp.Literal("E") | pp.Literal("&")) + RPAREN
brackettokenstring = LPAREN + tokenstring + RPAREN

# Hook.
# In the Maude Grammar it says that only an id-hook has a following token.
# This seems to be wrong as there are examples of all hooks having following tokens.
# There also seems to be detail missing

def idhookparseaction(x):
    if len(x) > 1:
        return ast.IDHook(x[0], x[1])
    else:
        return ast.IDHook(x[0], [])

idhook = pp.Group(pp.Literal("id-hook").suppress() + token + pp.Optional(brackettokenstring)).addParseAction(lambda x: idhookparseaction(x[0]))
ophook = pp.Group(pp.Literal("op-hook").suppress() + brackettokenstring).addParseAction(lambda x: ast.OPHook(x[0]))
termhook = pp.Group(pp.Literal("term-hook").suppress() + brackettokenstring).addParseAction(lambda x: ast.TermHook(x[0]))
hook = idhook | ophook | termhook

brackethooklist = LPAREN + pp.OneOrMore(hook) + RPAREN

# Print Item.
printitem = stringid | varid | varandsortid

# Statement Attribute
# TODO implement metadata, label and print classes
statementattr = LSBRACK + pp.OneOrMore(pp.Literal("nonexec").suppress().addParseAction(partial(ast.StatementAttribute,
                                                                                               ast.StatementAttributeType.nonexec)) |
                                       pp.Literal("otherwise").suppress().addParseAction(partial(ast.StatementAttribute,
                                                                                                 ast.StatementAttributeType.otherwise)) |
                                       pp.Literal("variant").suppress().addParseAction(partial(ast.StatementAttribute,
                                                                                               ast.StatementAttributeType.variant)) |
                                       pp.Group(pp.Literal("metadata").suppress() + stringid).addParseAction(partial(ast.StatementAttribute,
                                                                                                                     ast.StatementAttributeType.metadata)) |
                                       pp.Group(pp.Literal("label").suppress() + labelid).addParseAction(partial(ast.StatementAttribute,
                                                                                                                 ast.StatementAttributeType.label)) |
                                       pp.Group(pp.Literal("print").suppress() + pp.ZeroOrMore(printitem)).addParseAction(partial(ast.StatementAttribute,
                                                                                                                                  ast.StatementAttributeType.print))) + RSBRACK

def idparseaction(x):
    direction = x[0]
    if direction == "left":
        return ast.ID(ast.IDDirection.left, x.asList()[1:])
    elif direction == "right":
        return ast.ID(ast.IDDirection.right, x.asList()[1:])
    else:
        return ast.ID(direction, x.asList())

# Attributes
assocattr = pp.Literal("assoc").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.assoc))
commattr = pp.Literal("comm").suppress().addParseAction(partial(ast.MaudeAttribute, ast.AttributeType.comm))
idattr = pp.Group(pp.Optional(pp.Literal("left") | pp.Literal("right")) + pp.Literal("id:").suppress()
                  + term).addParseAction(lambda x: idparseaction(x[0]))
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

attr = LSBRACK + pp.OneOrMore( assocattr | commattr | idattr | idemattr | iterattr | memoattr
                                                | dittoattr | configattr | objattr | msgattr | metadataattr | stratattr
                                                | polyattr | frozenattr | precattr | gatherattr | formatattr
                                                | specialattr) + RSBRACK

# Sort
sort = pp.Forward()
sort << (sortid +
         pp.Optional(LCBRACK + sort + pp.ZeroOrMore(COMMA + sort) + RCBRACK)).addParseAction(lambda x: ast.Sort(x[0], x[1:]))

# Condition fragment
conditionfragment = pp.Forward()
conditionfragmentprime = conditionfragment | term + RIGHTARROW + term
conditionfragment << term + EQUAL + term | \
    term + ASSIGN + term | \
    term + COLON + sort

# Condition
condition = conditionfragment + pp.ZeroOrMore(AND + conditionfragment)
conditionprime = conditionfragmentprime + pp.ZeroOrMore(AND + conditionfragmentprime)

# Label
label = LSBRACK + labelid.addParseAction(lambda x: ast.Label(x[0])) + RSBRACK + COLON

# Statement
# TODO these statements had optional labels. I have removed them temporarily.
mbstatement = pp.Group(MB + term + COLON + sort).addParseAction(lambda x: ast.MbStatement(x[0][0], x[0][1]))
cmbstatement = pp.Group(CMB + term + COLON + sort + IF + condition).addParseAction(lambda x: ast.CmbStatement(x[0][0], x[0][1], x[0][2]))
eqstatement = pp.Group(EQ+ term + EQUAL + term).addParseAction(lambda x: ast.EqStatement(x[0][0], x[0][1]))
ceqstatement = pp.Group(CEQ+ term + EQUAL + term + IF + condition).addParseAction(lambda x: ast.CeqStatement(x[0][0], x[0][1], x[0][2]))
statement = mbstatement | cmbstatement | eqstatement | ceqstatement

rlstatement = pp.Group(RL + term + RIGHTARROW + term)
crlstatement = pp.Group(CRL + term + RIGHTARROW + term + IF + condition)
statementprime = rlstatement | crlstatement


# Mod elt
modelt = pp.Forward()
modeltprime = modelt | pp.Group(statementprime + pp.Optional(statementattr) + FULLSTOP)

# Kind
kind = LSBRACK + sort + pp.ZeroOrMore(COMMA + sort) + RSBRACK

# Type
maudetype = sort | kind

# Arrow
arrow = pp.Literal("->") | pp.Literal("~>")

# To part renaming item
topartrenamingitem = TO + opform + pp.Optional(attr)

# Renaming Item
renamingitem = pp.Group(SORT + sort + TO + sort) | \
               pp.Group(LABEL + labelid + TO + labelid) | \
               pp.Group(OP + opform + topartrenamingitem) | \
               pp.Group(OP + opform + COLON + pp.ZeroOrMore(maudetype) + arrow + maudetype + topartrenamingitem)
# Renaming
renaming = pp.Group(LPAREN + renamingitem + pp.ZeroOrMore(COMMA + renamingitem) + RPAREN)

# Mod Exp
modexp = pp.Forward()
modexp << modid | \
    pp.Group(LPAREN + modexp + RPAREN) | \
    pp.Group(modexp + "+" + modexp) | \
    pp.Group(modexp + "*" + renaming) | \
    pp.Group(modexp + LCBRACK + viewid + pp.ZeroOrMore(COMMA + viewid) + RCBRACK)

# View Elt
viewelt = pp.Group(VAR + pp.OneOrMore(varid) + COLON + maudetype + FULLSTOP) | \
          pp.Group(SORT + sort + TO + sort + FULLSTOP) | \
          pp.Group(LABEL + labelid + TO + labelid + FULLSTOP) | \
          pp.Group(OP + opform + TO + opform + FULLSTOP) | \
          pp.Group(OP + opform + COLON + pp.ZeroOrMore(maudetype) + arrow + maudetype + TO + opform + FULLSTOP) | \
          pp.Group(OP + term + TO + term + FULLSTOP)

#Subsort
subsort = pp.Group(pp.OneOrMore(sort) + pp.Group(pp.OneOrMore(LESSTHAN + pp.OneOrMore(sort)))).addParseAction(lambda x:  ast.Subsort(x[0][0], x[0][1].asList()))

# module elements
includeelt = pp.Group(INCLUDING + modexp + FULLSTOP).addParseAction(lambda x: ast.Include(x[0][0]))
extendelt = pp.Group(EXTENDING + modexp + FULLSTOP).addParseAction(lambda x: ast.Extend(x[0][0]))
protectelt = pp.Group(PROTECTING + modexp + FULLSTOP).addParseAction(lambda x: ast.Protect(x[0][0]))

# Mod Elt
modelt = includeelt | \
         extendelt | \
         protectelt | \
         pp.Group(SORTS + pp.OneOrMore(sort) + FULLSTOP) | \
         pp.Group(SUBSORTS + subsort + FULLSTOP) | \
         pp.Group(OP + opform + COLON + pp.ZeroOrMore(maudetype) + arrow + maudetype + pp.Optional(attr) + FULLSTOP) | \
         pp.Group(OPS + pp.OneOrMore(opid | LPAREN + opform + RPAREN) + COLON \
         + pp.ZeroOrMore(maudetype) + arrow + maudetype + pp.Optional(attr) + FULLSTOP) | \
         pp.Group(VARS + pp.OneOrMore(varid) + COLON + maudetype + FULLSTOP) | \
         pp.Group(statement + pp.Optional(statementattr) + FULLSTOP)

# ParameterDecl
parameterdecl = pp.Group(parameterid + "::" + modexp)

# Parameter List
parameterlist = pp.Group(LCBRACK + parameterdecl + pp.ZeroOrMore(COMMA + parameterdecl) + RCBRACK)

# View
view = pp.Group(VIEW + viewid + FROM + modexp + TO + modexp + IS + pp.ZeroOrMore(viewelt) + ENDV)

# Theory
theory = pp.Group(FTH + modid + IS + pp.ZeroOrMore(modelt) + ENDFTH) | \
         pp.Group(TH + modid + IS + pp.ZeroOrMore(modeltprime) + ENDTH)

# Module
module = pp.Group(FMOD + modid + pp.Optional(parameterlist) + IS + pp.ZeroOrMore(modelt) + ENDFM) | \
         pp.Group(MOD + modid + pp.Optional(parameterlist) + IS + pp.ZeroOrMore(modeltprime) + ENDFM)

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
inmodid = pp.Optional(IN + modid + COLON)
suchthatcondition = pp.Optional("such that" + condition)
optionaldebug = pp.Optional("debug")
optionalnat = pp.Optional(LSBRACK + nat + RSBRACK)

opidformlist = pp.OneOrMore(opid | (LPAREN + opform + RPAREN))
command = pp.Literal("select") + modid + FULLSTOP | \
          pp.Literal("parse") + inmodid + term + FULLSTOP | \
          optionaldebug + pp.Literal("reduce") + inmodid + term + FULLSTOP | \
          optionaldebug + pp.Literal("rewrite") + optionalnat + inmodid + term + FULLSTOP | \
          optionaldebug + pp.Literal("frewrite") + pp.Optional(
              "[" + nat + pp.Optional("," + nat) + "]") + inmodid + term + FULLSTOP | \
          optionaldebug + pp.Literal("erewrite") + pp.Optional(
              "[" + nat + pp.Optional("," + nat) + "]") + inmodid + term + FULLSTOP | \
          (pp.Literal("match") | pp.Literal(
              "xmatch")) + optionalnat + inmodid + term + "<=?" + term + suchthatcondition + FULLSTOP | \
          "unify" + optionalnat + inmodid + unificationequation + pp.ZeroOrMore(
              "/\\" + unificationequation) + FULLSTOP | \
          optionaldebug + "variant unify" + optionalnat + inmodid + unificationequation + pp.ZeroOrMore(
              "/\\" + unificationequation) + FULLSTOP | \
          optionaldebug + "get variants" + optionalnat + inmodid + term + FULLSTOP | \
          "search" + optionalnat + inmodid + term + searchtype + term + suchthatcondition + FULLSTOP | \
          optionaldebug + "continue" + nat + FULLSTOP | \
          "loop" + inmodid + term + FULLSTOP | \
          LPAREN + tokenstring + RPAREN | \
          "trace" + (pp.Literal("select") | pp.Literal("deselect") | pp.Literal("include") | pp.Literal(
              "exclude")) + opidformlist + FULLSTOP | \
          "print" + (pp.Literal("conceal") | pp.Literal("reveal")) + opidformlist + FULLSTOP | \
          "break" + (pp.Literal("select") | pp.Literal("deselect")) + opidformlist + FULLSTOP | \
          SHOW + showitem + pp.Optional(modid) + FULLSTOP | \
          SHOW + "view" + pp.Optional(viewid) + FULLSTOP | \
          SHOW + "modules" + FULLSTOP | \
          SHOW + "views" + FULLSTOP | \
          SHOW + "search" + "graph" + FULLSTOP | \
          SHOW + pp.Literal("path") + pp.Optional("labels") + nat + FULLSTOP | \
          pp.Literal("do") + pp.Literal("clear") + pp.Literal("memo") + FULLSTOP | \
          pp.Literal("set") + setoption + (pp.Literal("on") | pp.Literal("off")) + FULLSTOP

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

