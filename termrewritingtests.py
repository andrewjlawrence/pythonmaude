import unittest
import termrewriting


class VariableNameTestCase(unittest.TestCase):
    def test_construction(self):
        vname = termrewriting.VName("term1", 1)
        self.assertEqual(vname.index, 1)
        self.assertEqual(vname.name, "term1")


class TermTestCase(unittest.TestCase):
    def test_vtermconstruction(self):
        vterm = termrewriting.VTerm(termrewriting.VName("term1", 1))
        self.assertEqual(vterm.vname.index, 1)
        self.assertEqual(vterm.vname.name, "term1")

    def test_ttermconstruction(self):
        tterm = termrewriting.TTerm("Cat", list())
        self.assertEqual(tterm.term, "Cat")


if __name__ == '__main__':
    unittest.main()
