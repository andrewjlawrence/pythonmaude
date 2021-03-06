# Copyright 2017 Andrew Lawrence
import pyparsing
import maudeparser as mp
import ast
import unittest


def failureFun(string):
    result = False
    try:
        meh = mp.systemcommand.parseString(string)
    except pyparsing.ParseException:
        result = True
    return result


class TestSystemCommands(unittest.TestCase):
    def testInCommand(self):
        self.assertEqual(mp.systemcommand.parseString("in meh")[0], ast.InCommand("meh"))

    def testInCommandFailure(self):
        self.assert_(failureFun("inmeh"))

    def testLoadCommand(self):
        self.assertEqual(mp.systemcommand.parseString("load meh")[0], ast.LoadCommand("meh"))

    def testLoadCommandFailure(self):
        self.assert_(failureFun("loadmeh"))

    def testQuitCommnad(self):
        self.assertEqual(mp.systemcommand.parseString("quit")[0], ast.QuitCommand())

    def testEofCommand(self):
        self.assertEqual(mp.systemcommand.parseString("eof")[0], ast.EofCommand())

    def testPopDCommand(self):
        self.assertEqual(mp.systemcommand.parseString("popd")[0], ast.PopDCommand())

    def testPwdCommand(self):
        self.assertEqual(mp.systemcommand.parseString("pwd")[0], ast.PwdCommand())

    def testCDCommand(self):
        self.assertEqual(mp.systemcommand.parseString("cd meh")[0], ast.CdCommand("meh"))

    def testPushCommand(self):
        self.assertEqual(mp.systemcommand.parseString("push meh")[0], ast.PushCommand("meh"))

    def testLsCommand(self):
        self.assertEqual(mp.systemcommand.parseString("ls")[0], ast.LsCommand(""))

    def testLsCommand2(self):
        self.assertEqual(mp.systemcommand.parseString("ls meh")[0], ast.LsCommand("meh"))

    def testCommandFailure(self):
        self.assert_(failureFun("meh"))


class TestToken(unittest.TestCase):
    def testToken(self):
        self.assertEqual(mp.token.parseString("meh")[0], ast.Token("meh"))

    def testToken(self):
        self.assertEqual(mp.token.parseString("meh")[0], ast.Token("meh"))

class TestTokenString(unittest.TestCase):
    def testTokenString(self):
        print(mp.tokenstring.parseString("meh (meh meh)"))
        self.assertEqual(mp.tokenstring.parseString("meh (meh meh)")[0],
                         ast.TokenString([ast.Token("meh"), ast.TokenString([ast.Token("meh"), ast.Token("meh")])]))

    def testTokenString2(self):
        print(mp.tokenstring.parseString("(meh meh) meh"))
        self.assertEqual(mp.tokenstring.parseString("(meh meh) meh")[0],
                         ast.TokenString([ast.TokenString([ast.Token("meh"), ast.Token("meh")]), ast.Token("meh")]))

    def testTokenString3(self):
        print(mp.tokenstring.parseString("meh (meh (meh))"))
        self.assertEqual(mp.tokenstring.parseString("meh (meh (meh))")[0],
                         ast.TokenString([ast.Token("meh"), ast.TokenString([ast.Token("meh"), ast.TokenString([ast.Token("meh")])])]))

    def testTokenString4(self):
        self.assertEqual(mp.tokenstring.parseString("meh meh")[0], ast.TokenString([ast.Token("meh"), ast.Token("meh")]))

    def testTokenString5(self):
        print(mp.tokenstring.parseString("(meh) (meh)"))
        self.assertEqual(mp.tokenstring.parseString("(meh) (meh)")[0],
                         ast.TokenString([ast.TokenString([ast.Token("meh")]),ast.TokenString([ast.Token("meh")])]))


class TestBracketTokenString(unittest.TestCase):
    def testBracketTokenString(self):
        print(mp.brackettokenstring.parseString("(meh (meh meh))")[0])
        self.assertEqual(mp.brackettokenstring.parseString("(meh (meh meh))")[0],
                         ast.TokenString([ast.Token("meh"), ast.TokenString([ast.Token("meh"), ast.Token("meh")])]))


