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

class SubstTestCase(unittest.TestCase):
    def test_substconstruction(self):
        subst = termrewriting.Substitution()

    def test_substindomain(self):
        subst = termrewriting.Substitution()
        rterm = termrewriting.VTerm(termrewriting.VName("range term", 1))
        dvarname = termrewriting.VName("domain varname", 1)
        subst.add_mapping(dvarname, rterm)
        self.assertTrue(subst.indom(termrewriting.VName("domain varname", 1)))

    def test_application(self):
        subst = termrewriting.Substitution()
        rterm = termrewriting.VTerm(termrewriting.VName("range term", 1))
        dvarname = termrewriting.VName("domain varname", 1)
        subst.add_mapping(dvarname, rterm)
        lterm  = termrewriting.VTerm(dvarname)
        appresult = subst.app(lterm)
        self.assertEqual(rterm, appresult)

    def test_lift_vterm(self):
        # Lifting a variable term is the same as performing a
        # simple application
        subst = termrewriting.Substitution()
        rterm = termrewriting.VTerm(termrewriting.VName("range term", 1))
        dvarname = termrewriting.VName("domain varname", 1)
        subst.add_mapping(dvarname, rterm)
        lterm  = termrewriting.VTerm(dvarname)
        appresult = subst.lift(lterm)
        self.assertEqual(rterm, appresult)

    def test_lift_tterm(self):
        # Lifting a variable term is the same as performing a
        # simple application
        subst = termrewriting.Substitution()
        rterm1 = termrewriting.VTerm(termrewriting.VName("range term", 1))
        rterm = termrewriting.TTerm("rterm name", [rterm1])
        dvarname = termrewriting.VName("domain varname", 1)
        subst.add_mapping(dvarname, rterm)
        lterm  = termrewriting.TTerm("catterm", [termrewriting.VTerm(dvarname)])
        appresult = subst.lift(lterm)
        self.assertEqual(rterm, appresult)


if __name__ == '__main__':
    unittest.main()
