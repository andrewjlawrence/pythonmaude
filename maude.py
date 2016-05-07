import pyparsing as pp

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
hook = ("id-hook" + token + pp.Optional(pp.Group("(" + tokenstring + ")"))) | ((pp.Literal("op-hook") | pp.Literal("term-hook")) + pp.Group("(" + tokenstring + ")"))

# Print Item.
printitem = stringid | varid | varandsortid

# Statement Attribute
statementattr = "[" + pp.OneOrMore(pp.Literal("nonexec") | pp.Literal("otherwise") | pp.Literal("variant") | pp.Group(pp.Literal("metadata") + stringid) | pp.Group(pp.Literal("label") + labelid) | pp.Group(pp.Literal("print") + pp.ZeroOrMore(printitem))) + "]"


test = "[print \"meh\" \"meh\" \"meh\"]"
print (test, "->", statementattr.parseString(test))