class TestTerm(unittest.TestCase):
    def testTerm(self):
        self.assertEqual(mp.term.parseString("meh (meh)")[0], ast.Term([ast.Token("meh"), ast.Term([ast.Token("meh")])]))


class TestHook(unittest.TestCase):
    def testIDHook1(self):
        self.assertEqual(mp.hook.parseString("id-hook meh")[0], ast.IDHook(ast.Token("meh"), []))

    def testIDHook2(self):
        self.assertEqual(mp.hook.parseString("id-hook meh (meh)")[0], ast.IDHook(ast.Token("meh"), ast.TokenString([ast.Token("meh")])))

    def testOPHook(self):
        self.assertEqual(mp.hook.parseString("op-hook(meh meh)")[0], ast.OPHook([ast.TokenString([ast.Token("meh"), ast.Token("meh")])]))

    def testTermHook(self):
        self.assertEqual(mp.hook.parseString("term-hook(meh meh)")[0], ast.TermHook([ast.TokenString([ast.Token("meh"), ast.Token("meh")])]))


class TestAttribute(unittest.TestCase):
    def testAssoc(self):
        self.assertEqual(mp.attr.parseString("[ assoc ]")[0], ast.MaudeAttribute(ast.AttributeType.assoc))

    def testComm(self):
        self.assertEqual(mp.attr.parseString("[comm]")[0], ast.MaudeAttribute(ast.AttributeType.comm))

    def testCommAssoc(self):
        self.assertEqual(mp.attr.parseString("[comm assoc]").asList(),
                         [ast.MaudeAttribute(ast.AttributeType.comm), ast.MaudeAttribute(ast.AttributeType.assoc)])

    def testCommAssocNoSpace(self):
        self.assert_(failureFun("[commassoc]"))

    def testRightID(self):
        self.assertEqual(mp.attr.parseString("[right id: meh meh]")[0],
                         ast.ID(ast.IDDirection.right, [ast.Term([ast.Token("meh"), ast.Token("meh")])]))

    def testLeftID(self):
        mp.attr.setDebug()
        print(mp.attr.parseString("[left id: meh meh]")[0])
        self.assertEqual(mp.attr.parseString("[left id: meh meh]")[0],
                         ast.ID(ast.IDDirection.left, [ast.Term([ast.Token("meh"), ast.Token("meh")])]))

    def testIdem(self):
        self.assertEqual(mp.attr.parseString("[idem]")[0], ast.MaudeAttribute(ast.AttributeType.idem))

    def testIter(self):
        self.assertEqual(mp.attr.parseString("[iter]")[0], ast.MaudeAttribute(ast.AttributeType.iter))

    def testMemo(self):
        self.assertEqual(mp.attr.parseString("[memo]")[0], ast.MaudeAttribute(ast.AttributeType.memo))

    def testDitto(self):
        self.assertEqual(mp.attr.parseString("[ditto]")[0], ast.MaudeAttribute(ast.AttributeType.ditto))

    def testConfig(self):
        self.assertEqual(mp.attr.parseString("[config]")[0], ast.MaudeAttribute(ast.AttributeType.config))

    def testObj(self):
        self.assertEqual(mp.attr.parseString("[obj]")[0], ast.MaudeAttribute(ast.AttributeType.obj))

    def testMsg(self):
        self.assertEqual(mp.attr.parseString("[msg]")[0], ast.MaudeAttribute(ast.AttributeType.msg))

    def testMetadata(self):
        self.assertEqual(mp.attr.parseString("[metadata \"meh\"]")[0], ast.MetaData("\"meh\""))

    def testStrat(self):
        self.assertEqual(mp.attr.parseString("[strat (0 1 2)]")[0], ast.Strat([0,1,2]))

    def testPoly(self):
        self.assertEqual(mp.attr.parseString("[poly (0 1 2)]")[0], ast.Poly([0,1,2]))

    def testFrozen(self):
        ###self.assertEqual(mp.attr.parseString("[frozen]"), ast.Frozen([]))
        self.assertEqual(mp.attr.parseString("[frozen (0 1 2)]")[0], ast.Frozen([0, 1, 2]))

    def testPrec(self):
        self.assertEqual(mp.attr.parseString("[prec 0]")[0], ast.Prec([0]))

    def testPrecNoNum(self):
        self.assert_(failureFun("[prec]"))

    def testGather(self):
        self.assertEqual(mp.attr.parseString("[gather (e)]")[0], ast.Gather("e"))

    def testFormat(self):
        self.assertEqual(mp.attr.parseString("[format (meh)]")[0], ast.Format(ast.Token("meh")))

    def testSpecial(self):
        self.assertEqual(mp.attr.parseString("[special (id-hook meh)]")[0], ast.Special(ast.IDHook(ast.Token("meh"), [])))

