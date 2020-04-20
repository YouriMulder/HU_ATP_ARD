from enum import Enum

class TokenOperatorMath(Enum):
    PLUS        = "PLUS"
    MIN         = "MIN"
    DEVIDE      = "DEVIDE"
    MULTIPLY    = "MULTIPLY"

class tokenOperatorRelational(Enum):
    EQUALS      = "EQUALS"

class TokenOperatorAssignment(Enum):
    ASSIGNMENT = "ASSIGNMENT"

class TokenOperator():
    # OPERATORS
    MATH        = TokenOperatorMath
    RELATIONAL  = tokenOperatorRelational
    ASSIGNMENT  = TokenOperatorAssignment

class TokenConstant(Enum):
    INTEGER     = "INTEGER"

class TokenControlFlow(Enum):
    WHILE     = "WHILE"

class TokenDiverse(Enum):
    WHITESPACE  = "WHITESPACE"
    IDENTIFIER  = "IDENTIFIER"
    ENDOFSTATEMENT = "ENDOFSTATEMENT"
    EOF         = "EOF"

class TokenSymbol:
    OPERATOR = TokenOperator
    CONSTANT = TokenConstant
    CONTROL = TokenControlFlow
    DIVERSE = TokenDiverse



class Token:
    def __init__(self, symbol: TokenSymbol, value: str):
        self.symbol = symbol
        self.value = value

    def __str__(self):
        return self.symbol.value + " " + self.value