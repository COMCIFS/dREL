# pytest will run this file automatically.
# Test the autogenerated dREL parser against various dREL
# fragments.

import pytest
from lark import Lark
from CifFile import CifDic, CifFile
from py_transformer import TreeToPy, CategoryObject, Packet
import re

# Constants
grammar_file = "lark_grammar.ebnf"
dic_file = "/home/jrh/COMCIFS/cif_core/cif_core.dic"

frag_collection = {}

frag_collection["assign"] = "_a = 0"
frag_collection["brackets"] = """With c as cell
 
    return.value = Acosd(
    (Cosd(c.angle_beta)*Cosd(c.angle_gamma)-Cosd(c.angle_alpha))/(Sind(c.angle_beta)*Sind(c.angle_gamma)))"""

frag_collection["matrix"] = """
          a = 11 b = 12 c = -5.4
          return.val =  [[a,b,c],
                                               [1,2,3],
                                               ['a','b','c']]
"""
frag_collection["simple_index"] = """
    c = [1,2,3,4]
    return.val  =  c[0]+ c[3]
                       
"""
frag_collection["call_suite"] = """
   If(setting == 'triclinic') {
      If( Abs(a-b)<d || Abs(a-c)<d || Abs(b-c)<d )          Alert('B', warn_len)
      If( Abs(alp-90)<d || Abs(bet-90)<d || Abs(gam-90)<d ) Alert('B', warn_ang)
      }
"""
# 
@pytest.fixture
def lark_grammar(request,scope="module"):
    grammar_file = getattr(request.module,"grammar_file")
    grammar = open(grammar_file).read()
    parser = Lark(grammar,start="input",parser="lalr",lexer="contextual")
    return parser

@pytest.fixture
def load_cifdic(request,scope="module"):
    cifdic = getattr(request.module,"dic_file")
    return CifDic(cifdic,do_minimum=True)

@pytest.fixture
def drel_methods(request,scope="module"):
    p = load_cifdic(request, scope)
    has_meth = list([n for n in p.keys() if '_method.expression' in p[n]])
    has_meth.sort()
    return [(n,p[n]['_method.expression']) for n in has_meth]

@pytest.fixture
def pytransformer(request,scope="module"):
    tt = TreeToPy("return","val",{},None)
    return tt

@pytest.fixture
def getdata(request,scope="module"):
    d = CifFile("nick1.cif",grammar="STAR2")
    return d.first_block()

def process_a_phrase(phrase,parser,transformer=None):
    print("========")
    print(phrase)
    print("Tokens:")
    tokens = parser.lex(phrase)
    for t in tokens:
        print(repr(t))
    tree = parser.parse(phrase,debug=False)
    print(tree.pretty())
    if transformer is not None:
        return transformer.transform(tree)
    
def handle_a_phrase(*args,**kwargs):
    x = process_a_phrase(*args,**kwargs)
    print(x)
    return x
    
def execute_a_phrase(phrase,parser,transformer):
    """Execute the provided phrase and return the result"""
    x = handle_a_phrase(phrase,parser,transformer)
    test_code = "def myfunc():\n    " + re.sub(r"\n","\n    ",x)
    test_code = test_code + "\n"+4*' '+"return _dreltarget"
    print(test_code)
    exec(test_code,globals())
    p = myfunc()
    return p

class TestGrammar(object):
    def test_sum(self,lark_grammar,pytransformer):
        v = execute_a_phrase("return.val=1+2",lark_grammar,pytransformer)
        assert v == 3

    def test_list(self,lark_grammar,pytransformer):
        v = execute_a_phrase("c=[1,2,3,4] return.val=c[0]+c[2]",lark_grammar,pytransformer)
        assert v == 4

    def test_matrix(self,lark_grammar,pytransformer):
        v = execute_a_phrase(frag_collection["matrix"],lark_grammar,pytransformer)
        assert v[0][1] == 12

    def test_brackets(self,lark_grammar,pytransformer):
        handle_a_phrase(frag_collection["brackets"],lark_grammar,pytransformer)

    def test_assign(self,lark_grammar,pytransformer):
        handle_a_phrase(frag_collection["assign"],lark_grammar,pytransformer)

    def test_small_stmt(self,lark_grammar,pytransformer):
        """Test that a small statement after an IF statement is
        considered to be a suite"""
        handle_a_phrase(frag_collection["call_suite"],lark_grammar)

    def test_subs(self,lark_grammar,pytransformer):
        handle_a_phrase("c[0]",lark_grammar,pytransformer)

class TestHelpers(object):
    """Test extra objects"""
    def test_catobj(self,load_cifdic,getdata):
        c = CategoryObject(getdata,"atom_site",load_cifdic)
        print(str(c))
        assert c[{'':'o3'}].fract_x == '.2501(5)'

    def test_iteration(self,load_cifdic,getdata):
        c = CategoryObject(getdata,"atom_site",load_cifdic)
        vals = set([c.fract_y for c in c])
        assert set(getdata['_atom_site.fract_y']) == vals
        
    def test_packet(self,load_cifdic,getdata):
        af = lambda s:s
        p = Packet(af)
        assert p.stuff == "stuff"

    def test_multi_key(self,load_cifdic,getdata):
        """Test categories with more than one key data name"""
        c = CategoryObject(getdata,"geom_bond",load_cifdic)
        assert c[{'atom_site_label_1':'C1A',
                  'atom_site_label_2':'C10A',
                  'site_symmetry_1':'.',
                  'site_symmetry_2':'.'}].distance == '1.555(4)'

    def test_multi_iter(self,load_cifdic,getdata):
        """Test iterating categories with more than one key data name"""
        c = CategoryObject(getdata,"geom_bond",load_cifdic)
        vals = set([c.distance for c in c])
        assert set(getdata['_geom_bond.distance']) == vals
        
    def test_non_loop(self,load_cifdic,getdata):
        """Test that attributes for non-looped categories also work"""
        c = CategoryObject(getdata,"cell",load_cifdic)
        assert c.angle_beta == '90.8331(5)'

class DicTests(object):
    def test_dic_entries(drel_methods,lark_grammar):
        for mn,(name,one_m) in enumerate(drel_methods):
            for n,om in enumerate(one_m):   #multiple methods possible
                print("=== %s(%d) ===" % (name,mn))
                print(om)
                tokens = lark_grammar.lex(om+"\n")
                for t in tokens:
                    print(repr(t))
                tree = lark_grammar.parse(om+"\n")
                print(tree.pretty())
