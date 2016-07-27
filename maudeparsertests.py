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


class TestTokenString(unittest.TestCase):
    def testTokenString(self):
        self.assertEqual(mp.tokenstring.parseString("meh (meh meh)").asList(), ["meh", ["meh", "meh"]])

    def testTokenString2(self):
        self.assertEqual(mp.tokenstring.parseString("(meh meh) meh").asList(), [["meh", "meh"], "meh"])

    def testTokenString3(self):
        self.assertEqual(mp.tokenstring.parseString("meh (meh (meh))").asList(), ["meh", ["meh", ["meh"]]])

    def testTokenString4(self):
        self.assertEqual(mp.tokenstring.parseString("meh meh").asList(), ["meh", "meh"])


class TestBracketTokenString(unittest.TestCase):
    def testBracketTokenString(self):
        self.assertEqual(mp.brackettokenstring.parseString("(meh (meh meh))").asList(), ["meh", ["meh", "meh"]])

    def testBracketTokenString(self):
        self.assertEqual(mp.brackettokenstring.parseString("(meh (meh (meh)))").asList(), ["meh", ["meh", ["meh"]]])


class TestTerm(unittest.TestCase):
    def testTerm(self):
        self.assertEqual(mp.term.parseString("meh (meh)").asList(), ["meh", ["meh"]])


class TestHook(unittest.TestCase):
    def testIDHook(self):
        self.assertEqual(mp.hook.parseString("id-hook meh (meh) (meh)"), ast.IDHook("meh", ["meh", "meh"]))

    def testOPHook(self):
        self.assertEqual(mp.hook.parseString("op-hook meh (meh meh)")[0], ast.OPHook(["meh", "meh"]))

    def testTermHook(self):
        self.assertEqual(mp.hook.parseString("term-hook meh (meh meh)")[0], ast.TermHook(["meh", "meh"]))


class TestAttribute(unittest.TestCase):
    def testAssoc(self):
        self.assertEqual(mp.attr.parseString("[assoc]")[0], ast.MaudeAttribute(ast.AttributeType.assoc))

    def testComm(self):
        self.assertEqual(mp.attr.parseString("[comm]")[0], ast.MaudeAttribute(ast.AttributeType.comm))

    def testCommAssoc(self):
        self.assertEqual(mp.attr.parseString("[comm assoc]").asList(), [ast.MaudeAttribute(ast.AttributeType.comm), ast.MaudeAttribute(ast.AttributeType.assoc)])

    def testCommAssocNoSpace(self):
        self.assert_(failureFun("[commassoc]"))

    def testRightID(self):
        self.assertEqual(mp.attr.parseString("[right id: meh meh]")[0], ast.RightID(["meh", "meh"]))

    def testLeftID(self):
        self.assertEqual(mp.attr.parseString("[left id: meh meh]")[0], ast.LeftID(["meh", "meh"]))

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
        self.assertEqual(mp.attr.parseString("[format (meh)]")[0], ast.Format("meh"))

    def testSpecial(self):
        self.assertEqual(mp.attr.parseString("[special (id-hook meh meh)]")[0], ast.Special(ast.IDHook("meh", 1)))

if __name__ == '__main__':
    unittest.main()

