from ..token import TokenSymbol
from ..parser.tree import RootNode, ConditionNode, WhileNode, BinaryOpNode, AssignmentNode, IdentifierNode, NumberNode, PrintNode, TreeNode, Tree

from typing import Union, Tuple, Callable, List
import copy

class ProgramState:
    def __init__(self):
        self.variables = dict()
    
    def __str__(self) -> str:
        return str(self.variables)

def program_state_decorator(f: Callable[[ProgramState, TreeNode], any], program_state: ProgramState, node: TreeNode):
    output = f(program_state, node)
    if type(output) != tuple:
        return output, program_state

    return output

def visit_root_nodes(program_state: ProgramState, nodes: List[TreeNode]) -> Tuple[None, ProgramState]:
    if len(nodes) == 0:
        return None, program_state
    
    head, *tail = nodes
    node_output, program_state = visit_node(program_state, head)
    return visit_root_nodes(program_state, tail)

def visit_root_node(program_state: ProgramState, root_node: RootNode):
    return visit_root_nodes(program_state, root_node.nodes)
    
def get_operator_func(binary_operator_node: BinaryOpNode) -> Union[None, Callable[[any, any], any]]:
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
    
    operator_funcs = list(filter(lambda x: binary_operator_node.operator.value == x[0], operator_function_combinations))
    if len(operator_funcs) == 1:
        operator_func = operator_funcs[0][1]
        return operator_func
    
    return None

def visit_binary_operator(program_state: ProgramState, binary_operator_node: BinaryOpNode) -> any:
    func = get_operator_func(binary_operator_node)
    output_left, program_state_left = visit_node(program_state, binary_operator_node.left)
    output_right, program_state_right = visit_node(program_state, binary_operator_node.right)
    return func(output_left, output_right)

def visit_assignment_node(program_state: ProgramState, assignment_node: AssignmentNode) -> Tuple[None, ProgramState]:
    new_program_state = copy.deepcopy(program_state)
    node_output, program_state = visit_node(program_state, assignment_node.right)
    new_program_state.variables[assignment_node.left.value] = node_output
    return None, new_program_state

def visit_identifier_node(program_state: ProgramState, identifier_node: IdentifierNode) -> Union[None, any]:
    if identifier_node.value in program_state.variables.keys():
        return program_state.variables[identifier_node.value]
    
    return None

def visit_print_node(program_state: ProgramState, print_node: PrintNode) -> Tuple[None, ProgramState]:
    output, program_state = visit_node(program_state, print_node.print_node)
    print("interpreter:", output)
    return None, program_state

def visit_condition_node(program_state: ProgramState, condition_node: ConditionNode) -> Tuple[any, ProgramState]:
    output, program_state = visit_node(program_state, condition_node.condition_node)
    if output == False:
        return output, program_state
    
    return visit_node(program_state, condition_node.execute_node)

def visit_while_node(program_state: ProgramState, while_node: WhileNode) -> Tuple[any, ProgramState]:
    output, program_state = visit_node(program_state, while_node.condition_node)
    if output == False:
        return output, program_state
    
    output, program_state = visit_node(program_state, while_node.execute_node)
    visit_while_node(program_state, while_node)
    

def visit_node(program_state: ProgramState, node: TreeNode) -> Union[None, Tuple[any, ProgramState]]:
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
    
    return None

def interpret(ast: Tree) -> ProgramState:
    program_state = ProgramState()
    result, program_state = visit_node(program_state, ast.root_node)
    return program_state