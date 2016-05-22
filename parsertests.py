# Copyright 2016 Andrew Lawrence
import parser
import pyparsing
import ast
import unittest

def failureFun(string):
    result = False
    try:
        meh = parser.systemcommand.parseString(string)
    except pyparsing.ParseException:
        result = True
    return result

class TestSystemCommands(unittest.TestCase):
    def testInCommand(self):
        self.assertEqual(parser.systemcommand.parseString("in meh")[0], ast.InCommand("meh"))
    def testInCommandFailure(self):
        self.assert_(failureFun("inmeh"))
    def testLoadCommand(self):
        self.assertEqual(parser.systemcommand.parseString("load meh")[0], ast.LoadCommand("meh"))
    def testLoadCommandFailure(self):
        self.assert_(failureFun("loadmeh"))
    def testQuitCommnad(self):
        self.assertEqual(parser.systemcommand.parseString("quit")[0], ast.QuitCommand())
    def testEofCommand(self):
        self.assertEqual(parser.systemcommand.parseString("eof")[0], ast.EofCommand())
    def testPopDCommand(self):
        self.assertEqual(parser.systemcommand.parseString("popd")[0], ast.PopDCommand())
    def testPwdCommand(self):
        self.assertEqual(parser.systemcommand.parseString("pwd")[0], ast.PwdCommand())
    def testCDCommand(self):
        self.assertEqual(parser.systemcommand.parseString("cd meh")[0], ast.CdCommand("meh"))
    def testPushCommand(self):
        self.assertEqual(parser.systemcommand.parseString("push meh")[0], ast.PushCommand("meh"))
    def testLsCommand(self):
        self.assertEqual(parser.systemcommand.parseString("ls")[0], ast.LsCommand(""))
    def testLsCommand2(self):
        self.assertEqual(parser.systemcommand.parseString("ls meh")[0], ast.LsCommand("meh"))
    def testCommandFailure(self):
        self.assert_(failureFun("meh"))

if __name__ == '__main__':
    unittest.main()

