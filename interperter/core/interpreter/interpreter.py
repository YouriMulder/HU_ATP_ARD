from ..token import TokenSymbol
from ..parser.tree import BinaryOpNode, AssignmentNode, IdentifierNode, NumberNode

class ProgramState:
    def __init__(self):
        self.variables = dict()
    
    def __str__(self):
        return str(self.variables)

def get_operator_func(node):
    operator_function_combinations = [
        ("+", lambda x,y: x + y),
        ("-", lambda x,y: x - y),
        ("*", lambda x,y: x * y),
        ("/", lambda x,y: x / y),
    ]

    operator_funcs = list(filter(lambda x: node.operator.value == x[0], operator_function_combinations))
    
    if len(operator_funcs) == 1:
        operator_func = operator_funcs[0][1]
        return operator_func
    if len(operator_funcs) > 1:
        for operator_func in operator_funcs:
            print(operator_func)

def visit_binary_operator(program_state, node):
    func = get_operator_func(node)
    return func(node_visit(program_state, node.left), node_visit(program_state, node.right))

def visit_assignment_node(program_state, node):
    new_program_state = program_state
    new_program_state.variables[node.left.value] = node_visit(program_state, node.right)
    return new_program_state

def visit_identifier_node(program_state, node):
    return program_state.variables[node.value]

def node_visit(program_state, node):
    node_function_combinations = [
        (AssignmentNode, visit_assignment_node),
        (BinaryOpNode, visit_binary_operator),
        (NumberNode, lambda program_state, node: node.value),
        (IdentifierNode, visit_identifier_node)
    ]

    node_funcs = list(filter(lambda x: type(node) == x[0], node_function_combinations))

    if len(node_funcs) == 1:
        node_visit_func = node_funcs[0][1]
        return node_visit_func(program_state, node)
    
    if len(node_funcs) > 1:
        for node_func in node_funcs:
            print(node_func)

    return "node visit error"

def interpret(ast):
    program_state = ProgramState()
    for node in ast.root:
        result = node_visit(program_state, node)
    return result