class TestStatementAttribute(unittest.TestCase):
    def testNonExec(self):
        self.assertEqual(mp.statementattr.parseString("[nonexec]")[0],
                         ast.StatementAttribute(ast.StatementAttributeType.nonexec))

    def testOtherwise(self):
        self.assertEqual(mp.statementattr.parseString("[otherwise]")[0],
                         ast.StatementAttribute(ast.StatementAttributeType.otherwise))

    def testVariant(self):
        self.assertEqual(mp.statementattr.parseString("[variant]")[0],
                         ast.StatementAttribute(ast.StatementAttributeType.variant))

    def testMetadata(self):
        self.assertEqual(mp.statementattr.parseString("[metadata \"meh\"]")[0],
                         ast.StatementAttribute(ast.StatementAttributeType.metadata))

    def testLabel(self):
        self.assertEqual(mp.statementattr.parseString("[label meh]")[0],
                         ast.StatementAttribute(ast.StatementAttributeType.label))

    def testPrint(self):
        self.assertEqual(mp.statementattr.parseString("[print MEH]")[0],
                         ast.StatementAttribute(ast.StatementAttributeType.print))


class TestIdent(unittest.TestCase):
    def testSortID(self):
        self.assertEqual(mp.sortid.parseString("MEHID")[0],
                         ast.Ident("MEHID", 1, 1))

class TestSort(unittest.TestCase):
    def testSort1(self):
        self.assertEqual(mp.sort.parseString("MEHID")[0],
                         ast.Sort(ast.Ident("MEHID", 1, 1), []))

    def testSort2(self):
        self.assertEqual(mp.sort.parseString("LIST{NAT}")[0],
                         ast.Sort(ast.Ident("LIST", 1, 1), [ast.Sort(ast.Ident("NAT", 1, 6), [])]))


class TestSubsort(unittest.TestCase):
    def testSubsort1(self):
        self.assertEqual(mp.subsort.parseString("NAT < INT")[0].subsort,
                         ast.Sort(ast.Ident("NAT", 1, 1), []))

    def testSubsort2(self):
            self.assertEqual(ast.Subsort(mp.sort.parseString("NAT")[0], [mp.sort.parseString("INT")[0]]),
                             ast.Subsort(ast.Sort(ast.Ident("NAT", 1, 1), []), [ast.Sort(ast.Ident("INT", 1, 1), [])] ))

    def testSubsort3(self):
        self.assertEqual(mp.subsort.parseString("NAT < INT")[0].sortlist,
                         [ast.Sort(ast.Ident("INT", 1, 7), [])])

    def testSubsort4(self):
            self.assertEqual(mp.subsort.parseString("NAT < INT")[0],
                             ast.Subsort(ast.Sort(ast.Ident("NAT", 1, 1), []), [ast.Sort(ast.Ident("INT", 1, 7), [])]))

