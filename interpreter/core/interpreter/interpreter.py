from ..token import TokenSymbol
from ..parser.tree import RootNode, ConditionNode, WhileNode, BinaryOpNode, AssignmentNode, IdentifierNode, NumberNode, PrintNode, TreeNode, Tree

from typing import Union, Tuple, Callable, List
import copy


class ProgramState:
    def __init__(self):
        self.variables = dict()

    def __str__(self) -> str:
        return str(self.variables)


def program_state_decorator(f: Callable[[ProgramState, TreeNode], any]) -> Tuple[any, ProgramState]:
    """
    program_state_decorator :: (ProgramState -> TreeNode -> Any) -> (Any, ProgramState)
    @brief Decorator used to return the previous if none is provided.
    @param f The function you want to put the decorator use the decorator on.
    @return A tuple containig the output and the ProgramState
    """
    
    def argument_wrapper(program_state: ProgramState, node: TreeNode):
        output = f(program_state, node)
        
        if type(output) != tuple:
            return output, program_state

        return output
    
    return argument_wrapper


def visit_root_node(program_state: ProgramState, root_node: RootNode) -> Tuple[None, ProgramState]:
    """
    visit_root_node -> ProgramState -> RootNode -> (None -> ProgramState)
    @brief Function used to visit the a RootNode.
    @details
        This function is a wrapper for visit_root_nodes.
    @return The output of visit_root_nodes()
    """
    
    def visit_root_nodes(program_state: ProgramState, nodes: List[TreeNode]) -> Tuple[None, ProgramState]:
        """
        visit_root_nodes -> ProgramState -> [TreeNode] -> (None -> ProgramState)
        @brief Function used to visit the a RootNode.
        @details
            This function is a wrapper for visit_root_nodes.
        @return The output of visit_root_nodes()
        """
        
        if len(nodes) == 0:
            return None, program_state

        head, *tail = nodes
        node_output, program_state = visit_node(program_state, head)
        return visit_root_nodes(program_state, tail)


    return visit_root_nodes(program_state, root_node.nodes)


def get_operator_func(binary_operator_node: BinaryOpNode) -> Union[None, Callable[[any, any], any]]:
    """
    get_operator_func -> BinaryOpNode -> Maybe (Any -> Any -> Any)
    @brief function used to get the operator function of a BinaryOpNode.
    @param binary_operator_node the BinaryOpNode you want to get the operator function of.
    @return None or the operator function. 
    """
    
    operator_function_combinations = [
        ("+", lambda x, y: x + y),
        ("-", lambda x, y: x - y),
        ("*", lambda x, y: x * y),
        ("/", lambda x, y: x / y),

        (":==", lambda x, y: x == y),
        (":<", lambda x, y: x < y),
        (":<=", lambda x, y: x <= y),
        (":>", lambda x, y: x > y),
        (":>=", lambda x, y: x >= y),
    ]

    operator_funcs = list(filter(
        lambda x: binary_operator_node.operator.value == x[0], operator_function_combinations))
    if len(operator_funcs) == 1:
        operator_func = operator_funcs[0][1]
        return operator_func

    return None


def visit_binary_operator_node(program_state: ProgramState, binary_operator_node: BinaryOpNode) -> any:
    """
    visit_binary_operator_node -> ProgramState -> BinaryOpNode -> Any
    @brief function used to visit a BinaryOpNode.
    @details
        The output of the right and left node are put in the operator_function.
        The opartor function is determined using get_operator_func().
    @param program_state The current state of the program.
    @param binary_operator_node the BinaryOpNode you want to visit.
    @return The output of the operator function and the new ProgramState. 
    """

    operator_func = get_operator_func(binary_operator_node)
    output_left, program_state_left = visit_node(
        program_state, binary_operator_node.left)
    output_right, program_state_right = visit_node(
        program_state_left, binary_operator_node.right)
    return operator_func(output_left, output_right), program_state_right


