from .tree import IdentifierNode, NumberNode, OperatorNode, BinaryOpNode, AssignmentNode, Tree

from ..token import TokenSymbol

def token_is_operator(token):
    return token.symbol in TokenSymbol.OPERATOR

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
    factor : INTEGER
    """

    if parse_state.current_token.symbol == TokenSymbol.CONSTANT.INTEGER:
        return NumberNode(parse_state.pop_front().value)
    
    if parse_state.current_token.symbol == TokenSymbol.DIVERSE.IDENTIFIER:
        return IdentifierNode(parse_state.pop_front().value)
    

    return None

def term(parse_state):
    """
    term   : factor ((MUL | DIV) factor)*
    """

    node = factor(parse_state)
    while parse_state.current_token.symbol in (TokenSymbol.OPERATOR.MULTIPLY, TokenSymbol.OPERATOR.DEVIDE):
        node = BinaryOpNode(left=node, operator=OperatorNode(parse_state.pop_front().value), right=factor(parse_state))
    return node

def expr(parse_state):
    """
    expr   : term ((PLUS | MINUS) term)*
    term   : factor ((MUL | DIV) factor)*
    factor : INTEGER
    """

    node = term(parse_state)

    while parse_state.current_token.symbol in (TokenSymbol.OPERATOR.PLUS, TokenSymbol.OPERATOR.MIN):
        node = BinaryOpNode(left=node, operator=OperatorNode(parse_state.pop_front().value), right=term(parse_state))

    return node 

def parsing(parse_state, root=None):
    if parse_state.current_token.symbol == TokenSymbol.DIVERSE.IDENTIFIER:
        node = IdentifierNode(parse_state.pop_front().value)
        return parsing(parse_state, node)
    elif parse_state.current_token.symbol == TokenSymbol.OPERATOR.ASSIGNMENT:
        parse_state.pop_front()
        node = AssignmentNode(root, expr(parse_state))
        return parsing(parse_state, node)
       
    return root

def create_root_nodes(parse_state, root=list()):
    if len(parse_state.tokens) == 0 or parse_state.current_token.symbol == TokenSymbol.DIVERSE.EOF:
        return root
    
    node = parsing(parse_state)
    if parse_state.pop_front().symbol != TokenSymbol.DIVERSE.ENDOFSTATEMENT:
        print("create root nodes error")

    new_root = root
    new_root.append(node)
    return create_root_nodes(parse_state, new_root)

def create_ast(tokens):
    parse_state = ParseState(tokens)
    root = create_root_nodes(parse_state)
    tree = Tree()
    tree.root = root    
    return tree