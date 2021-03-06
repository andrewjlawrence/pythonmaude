# Copyright 2017 Andrew Lawrence
import pyparsing as pp
import ast as ast
from functools import partial
# Label identifier. Simple identifier
labelid = pp.Word(pp.alphanums)

# Natural numbers
nat = pp.Word(pp.nums).addParseAction(lambda x: int(x[0]))

# Token
# TODO I removed the eq symbol from tokens. Should it be allowed?
token = pp.Word(pp.alphanums + '!"#$%&*+,-/;<>?@^_`{|}~').setResultsName("token").addParseAction(lambda x: ast.Token(x.asList()[0]))

# Special Symbols
LPAREN,RPAREN,LCBRACK,RCBRACK,LSBRACK,RSBRACK,COMMA,FULLSTOP,EQUAL, = map(pp.Suppress, "(){}[],.=")
COLON,LESSTHAN = map(pp.Suppress, ":<")

# Key words
IF,OP,OPS,TO,IS,SHOW,IN,AND = map(pp.Suppress, map(pp.Keyword, ["if", "op", "ops", "to", "is", "show", "in", "/\\"]))
RIGHTARROW,ASSIGN = map(pp.Suppress, map(pp.Keyword, ["=>", ":="]))
FMOD,MOD,ENDFM = map(pp.Suppress, map(pp.Keyword, ["fmod", "mod", "endfm"]))
VAR,VARS,SORT,SORTS,SUBSORTS,LABEL = map(pp.Suppress, map(pp.Keyword, ["var", "vars", "sort", "sorts", "subsorts", "label"]))
INCLUDING,EXTENDING,PROTECTING = map(pp.Suppress, map(pp.Keyword, ["including", "extending", "protecting"]))
VIEW,FROM,ENDV = map(pp.Suppress, map(pp.Keyword, ["view", "from", "endv"]))
FTH,TH,ENDFTH,ENDTH = map(pp.Suppress, map(pp.Keyword, ["fth", "th", "endfth", "endth"]))
MB,CMB,EQ,CEQ,RL,CRL = map(pp.Suppress, map(pp.Keyword, ["mb", "cmb", "eq", "ceq", "rl", "crl"]))


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
opid = pp.Word(pp.alphanums + "_").addParseAction(lambda st,locn,toks: ast.Ident(toks[0],
                                                                                 pp.lineno(locn, st),
                                                                                 pp.col(locn, st)))

# Operation formula
opform = pp.Forward()
opformbody = opid | pp.Group(LPAREN + opform + RPAREN)
opform << pp.OneOrMore(opformbody)

# Variable and Sort ID. An identifier consisting of a variable name
# followed by a colon followed by a sort name
varandsortid = pp.Word(pp.alphanums) + COLON + pp.Word(pp.alphanums)

# Variable ID. Simple identifier. Capitalised.
varid = pp.Word(pp.srange("[A-Z]"), pp.alphanums).addParseAction(lambda st,locn,toks:ast.Ident(toks[0],
                                                                                               pp.lineno(locn, st),
                                                                                               pp.col(locn, st)))

# Sort ID.
sortid = pp.Word(pp.srange("[A-Z]"), pp.alphanums).addParseAction(lambda st,locn,toks: ast.Ident(toks[0],
                                                                                                 pp.lineno(locn, st),
                                                                                                 pp.col(locn, st)))

# Parameter ID.
parameterid = pp.Word(pp.srange("[A-Z]"), exact=1)

# View ID
viewid = pp.Word(pp.srange("[A-Z]"), pp.alphanums).addParseAction(lambda st,locn,toks: ast.Ident(toks[0],
                                                                                                 pp.lineno(locn, st),
                                                                                                 pp.col(locn, st)))

# Module ID
modid = pp.Word(pp.srange("[A-Z0-9]")).addParseAction(lambda st,locn,toks: ast.Ident(toks[0],
                                                                                     pp.lineno(locn, st),
                                                                                     pp.col(locn, st)))

# String ID
stringid = pp.dblQuotedString

# File name. OS dependent
windowsfilename = pp.Word(pp.alphanums) + FULLSTOP + pp.Word(pp.alphanums, max=3)
linuxfilename = pp.Word(pp.alphanums)
filename = pp.Word(pp.alphanums + ".")

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
ophook = pp.Group(pp.Literal("op-hook").suppress() + brackettokenstring).addParseAction(lambda x: ast.OPHook(x[0].asList()))
termhook = pp.Group(pp.Literal("term-hook").suppress() + brackettokenstring).addParseAction(lambda x: ast.TermHook(x[0].asList()))
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
conditionfragment <<  pp.Group(term + EQUAL + term).addParseAction(lambda x: ast.EqFragment(x[0][0], x[0][1])) | \
                      pp.Group(term + ASSIGN + term) | \
                      pp.Group(term + COLON + sort)

# Condition
condition = pp.Group(conditionfragment + pp.ZeroOrMore(AND + conditionfragment)).addParseAction(lambda x: ast.Condition(x[0].asList()))
conditionprime = pp.Group(conditionfragmentprime + pp.ZeroOrMore(AND + conditionfragmentprime)).addParseAction(lambda x: ast.Condition(x[0]))

# Label
label = LSBRACK + labelid.addParseAction(lambda x: ast.Label(x[0])) + RSBRACK + COLON

