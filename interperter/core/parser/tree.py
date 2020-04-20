class Tree:
    def __init__(self):
        self.root = []

    def __str__(self):
        result = ""
        for note in self.root:
            result += str(note) + " "
        return result

class BinaryOp():
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def exec(self):
        return self.operator.func(self.left.exec(), self.right.exec())

    def __str__(self):
        return \
            "(" + str(self.left) + ") " + \
            str(self.operator) + " " + \
            "(" + str(self.right) + ")"

class OperatorNode:
    def __init__(self, func):
        self.func = func

    def __str__(self):
        return "OperatorNode: " + str(self.func)

class NumberNode:
    def __init__(self, value):
        self.value = int(value)

    def exec(self):
        return self.value

    def __str__(self):
        return "NumberNode: " + str(self.value)