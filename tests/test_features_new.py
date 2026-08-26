import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bootstrap"))
from lexer.tokenizer import tokenize
from parser.parser import Parser
from compiler.type_checker import TypeInferer
from vm.compiler import Compiler
from vm.machine import VirtualMachine

def run_nv(code: str):
    toks = tokenize(code)
    ast = Parser(toks).parse()
    TypeInferer().infer(ast)
    prog = Compiler().compile(ast)
    vm = VirtualMachine(prog)
    vm.run()
    return vm

def test_byte():
    run_nv("x: byte = 42\nprint(x)")
    run_nv("a: byte = 255\nb: byte = 10\nc = a\nassert = 0\nif c == 255 { print(1) }")

def test_random_deterministic():
    code = """
chacha20_init(1, 2)
a = random()
chacha20_init(1, 2)
b = random()
if a == b { print(1) } else { print(0) }
r = random(5, 10)
if r >= 5 { print(1) }
if r <= 10 { print(1) }
"""
    run_nv(code)

def test_insert_clear():
    code = """
a = [1, 2, 3]
a.insert(1, 99)
if a[1] == 99 { print(1) }
if len(a) == 4 { print(1) }
a.clear()
if len(a) == 0 { print(1) }
"""
    run_nv(code)

def test_sizeof():
    code = """
data Pt { x: int y: int }
print(sizeof(42))
p = Pt()
print(sizeof(p))
"""
    run_nv(code)

def test_class_fields():
    code = """
class Counter {
    val: int
}
c = Counter()
c.val = 5
if c.val == 5 { print(1) }
c.val = c.val + 1
if c.val == 6 { print(1) }
"""
    run_nv(code)

def test_api_stub():
    code = """
print(1)
"""
    run_nv(code)
