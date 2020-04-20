from enum import Enum

class TokenOperator(Enum):
    # OPERATORS
    PLUS        = "PLUS"
    MIN         = "MIN"
    DEVIDE      = "DEVIDE"
    MULTIPLY    = "MULTIPLY"
    ASSIGNMENT  = "ASSIGNMENT"

class TokenConstant(Enum):
    INTEGER     = "INTEGER"

class TokenDiverse(Enum):
    WHITESPACE  = "WHITESPACE"
    IDENTIFIER  = "IDENTIFIER"
    ENDOFSTATEMENT = "ENDOFSTATEMENT"
    EOF         = "EOF"

class TokenSymbol:
    OPERATOR = TokenOperator
    CONSTANT = TokenConstant
    DIVERSE = TokenDiverse


class Token:
    def __init__(self, symbol: TokenSymbol, value: str):
        self.symbol = symbol
        self.value = value

    def __str__(self):
        return self.symbol.value + " " + self.value