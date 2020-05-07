from .tree import TreeNode, ConditionNode, WhileNode, RootNode, IdentifierNode, NumberNode, OperatorNode, BinaryOpNode, AssignmentNode, PrintNode, Tree
from ..token import TokenSymbol, Token

from typing import List, Tuple, Union, Callable

import copy


class ParseState:
    """
    @brief This class is used to store the current state when parsing.
    @details The class contains the tokens of the current parsing state
    """
    def __init__(self, tokens: List[Token]):
        """
        @brief Initialises the ParseState object.
        @details
            If the tokens list is empty it is assumed that it is the end of the file.
        @param tokens The tokens in the current ParseState.
        """
        self.tokens = tokens

        if len(self.tokens) > 0:
            self.current_token = self.tokens[0]
        else:
            self.current_token = Token(TokenSymbol.DIVERSE.EOF, "")

    def __str__(self) -> str:
        result = map(lambda token: str(token), self.tokens)
        return '[' + ', '.join(result) + ']'

def parse_pop_first_token(parse_state: ParseState) -> Tuple[Token, ParseState]:
    """
    parse_pop_first_token :: ParseState -> (Token, ParseState)
    @brief This function pops the first token of the ParseState
    @param parse_state The current ParseState of the abstract syntax tree parsing.
    @return A tuple containing the popped token and the new ParseState
    """
    item = parse_state.current_token
    return item, ParseState(parse_state.tokens[1:])


def factor(parse_state: ParseState) -> Tuple[Union[None, TreeNode], ParseState]:
    """
    factor :: ParseState -> (None | TreeNode, ParseState)
    @brief This function creates a factor.
    @details
        factor : INTEGER | IDENTIFIER
        This function creates either a:
        number or 
        identifier node.
        If none of the above is found None is returned
    @param parse_state The current ParseState of the abstract syntax tree parsing.
    @return A tuple containing a (TreeNode or None) and the current ParseState.
    """

    if parse_state.current_token.symbol == TokenSymbol.CONSTANT.INTEGER:
        token, parse_state = parse_pop_first_token(parse_state)
        return NumberNode(token.value), parse_state

    if parse_state.current_token.symbol == TokenSymbol.DIVERSE.IDENTIFIER:
        token, parse_state = parse_pop_first_token(parse_state)
        return IdentifierNode(token.value), parse_state

    return None, parse_state


def term(parse_state: ParseState, root: TreeNode = None) -> Tuple[TreeNode, ParseState]:
    """
    WARINING
    term :: ParseState -> (TreeNode, ParseState)
    @brief This function creates a term
    @details
        term   : factor ((MUL | DIV) factor)*
    @param parse_state The current ParseState of the abstract syntax tree parsing.
    @return Tuple containing a TreeNode with the current found expression and the current ParseState.
    """

    if root == None:
        root, parse_state = factor(parse_state)

    return expr_check_operator(parse_state, root, factor, (TokenSymbol.OPERATOR.MATH.MULTIPLY, TokenSymbol.OPERATOR.MATH.DEVIDE))


def expr_check_operator(parse_state: ParseState, root: TreeNode, further_parse_method: Callable[[ParseState], Tuple[Union[None, TreeNode], ParseState]], check_operators: Tuple[TokenSymbol.OPERATOR]) -> Tuple[TreeNode, ParseState]:
    """
    expr :: ParseState -> TreeNode -> operators -> (TreeNode, ParseState)
    @brief This function creates a binary node if token in check_operators.
    @details
        expr   : term ((PLUS | MINUS) term)*
        This functions checks if the current token is equal to one of the check_operators.
        If this is equal to one of the check_operators the operator is created and returned.
    @param parse_state The current ParseState of the abstract syntax tree parsing.
    @param root A TreeNode containing the current expression.
    @param check_operators The operators which are checked upon.
    @return Tuple containing a TreeNode with the current found expression and the current ParseState.
    """
    
    if parse_state.current_token.symbol not in check_operators:
        return root, parse_state

    token, parse_state = parse_pop_first_token(parse_state)
    right_node, parse_state = further_parse_method(parse_state)
    node = BinaryOpNode(left=root, operator=OperatorNode(
        token.value), right=right_node)
    return expr_check_operator(parse_state, node, further_parse_method, check_operators)


def expr(parse_state: ParseState, initial_term: Union[None, TreeNode] = None) -> Tuple[TreeNode, ParseState]:
    """
    expr :: ParseState -> None | TreeNode -> (TreeNode, ParseState)    
    @brief This function is used to parse an expression.
    @details
        expr : term ((PLUS | MINUS) term)*
    @param parse_state The current ParseState of the abstract syntax tree parsing.
    @param root The initial term found to start the expression with.
    @return A tuple containing the treeNode(expression) and current ParseState.
    """
    node, parse_state = term(parse_state, initial_term)

    return expr_check_operator(parse_state, node, term, (TokenSymbol.OPERATOR.MATH.PLUS, TokenSymbol.OPERATOR.MATH.MIN))
    

