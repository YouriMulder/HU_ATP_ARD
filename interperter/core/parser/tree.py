class Tree:
    def __init__(self, root_node):
        self.root_node = root_node

    def __str__(self):
        node_strings = list(map(lambda node: str(node), self.root_node.nodes))
        return "\n".join(node_strings)

class RootNode:
    def __init__(self, nodes):
        self.nodes = nodes

class BinaryOpNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return \
            "(" + str(self.left) + ") " + \
            str(self.operator) + " " + \
            "(" + str(self.right) + ")"

class AssignmentNode(BinaryOpNode):
    def __init__(self, identifier, expr):
        BinaryOpNode.__init__(self, identifier, ":=", expr)

class OperatorNode:
    def __init__(self, value):
        self.value = str(value)

    def __str__(self):
        return "OperatorNode: " + str(self.value)

class NumberNode:
    def __init__(self, value):
        self.value = int(value)

    def __str__(self):
        return "NumberNode: " + str(self.value)

class IdentifierNode:
    def __init__(self, value):
        self.value = str(value)