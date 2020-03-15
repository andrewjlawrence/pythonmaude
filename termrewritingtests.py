import unittest
import termrewriting
from termrewriting import TTerm,VTerm,VName

class VariableNameTestCase(unittest.TestCase):
    def test_construction(self):
        vname = VName("term1", 1)
        self.assertEqual(vname.index, 1)
        self.assertEqual(vname.name, "term1")


class TermTestCase(unittest.TestCase):
    def test_vtermconstruction(self):
        vterm = VTerm(VName("term1", 1))
        self.assertEqual(vterm.vname.index, 1)
        self.assertEqual(vterm.vname.name, "term1")

    def test_ttermconstruction(self):
        tterm = TTerm("Cat", list())
        self.assertEqual(tterm.term, "Cat")

class SubstTestCase(unittest.TestCase):
    def test_substconstruction(self):
        subst = termrewriting.Substitution()

    def test_substindomain(self):
        subst = termrewriting.Substitution()
        rterm = VTerm(VName("range term", 1))
        dvarname = VName("domain varname", 1)
        subst.add_mapping(dvarname, rterm)
        self.assertTrue(subst.indom(VName("domain varname", 1)))

    def test_application(self):
        subst = termrewriting.Substitution()
        rterm = VTerm(VName("range term", 1))
        dvarname = VName("domain varname", 1)
        subst.add_mapping(dvarname, rterm)
        lterm  = VTerm(dvarname)
        appresult = subst.app(lterm)
        self.assertEqual(rterm, appresult)

    def test_lift_vterm(self):
        # Lifting a variable term is the same as performing a
        # simple application
        subst = termrewriting.Substitution()
        rterm = VTerm(VName("range term", 1))
        dvarname = VName("domain varname", 1)
        subst.add_mapping(dvarname, rterm)
        lterm  = VTerm(dvarname)
        appresult = subst.lift(lterm)
        self.assertEqual(rterm, appresult)

    def test_lift_tterm(self):
        # Lifting a variable term is the same as performing a
        # simple application
        subst = termrewriting.Substitution()
        rterm1 = VTerm(termrewriting.VName("range term", 1))
        rterm = TTerm("rterm name", [rterm1])
        dvarname = VName("domain varname", 1)
        subst.add_mapping(dvarname, rterm)
        lterm  = TTerm("lterm name", [VTerm(dvarname)])
        appresult = subst.lift(lterm)
        self.assertEqual(TTerm("lterm name",[rterm]), appresult)


# f(x,y) =? f(g(cz), cx)
# results in a substitution [x -> g(cz), y -> cx]
class UnifyTestCase(unittest.TestCase):

    def test_unify(self):
        xt = VTerm(VName("x",1))
        yt = VTerm(VName("y",1))
        ft1 = TTerm("f", [xt, yt])

        cz = TTerm("cz", [])
        gt = TTerm("g", [cz])
        cx = TTerm("cx", [])
        ft2 = TTerm("f",[gt, cx])

        subst = termrewriting.unify(ft1, ft2)
        print(subst)
        self.assertEqual(len(subst) , 2)
        self.assertEqual(subst.app(xt), gt)
        self.assertEqual(subst.app(yt), cx)

if __name__ == '__main__':
    unittest.main()