def parse_condition(parse_state: ParseState, condition_node_type: type) -> Tuple[Union[None, TreeNode], ParseState]:
    """
    create_ast :: ParseState -> type -> (None|TreeNode, ParseState) 
    @brief Function used to parse a condition node (while, if).
    @param parse_state The current ParseState of the abstract syntax tree parsing.
    @condition_node_type The type of the condition node ConditionNode, WhileNode
    @return A tuple containing the created condition node and the current ParseState. 
    """

    token, parse_state = parse_pop_first_token(parse_state)
    if token.symbol != TokenSymbol.CONTROL.LPARAN:
        return None, parse_state

    condition_node, parse_state = parsing(parse_state)

    token, parse_state = parse_pop_first_token(parse_state)
    if token.symbol != TokenSymbol.CONTROL.RPARAN:
        return None, parse_state

    token, parse_state = parse_pop_first_token(parse_state)
    if token.symbol != TokenSymbol.CONTROL.LBRACE:
        return None, parse_state

    execute_node, parse_state = create_root_node(parse_state)
    node = condition_node_type(condition_node, execute_node)

    token, parse_state = parse_pop_first_token(parse_state)
    if token.symbol != TokenSymbol.CONTROL.RBRACE:
        return None, parse_state

    return node, parse_state

def check_identifier_capital(identifier_value: str, char_should_be_capital: bool = True) -> bool:
    """
    check_identifier_capital :: [a] -> char_should_be_capital -> bool
    @brief This function is used to check if the capitalisation is correct.
    @detail
        The identifier must start with a capital.
        The following characters should be alternating from lower to upper case.
        Any character after a _ or 0-9 must be a capital.
    @param identifier_value The identifier you want to check.
    @param char_should_be_capital Whether the current character should be a capital.
    @return A boolean containing whether the capitalisation is correct.
    """

    if len(identifier_value) == 0:
        return True
    
    head, *tail = identifier_value

    if head == '_' or head.isdigit():
        return check_identifier_capital(tail, True)
    
    if char_should_be_capital != head.isupper():
        return False
    
    return check_identifier_capital(tail, not char_should_be_capital)


def parsing(parse_state: ParseState, root: Union[None, TreeNode] = None) -> Tuple[TreeNode, ParseState]:
    """
    create_ast :: ParseState -> Maybe TreeNode -> (TreeNode, ParseState)
    @brief Function used to parse tokens until end of statement or other end of code block like } or EOF.
    @details
        Function creates a new node using a given token in de parse_state.
        It creates a new node and makes it as a child of the root node.
    @param parse_state The current ParseState of the abstract syntax tree parsing.
    @param root the previous node created used as root for the current node.
    @return A tuple containing the created TreeNode containing his children and the current ParseState. 
    """

    if parse_state.current_token.symbol == TokenSymbol.OPERATOR.ASSIGNMENT.ASSIGNMENT:
        token, parse_state = parse_pop_first_token(parse_state)
        assignment_node, parse_state = parsing(parse_state)
        node = AssignmentNode(root, assignment_node)
        return parsing(parse_state, node)

    elif parse_state.current_token.symbol == TokenSymbol.CONSTANT.INTEGER:
        node, parse_state = expr(parse_state)
        return parsing(parse_state, node)

    elif parse_state.current_token.symbol == TokenSymbol.DIVERSE.IDENTIFIER:
        token, parse_state = parse_pop_first_token(parse_state)
        if not check_identifier_capital(token.value):
            return None, parse_state
        node = IdentifierNode(token.value)    
        return parsing(parse_state, node)

    elif parse_state.current_token.symbol in TokenSymbol.OPERATOR.RELATIONAL:
        token, parse_state = parse_pop_first_token(parse_state)
        expr_node, parse_state = expr(parse_state)
        node = BinaryOpNode(root, OperatorNode(token.value), expr_node)
        return parsing(parse_state, node)

    elif parse_state.current_token.symbol == TokenSymbol.DIVERSE.SHOW:
        token, parse_state = parse_pop_first_token(parse_state)
        print_node_content, parse_state = parsing(parse_state, root)
        return PrintNode(print_node_content), parse_state

    elif parse_state.current_token.symbol == TokenSymbol.CONTROL.IF:
        token, parse_state = parse_pop_first_token(parse_state)
        return parse_condition(parse_state, ConditionNode)

    elif parse_state.current_token.symbol == TokenSymbol.CONTROL.WHILE:
        token, parse_state = parse_pop_first_token(parse_state)
        return parse_condition(parse_state, WhileNode)

    elif parse_state.current_token.symbol in TokenSymbol.OPERATOR.MATH:
        return expr(parse_state, root)

    elif parse_state.current_token.symbol == TokenSymbol.DIVERSE.ENDOFSTATEMENT:
        return root, parse_state

    return root, parse_state


def create_root_node(parse_state: ParseState, child_nodes: List[TreeNode] = []) -> Tuple[RootNode, ParseState]:
    """
    create_ast :: ParseState -> [TreeNode] -> (RootNode, ParseState)
    @brief Function used to create a root node and his children nodes.
    @param parse_state The current ParseState of the abstract syntax tree parsing.
    @param child_nodes All the current child nodes of the root node.
    @return A tuple containing the created root node and the current ParseState. 
    """

    if parse_state.current_token.symbol in (TokenSymbol.DIVERSE.EOF, TokenSymbol.CONTROL.RBRACE):
        return RootNode(child_nodes), parse_state

    node, parse_state = parsing(parse_state)

    if parse_state.current_token.symbol == TokenSymbol.DIVERSE.ENDOFSTATEMENT:
        token, parse_state = parse_pop_first_token(parse_state)

    return create_root_node(parse_state, child_nodes + [node])


def create_ast(tokens: List[Token]) -> Tree:
    """
    create_ast :: [Token] -> Tree
    @brief Function used to create an abstract syntax tree using tokens.
    @param token A list of containing all the tokens to create an ast.
    @return A Tree containing the root node of the abstract syntax tree. 
    """
    parse_state = ParseState(tokens)
    root_node, parse_state = create_root_node(parse_state)
    tree = Tree(root_node)
    return tree
