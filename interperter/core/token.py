from enum import Enum

class TokenOperator(Enum):
    # OPERATORS
    PLUS        = "PLUS"
    MIN         = "MIN"
    DEVIDE      = "DEVIDE"
    MULTIPLY    = "MULTIPLY"
 
class TokenDiverse(Enum):
    WHITESPACE  = "WHITESPACE"
    INTEGER     = "INTEGER"
    EOF         = "EOF"

class TokenSymbol:
    OPERATOR = TokenOperator
    DIVERSE = TokenDiverse


class Token:
    def __init__(self, symbol: TokenSymbol, value: str):
        self.symbol = symbol
        self.value = value

    def __str__(self):
        return self.symbol.value + " " + self.value