import pyparsing as pp
import functools

def generateTermParsers (moduleset):
    termparser = pp.Forward()
    ttermparsers = list()
    for module in moduleset:
        for op in module.ops:
            argparsera = list()
            for i in range(len(op.arrow)):
                argparsera.append(termparser)
                if i + 1 < len(op.arrow):
                    argparsera.append(pp.Keyword(","))
                    argparser = functools.reduce(pp.And, argparsera)
                ttermparsers.append(pp.Group(pp.Token(op.opform) +  pp.Token("(") + argparser + pp.Token(")")))

    vtermparsers = list()
    for module in moduleset:
        for var in module.vars():
            vtermparsers.append(pp.Token(var))

    ttermparser = functools.reduce(pp.MatchFirst, ttermparsers)
    vtermparser = functools.reduce(pp.MatchFirst, vtermparsers)

    termparser << (ttermparser | vtermparser)

    return termparser



