from .tree import ConditionNode, WhileNode, RootNode, IdentifierNode, NumberNode, OperatorNode, BinaryOpNode, AssignmentNode, PrintNode, Tree
from ..token import TokenSymbol, Token

import copy

def token_is_operator(token):
    return token.symbol in TokenSymbol.OPERATOR

class ParseState:
    def __init__(self, tokens):
        self.tokens = tokens
        if len(self.tokens) > 0:
            self.current_token = self.tokens[0]
        else:
            self.current_token = Token(TokenSymbol.DIVERSE.EOF, "")

def parse_pop_first_token(parse_state):
    item = parse_state.current_token
    return item, ParseState(parse_state.tokens[1:])

def factor(parse_state):
    """
    factor : INTEGER
    """

    if parse_state.current_token.symbol == TokenSymbol.CONSTANT.INTEGER:
        token, parse_state = parse_pop_first_token(parse_state)
        return NumberNode(token.value), parse_state
    
    if parse_state.current_token.symbol == TokenSymbol.DIVERSE.IDENTIFIER:
        token, parse_state = parse_pop_first_token(parse_state)
        return IdentifierNode(token.value), parse_state
    
    return None, parse_state

def term_check_multiply_or_devide(parse_state, root):
    if parse_state.current_token.symbol not in (TokenSymbol.OPERATOR.MATH.MULTIPLY, TokenSymbol.OPERATOR.MATH.DEVIDE):
        return root, parse_state
    
    token, parse_state = parse_pop_first_token(parse_state)
    right_node, parse_state = factor(parse_state)
    node = BinaryOpNode(left=root, operator=OperatorNode(token.value), right=right_node)
    return term_check_multiply_or_devide(parse_state, node)

def term(parse_state):
    """
    term   : factor ((MUL | DIV) factor)*
    """

    node, parse_state = factor(parse_state)
    
    return term_check_multiply_or_devide(parse_state, node)

def expr_check_plus_or_minus(parse_state, root):
    if parse_state.current_token.symbol not in (TokenSymbol.OPERATOR.MATH.PLUS, TokenSymbol.OPERATOR.MATH.MIN):
        return root, parse_state
    
    token, parse_state = parse_pop_first_token(parse_state)
    right_node, parse_state = term(parse_state)
    node = BinaryOpNode(left=root, operator=OperatorNode(token.value), right=right_node)
    return expr_check_plus_or_minus(parse_state, node)

def expr(parse_state, initial_term=None):
    """
    expr   : term ((PLUS | MINUS) term)*
    term   : factor ((MUL | DIV) factor)*
    factor : INTEGER | IDENTIFIER
    """
    if initial_term == None:
        node, parse_state = term(parse_state)
    else:
        node = initial_term

    return expr_check_plus_or_minus(parse_state, node)

def parse_condition(parse_state, root_node, condition_node_type) -> None:
    
    token, parse_state = parse_pop_first_token(parse_state)
    if token.symbol != TokenSymbol.CONTROL.LPARAN:
        print("LPARAN expected got:", token)
        return None, parse_state

    condition_node, parse_state = parsing(parse_state)
    
    token, parse_state = parse_pop_first_token(parse_state)
    if token.symbol != TokenSymbol.CONTROL.RPARAN:
        print("RPARAN expected got:", token)
        return None, parse_state

    token, parse_state = parse_pop_first_token(parse_state)
    if token.symbol != TokenSymbol.CONTROL.LBRACE:
        print("LBRACE expected got:", token)
        return None, parse_state
    
    execute_node, parse_state = create_root_node(parse_state)
    node = condition_node_type(condition_node, execute_node)

    token, parse_state = parse_pop_first_token(parse_state)
    if token.symbol != TokenSymbol.CONTROL.RBRACE:
        print("RBRACE expected got:", token)
        return None, parse_state
    
    return node, parse_state
    
def parsing(parse_state, root=None):
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
        return parse_condition(parse_state, root, ConditionNode)

    elif parse_state.current_token.symbol == TokenSymbol.CONTROL.WHILE:
        token, parse_state = parse_pop_first_token(parse_state)
        return parse_condition(parse_state, root, WhileNode)

    elif parse_state.current_token.symbol in TokenSymbol.OPERATOR.MATH:
        return expr(parse_state, root)
    
    elif parse_state.current_token.symbol == TokenSymbol.DIVERSE.ENDOFSTATEMENT:
        return root, parse_state

    return root, parse_state

def create_root_node(parse_state, nodes=[]):
    if parse_state.current_token.symbol in (TokenSymbol.DIVERSE.EOF, TokenSymbol.CONTROL.RBRACE):
        return RootNode(nodes), parse_state

    node, parse_state = parsing(parse_state)
    
    if parse_state.current_token.symbol == TokenSymbol.DIVERSE.ENDOFSTATEMENT:
        token, parse_state = parse_pop_first_token(parse_state)

    return create_root_node(parse_state, nodes + [node])

def create_ast(parse_state):
    if len(parse_state.tokens) == 0 or parse_state.current_token == Token.Diverse.EOF:
        return Tree(root_node)

def create_ast(tokens):
    parse_state = ParseState(tokens)
    root_node, parse_state = create_root_node(parse_state)
    tree = Tree(root_node)
    return tree