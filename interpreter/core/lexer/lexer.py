from ..token import TokenSymbol, Token

import re
from typing import Union, List

class TokenCombination:
    def __init__(self, symbol: TokenSymbol, regex: str):
        self.symbol = symbol
        self.regex = regex

    def __str__(self) -> str:
        return self.symbol.value + " " + self.regex


def get_matching_token_combination(sequence: str) -> Union[TokenCombination, None]:
    token_type_combinations = [
        TokenCombination(TokenSymbol.CONTROL.WHILE,         r"^WhIlE$"),
        TokenCombination(TokenSymbol.CONTROL.IF,            r"^iF$"),
        TokenCombination(TokenSymbol.CONTROL.LPARAN,        r"\("),
        TokenCombination(TokenSymbol.CONTROL.RPARAN,        r"\)"),
        TokenCombination(TokenSymbol.CONTROL.LBRACE,        r"\{"),
        TokenCombination(TokenSymbol.CONTROL.RBRACE,        r"\}"),

        TokenCombination(TokenSymbol.OPERATOR.MATH.PLUS,    r"\+"),
        TokenCombination(TokenSymbol.OPERATOR.MATH.MIN,     r"\-"),
        TokenCombination(TokenSymbol.OPERATOR.MATH.DEVIDE,  r"\/"),
        TokenCombination(TokenSymbol.OPERATOR.MATH.MULTIPLY,r"\*"),
        TokenCombination(TokenSymbol.OPERATOR.ASSIGNMENT.ASSIGNMENT,    r"^:=$"),
        
        TokenCombination(TokenSymbol.OPERATOR.RELATIONAL.EQUALS,        r"^:==$"),
        TokenCombination(TokenSymbol.OPERATOR.RELATIONAL.LESS,          r"^:<$"),
        TokenCombination(TokenSymbol.OPERATOR.RELATIONAL.LESS_EQUAL,    r"^:<=$"),
        TokenCombination(TokenSymbol.OPERATOR.RELATIONAL.GREATER,       r"^:>$"),
        TokenCombination(TokenSymbol.OPERATOR.RELATIONAL.GREATER_EQUAL, r"^:>=$"),

        TokenCombination(TokenSymbol.CONSTANT.INTEGER,      r"\d+"),
        
        TokenCombination(TokenSymbol.DIVERSE.SHOW,          r"^ShOw$"),
        TokenCombination(TokenSymbol.DIVERSE.ENDOFSTATEMENT,r"!"),
        TokenCombination(TokenSymbol.DIVERSE.IDENTIFIER,    r"[a-zA-Z]"),
    ]

    token_types = list(filter(lambda x: re.match(x.regex, sequence), token_type_combinations))

    if len(token_types) == 0:
        return None
        
    return token_types[0]

def tokenize(characters: List[str], tokens: List[Token]=[], sequence: str="") -> List[Token]:
    head, *tail = characters
    characters = tail

    WHITESPACE = " "
    NEWLINE = "\n"
    ENDOFSTATEMENT = "!"
    if head not in (WHITESPACE, ENDOFSTATEMENT, NEWLINE):
        sequence = sequence + head

    if head in (WHITESPACE, ENDOFSTATEMENT, NEWLINE) or len(characters) == 0:
        if sequence != "":
            token_combination = get_matching_token_combination(sequence)
            tokens = tokens + [Token(token_combination.symbol, sequence)]

            sequence = ""
        
        if head == ENDOFSTATEMENT:
            token_combination = get_matching_token_combination(head)
            tokens = tokens + [Token(token_combination.symbol, head)]
        
    if len(characters) == 0:
        tokens = tokens + [Token(TokenSymbol.DIVERSE.EOF, "")]
        return tokens
        
    return tokenize(characters, tokens, sequence)

def lexer(source_code: str) -> List[Token]:
    tokens = tokenize(list(source_code))
    return tokens
    