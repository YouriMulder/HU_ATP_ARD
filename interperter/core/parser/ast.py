from .tree import *

from ..token import TokenSymbol

def token_is_operator(token):
    return token.symbol in TokenSymbol.OPERATOR

def get_operator_from_token(token):
    operator_combinations = [
        (TokenSymbol.OPERATOR.PLUS,      lambda x,y: x + y),
        (TokenSymbol.OPERATOR.MIN,       lambda x,y: x - y),
        (TokenSymbol.OPERATOR.DEVIDE,    lambda x,y: x / y),
        (TokenSymbol.OPERATOR.MULTIPLY,  lambda x,y: x * y),
    ]
    
    filtered_token_operators = list(filter(lambda x: token.symbol == x[0], operator_combinations))
    if len(filtered_token_operators) > 1:
        # filtered multiple tokens
        pass
    
    operator_token = filtered_token_operators[0]
    return OperatorNode(operator_token[1])

class ParseState:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = self.tokens[0]

    def pop_front(self):
        item = self.tokens.pop(0)
        if len(self.tokens) > 0:
            self.current_token = self.tokens[0]
        return item

def factor(parse_state):
    """
    factor : INTEGER | LPAREN expr RPAREN
    """

    if parse_state.current_token.symbol == TokenSymbol.DIVERSE.INTEGER:
        return NumberNode(parse_state.pop_front().value)

    return None

def term(parse_state):
    """
    term   : factor ((MUL | DIV) factor)*
    """
    
    node = factor(parse_state)
    while parse_state.current_token.symbol in (TokenSymbol.OPERATOR.MULTIPLY, TokenSymbol.OPERATOR.DEVIDE):
        node = BinaryOp(left=node, operator=get_operator_from_token(parse_state.pop_front()), right=factor(parse_state))

    return node

def expr(parse_state):
    """
    expr   : term ((PLUS | MINUS) term)*
    term   : factor ((MUL | DIV) factor)*
    factor : INTEGER | LPAREN expr RPAREN
    """

    node = term(parse_state)

    while parse_state.current_token.symbol in (TokenSymbol.OPERATOR.PLUS, TokenSymbol.OPERATOR.MIN):
        node = BinaryOp(left=node, operator=get_operator_from_token(parse_state.pop_front()), right=term(parse_state))

    return node

def parse(tokens):
    parse_state = ParseState(tokens)
    output = expr(parse_state)
    tree = Tree()
    tree.root.append(output)

    return tree 