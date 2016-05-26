# Copyright 2016 Andrew Lawrence
import pyparsing
from maudeparser import systemcommand
import ast
import unittest

def failureFun(string):
    result = False
    try:
        meh = systemcommand.parseString(string)
    except pyparsing.ParseException:
        result = True
    return result

class TestSystemCommands(unittest.TestCase):
    def testInCommand(self):
        self.assertEqual(systemcommand.parseString("in meh")[0], ast.InCommand("meh"))
    def testInCommandFailure(self):
        self.assert_(failureFun("inmeh"))
    def testLoadCommand(self):
        self.assertEqual(systemcommand.parseString("load meh")[0], ast.LoadCommand("meh"))
    def testLoadCommandFailure(self):
        self.assert_(failureFun("loadmeh"))
    def testQuitCommnad(self):
        self.assertEqual(systemcommand.parseString("quit")[0], ast.QuitCommand())
    def testEofCommand(self):
        self.assertEqual(systemcommand.parseString("eof")[0], ast.EofCommand())
    def testPopDCommand(self):
        self.assertEqual(systemcommand.parseString("popd")[0], ast.PopDCommand())
    def testPwdCommand(self):
        self.assertEqual(systemcommand.parseString("pwd")[0], ast.PwdCommand())
    def testCDCommand(self):
        self.assertEqual(systemcommand.parseString("cd meh")[0], ast.CdCommand("meh"))
    def testPushCommand(self):
        self.assertEqual(systemcommand.parseString("push meh")[0], ast.PushCommand("meh"))
    def testLsCommand(self):
        self.assertEqual(systemcommand.parseString("ls")[0], ast.LsCommand(""))
    def testLsCommand2(self):
        self.assertEqual(systemcommand.parseString("ls meh")[0], ast.LsCommand("meh"))
    def testCommandFailure(self):
        self.assert_(failureFun("meh"))

from maudeparser import attr

class TestAttribute(unittest.TestCase):
    def testAssoc(self):
        self.assertEqual(attr.parseString("[assoc]"), ast.Attribute(ast.AttributeType.assoc))

if __name__ == '__main__':
    unittest.main()

