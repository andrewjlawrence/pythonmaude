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


class TestAttribute(unittest.TestCase):
    def testAssoc(self):
        print(mp.attr.parseString("[assoc]")[0])
        self.assertEqual(mp.attr.parseString("[assoc]")[0], ast.MaudeAttribute(ast.AttributeType.assoc))

    def testComm(self):
        self.assertEqual(mp.attr.parseString("[comm]")[0], ast.MaudeAttribute(ast.AttributeType.comm))

    def testCommAssoc(self):
        self.assertEqual(mp.attr.parseString("[comm assoc]").asList(), [ast.MaudeAttribute(ast.AttributeType.comm), ast.MaudeAttribute(ast.AttributeType.assoc)])

    def testCommAssocNoSpace(self):
        self.assert_(failureFun("[commassoc]"))


if __name__ == '__main__':
    unittest.main()