def visit_assignment_node(program_state: ProgramState, assignment_node: AssignmentNode) -> Tuple[None, ProgramState]:
    """
    visit_assignment_node -> ProgramState -> AssignmentNode -> Maybe ProgramState
    @brief function used to visit an AssignmentNode.
    @details
        The right node's output of the  is assigned to the left node.
    @param program_state The current state of the program.
    @param assignment_node the AssignmentNode you want to visit.
    @return None and the new ProgramState. 
    """
    
    new_program_state = copy.deepcopy(program_state)
    node_output, program_state = visit_node(
        program_state, assignment_node.right)
    new_program_state.variables[assignment_node.left.value] = node_output
    return None, new_program_state


def visit_identifier_node(program_state: ProgramState, identifier_node: IdentifierNode) -> Union[None, any]:
    """
    visit_identifier_node -> ProgramState -> IdentifierNode -> Maybe Any
    @brief function used to visit an IdentifierNode.
    @param program_state The current state of the program.
    @param identifier_node the IdentifierNode you want to visit.
    @return The value of the identifier. 
    """
    
    if identifier_node.value in program_state.variables.keys():
        return program_state.variables[identifier_node.value]
    
    return None


def visit_print_node(program_state: ProgramState, print_node: PrintNode) -> Tuple[None, ProgramState]:
    """
    visit_print_node -> ProgramState -> PrintNode -> (None, ProgramState)
    @brief function used to visit a PrintNode.    
    @param program_state The current state of the program.
    @param print_node the PrintNode you want to visit.
    @warning 
        This function has side effects.
        This function is not conform the functional programming principles.
    @return None and the new ProgramState. 
    """
    
    output, program_state = visit_node(program_state, print_node.print_node)
    print("interpreter:", output)
    return None, program_state


def visit_condition_node(program_state: ProgramState, condition_node: ConditionNode) -> Tuple[any, ProgramState]:
    """
    visit_condition_node -> ProgramState -> ConditionNode -> (Any, ProgramState)
    @brief function used to visit a ConditionNode.
    @details
        If the condition of the ConditionNode 
        is True the function executes 
        the execute_node in the ConditionNode.
        
    @param program_state The current state of the program.
    @param condition_node the ConditionNode you want to visit.
    @return The output after the condition or the execution. 
    """
    
    output, program_state = visit_node(
        program_state, condition_node.condition_node)
    if output == False:
        return output, program_state

    return visit_node(program_state, condition_node.execute_node)


def visit_while_node(program_state: ProgramState, while_node: WhileNode) -> Tuple[any, ProgramState]:
    """
    visit_while_node -> ProgramState -> WhileNode -> (Any, ProgramState)
    @brief function used to visit a WhileNode.
    @param program_state The current state of the program.
    @param while_node the WhileNode you want to visit.
    @return The output of the last visit and the new ProgramState. 
    """

    output, program_state = visit_node(
        program_state, while_node.condition_node)
    if output == False:
        return output, program_state

    output, program_state = visit_node(program_state, while_node.execute_node)
    return visit_while_node(program_state, while_node)

@program_state_decorator
def visit_node(program_state: ProgramState, node: TreeNode) -> Union[None, Tuple[any, ProgramState]]:
    """
    visit_node -> ProgramState -> TreeNode -> Maybe (Any, ProgramState)
    @brief function used to visit a node in the tree.
    @param program_state The current state of the program.
    @param node A TreeNode you want to visit.
    @return None or the output of the node visit and the new ProgramState. 
    """
    
    node_function_combinations = [
        (RootNode, visit_root_node),
        (AssignmentNode, visit_assignment_node),
        (BinaryOpNode, visit_binary_operator_node),
        (NumberNode, lambda program_state, node: node.value),
        (IdentifierNode, visit_identifier_node),
        (PrintNode, visit_print_node),
        (ConditionNode, visit_condition_node),
        (WhileNode, visit_while_node),
    ]
    node_funcs = list(filter(lambda x: type(node) ==
                             x[0], node_function_combinations))
    if len(node_funcs) == 1:
        visit_node_func = node_funcs[0][1]
        return visit_node_func(program_state, node)

    return None


def interpret(ast: Tree) -> ProgramState:
    """
    interpret :: Tree -> ProgramState
    @brief This function interprets the abstact syntax tree.
    @details
        The function visits the root node of the abstract syntax tree
    @param ast The abstract syntax tree you want to interpret
    @return The program state after interpreting the ast.
    """
    program_state = ProgramState()
    result, program_state = visit_node(program_state, ast.root_node)
    return program_state
