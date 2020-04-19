class Tree:
    def __init__(self):
        self.root = []

class BinaryOp():
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self):
        return \
            str(self.left) + \
            str(self.operator) + \
            str(self.right)
    
    def exec(self):
        return self.operator.func(self.left.exec(), self.right.exec())

class OperatorNode:
    def __init__(self, func):
        self.func = func

class NumberNode:
    def __init__(self, value):
        self.value = int(value)

    def exec(self):
        return self.value