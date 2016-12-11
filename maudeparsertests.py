# Copyright 2016 Andrew Lawrence
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
        self.assertEqual(mp.hook.parseString("term-hook(meh meh)")[0], ast.TermHook([ast.Token("meh"), ast.Token("meh")]))


class TestAttribute(unittest.TestCase):
    def testAssoc(self):
        self.assertEqual(mp.attr.parseString("[assoc]")[0], ast.MaudeAttribute(ast.AttributeType.assoc))

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


if __name__ == '__main__':
    unittest.main()

