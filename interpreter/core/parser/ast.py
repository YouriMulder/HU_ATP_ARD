from .tree import ConditionNode, WhileNode, RootNode, IdentifierNode, NumberNode, OperatorNode, BinaryOpNode, AssignmentNode, PrintNode, Tree

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

def term_check_multiply_or_devide(parse_state, root):
    if parse_state.current_token.symbol not in (TokenSymbol.OPERATOR.MATH.MULTIPLY, TokenSymbol.OPERATOR.MATH.DEVIDE):
        return root
    
    node = BinaryOpNode(left=root, operator=OperatorNode(parse_state.pop_front().value), right=factor(parse_state))
    return term_check_multiply_or_devide(parse_state, node)

def term(parse_state):
    """
    term   : factor ((MUL | DIV) factor)*
    """

    node = factor(parse_state)
    
    return term_check_multiply_or_devide(parse_state, node)

def expr_check_plus_or_minus(parse_state, root):
    if parse_state.current_token.symbol not in (TokenSymbol.OPERATOR.MATH.PLUS, TokenSymbol.OPERATOR.MATH.MIN):
        return root
    
    node = BinaryOpNode(left=root, operator=OperatorNode(parse_state.pop_front().value), right=term(parse_state))
    return expr_check_plus_or_minus(parse_state, node)

def expr(parse_state, initial_term=None):
    """
    expr   : term ((PLUS | MINUS) term)*
    term   : factor ((MUL | DIV) factor)*
    factor : INTEGER | IDENTIFIER
    """
    if initial_term == None:
        node = term(parse_state)
    else:
        node = initial_term

    return expr_check_plus_or_minus(parse_state, node)

def parse_condition(parse_state, root_node, condition_node_type) -> None:
    if parse_state.pop_front().symbol not in (TokenSymbol.CONTROL.IF, TokenSymbol.CONTROL.WHILE):
        return None
        
    if parse_state.pop_front().symbol != TokenSymbol.CONTROL.LPARAN:
        return None

    condition_node = parsing(parse_state)

    if parse_state.pop_front().symbol != TokenSymbol.CONTROL.RPARAN:
        return None
    
    execute_node = parsing(parse_state)

    return condition_node_type(condition_node, execute_node)
    
def parsing(parse_state, root=None):
    
    if parse_state.current_token.symbol == TokenSymbol.CONTROL.LBRACE:
        parse_state.pop_front()
        root_node = RootNode([])
        root_node = create_root_node(parse_state, root_node)
        return root_node
    
    elif parse_state.current_token.symbol == TokenSymbol.OPERATOR.ASSIGNMENT.ASSIGNMENT:
        parse_state.pop_front()
        assignment_node = parsing(parse_state)
        node = AssignmentNode(root, assignment_node)
        return parsing(parse_state, node)
    
    elif parse_state.current_token.symbol == TokenSymbol.CONSTANT.INTEGER:
        node = expr(parse_state)
        return parsing(parse_state, node)
    
    elif parse_state.current_token.symbol == TokenSymbol.DIVERSE.IDENTIFIER:
        node = IdentifierNode(parse_state.pop_front().value)
        return parsing(parse_state, node)
    
    elif parse_state.current_token.symbol in TokenSymbol.OPERATOR.RELATIONAL:
        node = BinaryOpNode(root, OperatorNode(parse_state.pop_front().value), expr(parse_state))
        return parsing(parse_state, node)
    
    elif parse_state.current_token.symbol == TokenSymbol.DIVERSE.SHOW:
        parse_state.pop_front().value
        return PrintNode(parsing(parse_state, root))

    elif parse_state.current_token.symbol == TokenSymbol.CONTROL.IF:
        return parse_condition(parse_state, root, ConditionNode)

    elif parse_state.current_token.symbol == TokenSymbol.CONTROL.WHILE:
        return parse_condition(parse_state, root, WhileNode)

    elif parse_state.current_token.symbol in TokenSymbol.OPERATOR.MATH:
        return expr(parse_state, root)
    
    elif parse_state.current_token.symbol in (TokenSymbol.CONTROL.RPARAN, TokenSymbol.CONTROL.RBRACE):
        return root

    return root

def create_root_node(parse_state, root_node):
    if len(parse_state.tokens) == 0 or parse_state.current_token.symbol in (TokenSymbol.DIVERSE.EOF, TokenSymbol.CONTROL.RBRACE):
        return root_node
    
    node = parsing(parse_state)
    if parse_state.pop_front().symbol != TokenSymbol.DIVERSE.ENDOFSTATEMENT:
        print("create root nodes error")

    new_root_node = root_node
    new_root_node.nodes.append(node)
    return create_root_node(parse_state, new_root_node)

def create_ast(tokens):
    parse_state = ParseState(tokens)
    root_node = RootNode([])
    root_node = create_root_node(parse_state, root_node)
    tree = Tree(root_node)
    return tree