# Statement
# TODO these statements had optional labels. I have removed them temporarily.
mbstatement = pp.Group(MB + term + COLON + sort).addParseAction(lambda x: ast.MbStatement(x[0][0], x[0][1]))
cmbstatement = pp.Group(CMB + term + COLON + sort + IF + condition).addParseAction(lambda x: ast.CmbStatement(x[0][0], x[0][1], x[0][2]))
eqstatement = pp.Group(EQ + term + EQUAL + term).addParseAction(lambda x: ast.Equation(x[0][0], x[0][1]))
ceqstatement = pp.Group(CEQ + term + EQUAL + term + IF + condition).addParseAction(lambda x: ast.ConditionalEquation(x[0][0], x[0][1], x[0][2]))
statement = mbstatement | cmbstatement | eqstatement | ceqstatement

rlstatement = pp.Group(RL + term + RIGHTARROW + term).addParseAction(lambda x: ast.RlStatement(x[0][0], x[0][1]))
crlstatement = pp.Group(CRL + term + RIGHTARROW + term + IF + condition)
statementprime = rlstatement | crlstatement

def makeStatement(statementparse):
    attrs = None
    if len(statementparse.asList()) == 2:
        attrs = statementparse.asList()[1]
    result = ast.Statement(statementparse[0].asList()[0],
                         attrs)
    return result

# Mod elt
modelt = pp.Forward()
modeltprime = modelt | (pp.Group(statementprime + pp.Optional(statementattr) + FULLSTOP)).addParseAction(makeStatement)

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

# Module elements
includeelt = pp.Group(INCLUDING + modexp + FULLSTOP).addParseAction(lambda x: ast.Include(x[0][0]))
extendelt = pp.Group(EXTENDING + modexp + FULLSTOP).addParseAction(lambda x: ast.Extend(x[0][0]))
protectelt = pp.Group(PROTECTING + modexp + FULLSTOP).addParseAction(lambda x: ast.Protect(x[0][0]))
sortselt =  pp.Group(SORTS + pp.OneOrMore(sort) + FULLSTOP).addParseAction(lambda x: ast.Sorts(x[0].asList()))
subsortselt = pp.Group(SUBSORTS + subsort + FULLSTOP)
opelt = pp.Group(OP + opform + COLON + pp.Group(pp.ZeroOrMore(maudetype)) +
                 arrow + maudetype + pp.Optional(attr,default=[]) + FULLSTOP).addParseAction(lambda x: ast.Op(x[0].asList()[0],
                                                                                                   x[0].asList()[1],
                                                                                                   x[0].asList()[2],
                                                                                                   x[0].asList()[3],
                                                                                                   x[0].asList()[4]))
opselt = pp.Group(OPS + pp.OneOrMore(opid | LPAREN + opform + RPAREN) + COLON \
                  + pp.ZeroOrMore(maudetype) + arrow + maudetype + pp.Optional(attr) + FULLSTOP)
varselt = pp.Group(VARS + pp.Group(pp.OneOrMore(varid)) + COLON +
                   maudetype + FULLSTOP).addParseAction(lambda x: ast.Vars(x[0].asList()[0],
                                                        x[0].asList()[1]))

statementelt = pp.Group(statement +
                        pp.Optional(statementattr,default=[]) + FULLSTOP).addParseAction(lambda x: ast.Statement(x[0].asList()[0],
                                                                                                                 x[0].asList()[1]))

# Mod Elt
modelt << (includeelt | extendelt | protectelt | sortselt | subsortselt | opelt | opselt | varselt | statementelt)

# ParameterDecl
parameterdecl = pp.Group(parameterid + "::" + modexp)

# Parameter List
parameterlist = pp.Group(LCBRACK + parameterdecl + pp.ZeroOrMore(COMMA + parameterdecl) + RCBRACK)

# View
view = pp.Group(VIEW + viewid + FROM + modexp + TO + modexp + IS + pp.ZeroOrMore(viewelt) + ENDV)

# Theory
theory = pp.Group(FTH + modid + IS + pp.ZeroOrMore(modelt) + ENDFTH) | \
         pp.Group(TH + modid + IS + pp.ZeroOrMore(modeltprime) + ENDTH)


def constructFunctionalModule(moduleid, parameterlist, elementlist):
    module = ast.Module(moduleid, parameterlist)
    for element in elementlist:
        if type(element) == ast.Sorts:
            for sort in element.sortlist:
                module.addsort(sort)
        if type(element) == ast.Vars:
            for var in element.varlist:
                module.addvar(var)
        if type(element) == ast.Op:
            module.addop(element)
        if type(element) == ast.Statement:
            module.addstatement(element)
    return module

# Module
module = pp.Group(FMOD + modid + pp.Optional(parameterlist,default=[]) +
                  IS + pp.Group(pp.ZeroOrMore(modelt)) + ENDFM).addParseAction(lambda x: constructFunctionalModule(x[0].asList()[0],
                                                                                                                   x[0].asList()[1],
                                                                                                                   x[0].asList()[2])) | \
         pp.Group(MOD + modid + pp.Optional(parameterlist, default=[]) + IS + pp.Group(pp.ZeroOrMore(modeltprime)) \
                  + ENDFM).addParseAction(lambda x: constructFunctionalModule(x[0].asList()[0],
                                                                              x[0].asList()[1],
                                                                              x[0].asList()[2]))

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

