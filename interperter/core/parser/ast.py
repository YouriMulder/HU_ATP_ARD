from .tree import *

from ..token import TokenSymbol

def factor(token):
    if token.symbol == TokenSymbol.DIVERSE.INTEGER:
        return NumberNode(token.value)
    
    return None

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


def expr(tokens, previous_node = None):
    if len(tokens) == 0:
        return previous_node
    
    if token_is_operator(tokens[0]):
        # left is expression
        left_node = previous_node
        
        current_token, *tokens = tokens

        operator_node = get_operator_from_token(current_token) 
        
        current_token, *tokens = tokens
        right_node = factor(current_token)
    else:
        current_token, *tokens = tokens
        left_node = factor(current_token)

        current_token, *tokens = tokens
        operator_node = get_operator_from_token(current_token) 
        
        current_token, *tokens = tokens
        right_node = factor(current_token)
    
    node = BinaryOp(left_node, operator_node, right_node)
    return expr(tokens, node)

def parse(tokens):
    tree = Tree()
    output = expr(tokens)
    tree.root.append(output)
    return tree