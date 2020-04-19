from ..token import TokenSymbol
from ..parser.ast import OperatorNode

def node_visit(node):
    return node.exec()

def visit_bin_op(node):
    return 

def interpret(ast):
    for node in ast.root:
        result = node_visit(node)
    return result