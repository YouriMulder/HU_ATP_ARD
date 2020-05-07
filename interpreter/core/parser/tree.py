from typing import List


class TreeNode:
    pass


class RootNode(TreeNode):
    def __init__(self, nodes: List[TreeNode]):
        self.nodes = nodes

    def __str__(self) -> str:
        result = map(lambda node: str(node), self.nodes)
        return '[' + ', '.join(result) + ']'


class IdentifierNode(TreeNode):
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return self.value


class OperatorNode(TreeNode):
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return self.value


class BinaryOpNode(TreeNode):
    def __init__(self, left: TreeNode, operator: OperatorNode, right: TreeNode):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return \
            "(" + str(self.left) + ") " + \
            str(self.operator) + " " + \
            "(" + str(self.right) + ")"


class AssignmentNode(BinaryOpNode):
    def __init__(self, identifier: IdentifierNode, expr: TreeNode):
        BinaryOpNode.__init__(self, identifier, ":=", expr)


class NumberNode(TreeNode):
    def __init__(self, value: str):
        self.value = int(value)

    def __str__(self) -> str:
        return str(self.value)


class PrintNode(TreeNode):
    def __init__(self, print_node: TreeNode):
        self.print_node = print_node

    def __str__(self) -> str:
        return str(self.print_node)


class ConditionNode(TreeNode):
    def __init__(self, condition_node: TreeNode, execute_node: TreeNode):
        self.condition_node = condition_node
        self.execute_node = execute_node

    def __str__(self) -> str:
        return str(self.condition_node) + " -> " + str(self.execute_node)


class WhileNode(ConditionNode):
    def __init__(self, condition_node, execute_node):
        ConditionNode.__init__(self, condition_node, execute_node)

    def __str__(self) -> str:
        return ConditionNode.__str__(self)


class Tree:
    def __init__(self, root_node: TreeNode):
        self.root_node = root_node

    def __str__(self):
        node_strings = list(map(lambda node: str(node), self.root_node.nodes))
        return "\n".join(node_strings)