class TestStatement(unittest.TestCase):
    def testEqStatement(self):
        self.assertEqual(mp.eqstatement.parseString("eq term1 = term2")[0],
                         ast.Equation(ast.Term([ast.Token("term1")]), ast.Term([ast.Token("term2")])))

    def testMbStatement(self):
        self.assertEqual(mp.mbstatement.parseString("mb term : NAT")[0],
                         ast.MbStatement(ast.Term([ast.Token("term")]), ast.Sort(ast.Ident("NAT", 1, 11),[])))

    def testCmbStatement(self):
        self.assertEqual(mp.cmbstatement.parseString("cmb term : NAT if x = y")[0], ast.CmbStatement(ast.Term([ast.Token("term")]),
                                                                                                     ast.Sort(ast.Ident("NAT", 1, 12),[]),
                                                                                                     ast.Condition([ast.EqFragment(ast.Term([ast.Token("x")]),
                                                                                                                                   ast.Term([ast.Token("y")]))])))

    def testCmbStatement2(self):
        self.assertEqual(mp.cmbstatement.parseString("cmb term : NAT if x = y")[0].condition,
                         ast.Condition([ast.EqFragment(ast.Term([ast.Token("x")]), ast.Term([ast.Token("y")]))]))


    def testRlStatement(self):
        self.assertEqual(mp.rlstatement.parseString("rl x => y")[0],
                         ast.RlStatement(ast.Term([ast.Token("x")]), ast.Term([ast.Token("y")])))
"""
Add these tests when conditions are implemented.
    def testCeqStatement(self):
        mp.ceqstatement.setDebug(True)
        self.assertEqual(mp.ceqstatement.parseString("ceq term1 = term2 if xistrue")[0],
                         ast.CeqStatement(ast.Term([ast.Token("term1")]), ast.Term([ast.Token("term2")])))
                         )
"""

class TestConditionFragment(unittest.TestCase):
    def testEqFragment1(self):
        self.assertEqual(mp.conditionfragment.parseString("term1 = term2")[0],
                         ast.EqFragment(ast.Term([ast.Token("term1")]), ast.Term([ast.Token("term2")])))

    def testEqFragment2(self):
        self.assertEqual(mp.conditionfragment.parseString("term1 = term2")[0].leftterm,
                         ast.Term([ast.Token("term1")]))

    def testEqFragment3(self):
        self.assertEqual(mp.conditionfragment.parseString("term1 = term2")[0].rightterm,
                        ast.Term([ast.Token("term2")]))


class TestCondition(unittest.TestCase):
    def testCondition(self):
        self.assertEqual(mp.condition.parseString("term1 = term2")[0],
                         ast.Condition([ast.EqFragment(ast.Term([ast.Token("term1")]), ast.Term([ast.Token("term2")]))]))

    def testConditionFragmentlist(self):
        self.assertEqual(mp.condition.parseString("term1 = term2")[0].fragmentlist,
                         ast.Condition([ast.EqFragment(ast.Term([ast.Token("term1")]), ast.Term([ast.Token("term2")]))]).fragmentlist)


class TestModuleElement(unittest.TestCase):
    def testSorts(self):
        self.assertEqual(mp.sortselt.parseString("sorts SORTX SORTY .", parseAll=True)[0],
                         ast.Sorts([ast.Sort(ast.Ident("SORTX", 1 , 7),[]),
                                    ast.Sort(ast.Ident("SORTY", 1, 13),[])]))

    def testOp(self):
        self.assertEqual(mp.opelt.parseString("op plus : NAT NAT -> NAT .", parseAll=True)[0],
                         ast.Op(ast.Ident("plus", 1 ,4),
                                [ast.Sort(ast.Ident("NAT", 1, 11), []), ast.Sort(ast.Ident("NAT", 1, 15), [])],
                                "->",
                                ast.Sort(ast.Ident("NAT", 1, 22), []),
                                []))
    def testOpOpForm(self):
        self.assertEqual(mp.opelt.parseString("op plus : NAT NAT -> NAT .", parseAll=True)[0].opform,
                         ast.Op(ast.Ident("plus", 1 ,4),
                                [ast.Sort(ast.Ident("NAT", 1, 10), []), ast.Sort(ast.Ident("NAT", 1, 14), [])],
                                "->",
                                ast.Sort(ast.Ident("NAT", 1, 21), []),
                                []).opform)

    def testVars(self):
        self.assertEqual(mp.varselt.parseString("vars X1 : NAT .", parseAll=True)[0],
                         ast.Vars([ast.Ident("X1", 1, 6)], ast.Sort(ast.Ident("NAT", 1, 11), [])))

    def testStatement(self):
        self.assertEqual(mp.statementelt.parseString("eq term1 = term2 .", parseAll=True)[0],
                         ast.Statement(ast.Equation(ast.Term([ast.Token("term1")]), ast.Term([ast.Token("term2")])),[]))

