from ..token import TokenSymbol
from ..parser.tree import RootNode, ConditionNode, WhileNode, BinaryOpNode, AssignmentNode, IdentifierNode, NumberNode, PrintNode

class ProgramState:
    def __init__(self):
        self.variables = dict()
    
    def __str__(self):
        return str(self.variables)

def program_state_decorator(f, program_state, node):
    output = f(program_state, node)
    if type(output) == ProgramState:
        return output, output 

    return program_state, output

def visit_root_nodes(program_state, nodes):
    if len(nodes) == 0:
        return program_state, program_state
    
    head, *tail = nodes
    program_state, node_output = visit_node(program_state, head)
    return visit_root_nodes(program_state, tail)

def visit_root_node(program_state, node):
    return visit_root_nodes(program_state, node.nodes)
    
def get_operator_func(node):
    operator_function_combinations = [
        ("+",   lambda x,y: x + y),
        ("-",   lambda x,y: x - y),
        ("*",   lambda x,y: x * y),
        ("/",   lambda x,y: x / y),
        
        (":==", lambda x,y: x == y),
        (":<",  lambda x,y: x < y),
        (":<=", lambda x,y: x <= y),
        (":>",  lambda x,y: x > y),
        (":>=", lambda x,y: x >= y),
        
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
    program_state_left, output_left = visit_node(program_state, node.left)
    program_state_right, output_right = visit_node(program_state, node.right)
    return func(output_left, output_right)

def visit_assignment_node(program_state, node):
    new_program_state = program_state
    program_state, node_output = visit_node(program_state, node.right)
    new_program_state.variables[node.left.value] = node_output
    return new_program_state

def visit_identifier_node(program_state, node):
    return program_state.variables[node.value]

def visit_print_node(program_state, node):
    program_state, output = visit_node(program_state, node.print_node)
    print("interpreter:", output)
    return program_state, None

def visit_condition_node(program_state, node):
    program_state, output = visit_node(program_state, node.condition_node)
    if output == False:
        return program_state, output
    
    return visit_node(program_state, node.execute_node)

def visit_while_node(program_state, node):
    program_state, output = visit_node(program_state, node.condition_node)
    if output == False:
        return program_state, output
    
    program_state, output = visit_node(program_state, node.execute_node)
    visit_while_node(program_state, node)
    

def visit_node(program_state, node):
    node_function_combinations = [
        (RootNode, visit_root_node),
        (AssignmentNode, visit_assignment_node),
        (BinaryOpNode, visit_binary_operator),
        (NumberNode, lambda program_state, node: node.value),
        (IdentifierNode, visit_identifier_node),
        (PrintNode, visit_print_node),
        (ConditionNode, visit_condition_node),
        (WhileNode, visit_while_node),
    ]

    node_funcs = list(filter(lambda x: type(node) == x[0], node_function_combinations))

    if len(node_funcs) == 1:
        visit_node_func = node_funcs[0][1]
        return program_state_decorator(visit_node_func, program_state, node)
    
    if len(node_funcs) > 1:
        for node_func in node_funcs:
            print(node_func)

    return "node visit error"

def interpret(ast):
    program_state = ProgramState()  
    program_state, output = visit_node(program_state, ast.root_node)
    return program_state, output