from enum import Enum

class TokenOperatorMath(Enum):
    PLUS            = "PLUS"
    MIN             = "MIN"
    DEVIDE          = "DEVIDE"
    MULTIPLY        = "MULTIPLY"

class tokenOperatorRelational(Enum):
    EQUALS          = "EQUALS"
    LESS            = "LESS"
    LESS_EQUAL      = "LESS_EQUAL"
    GREATER         = "GREATER"
    GREATER_EQUAL   = "GREATER_EQUAL"

class TokenOperatorAssignment(Enum):
    ASSIGNMENT      = "ASSIGNMENT"

class TokenOperator():
    # OPERATORS
    MATH            = TokenOperatorMath
    RELATIONAL      = tokenOperatorRelational
    ASSIGNMENT      = TokenOperatorAssignment

class TokenConstant(Enum):
    INTEGER         = "INTEGER"

class TokenControlFlow(Enum):
    IF              = "IF"
    WHILE           = "WHILE"
    LPARAN          = "LPAREN"
    RPARAN          = "RPAREN"
    LBRACE          = "LBRACE"
    RBRACE          = "RBRACE"
    
class TokenDiverse(Enum):
    WHITESPACE  = "WHITESPACE"
    SHOW        = "SHOW"
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