class TestModuleElementPrime(unittest.TestCase):
    def testSorts(self):
        result = mp.modeltprime.parseString("sorts SORTX SORTY .", parseAll=True)[0]
        self.assertEqual(mp.modeltprime.parseString("sorts SORTX SORTY .", parseAll=True)[0],
                         ast.Sorts([ast.Sort(ast.Ident("SORTX", 1 , 7),[]),
                                    ast.Sort(ast.Ident("SORTY", 1, 13),[])]))

    def testRules(self):
        result = mp.modeltprime.parseString("sorts SORTX SORTY .", parseAll=True)[0]
        self.assertEqual(mp.modeltprime.parseString("sorts SORTX SORTY .", parseAll=True)[0],
                         ast.Sorts([ast.Sort(ast.Ident("SORTX", 1 , 7),[]),
                                    ast.Sort(ast.Ident("SORTY", 1, 13),[])]))



class TestFModule(unittest.TestCase):

    def testemptyfmod(self):
        self.assertEqual(mp.module.parseString("fmod MYMODULE is endfm", parseAll=True)[0],
                         ast.Module(ast.Ident("MYMODULE", 1, 6), []))

    def testemptymodule(self):
        self.assertEqual(mp.module.parseFile("./testdata/emptymodule.maude", parseAll=True)[0],
                         ast.Module(ast.Ident("MYMODULE", 1, 6), []))

    def testemptyfmodule(self):
        self.assertEqual(mp.module.parseFile("./testdata/emptyfmodule.maude", parseAll=True)[0],
                         ast.Module(ast.Ident("MYMODULE", 1, 6), []))

    def testsimplemodule(self):
        module = ast.Module(ast.Ident("MYMODULE", 1, 5), [])
        module.addsort(ast.Sort(ast.Ident("SORTX", 2, 11), []))
        module.addsort(ast.Sort(ast.Ident("SORTY", 2, 17), []))
        module.addop(ast.Op(ast.Ident("plus", 3, 8),
                            [ast.Sort(ast.Ident("NAT", 3, 15), []),
                             ast.Sort(ast.Ident("NAT", 3, 19), [])],
                             "->",
                             ast.Sort(ast.Ident("NAT", 3, 26), []),
                            []))
        module.addvar(ast.Var(ast.Ident("X1", 4, 10),
                              ast.Sort(ast.Ident("NAT", 4, 15), [])))
        rulestatement = ast.RlStatement(ast.Term([ast.Token("term1")]),
                                      ast.Term([ast.Token("term2")]))
        module.addstatement(ast.Statement(rulestatement, None))
        resultingmodule = mp.module.parseFile("./testdata/simplemodule.maude", parseAll=True)[0]
        self.assertEqual(module,
                         resultingmodule)

    def testsimplemodule2(self):
        self.assertEqual(mp.module.parseFile("./testdata/simplefmodule.maude", parseAll=True)[0].elementlist,
                         [ast.Sorts([ast.Sort(ast.Ident("SORTX", 2, 11), []), ast.Sort(ast.Ident("SORTY", 2, 17), [])]),
                          ast.Op(ast.Ident("plus", 3, 8),
                                [ast.Sort(ast.Ident("NAT", 3, 15), []),
                                 ast.Sort(ast.Ident("NAT", 3, 19), [])],
                                "->",
                                ast.Sort(ast.Ident("NAT", 3, 26), []),
                                []),
                          ast.Vars([ast.Ident("X1", 4, 10)], ast.Sort(ast.Ident("NAT", 4, 15), [])),
                          ast.Statement(
                             ast.Equation(ast.Term([ast.Token("term1")]),
                                          ast.Term([ast.Token("term2")])), [])
                         ])

if __name__ == '__main__':
    unittest.main()

