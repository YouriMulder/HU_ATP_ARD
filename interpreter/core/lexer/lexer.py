from ..token import TokenSymbol, Token

import re
from typing import List
import copy

class TokenCombination:
    def __init__(self, symbol: TokenSymbol, regex: str):
        self.symbol = symbol
        self.regex = regex

    def __str__(self):
        return self.symbol.value + " " + self.regex

def get_matching_token_combination(sequence):
    token_type_combinations = [
        TokenCombination(TokenSymbol.OPERATOR.MATH.PLUS,         r"\+"),
        TokenCombination(TokenSymbol.OPERATOR.MATH.MIN,          r"\-"),
        TokenCombination(TokenSymbol.OPERATOR.MATH.DEVIDE,       r"\/"),
        TokenCombination(TokenSymbol.OPERATOR.MATH.MULTIPLY,     r"\*"),
        TokenCombination(TokenSymbol.OPERATOR.ASSIGNMENT.ASSIGNMENT,   r"^:=$"),
        TokenCombination(TokenSymbol.OPERATOR.RELATIONAL.EQUALS,       r"^:==$"),
        
        TokenCombination(TokenSymbol.CONSTANT.INTEGER,      r"\d+"),
        
        TokenCombination(TokenSymbol.DIVERSE.SHOW,    r"^ShOw$"),
        TokenCombination(TokenSymbol.DIVERSE.ENDOFSTATEMENT,r"!"),
        TokenCombination(TokenSymbol.DIVERSE.IDENTIFIER,    r"[a-zA-Z]"),
    ]

    token_types = list(filter(lambda x: re.match(x.regex, sequence), token_type_combinations))

    if len(token_types) == 1:
        return token_types[0]
    if len(token_types) > 1:
        pass
        # for token in token_types:
        #     print(token)
    return token_types[0]

def tokenize(characters: List[str], tokens=[], sequence: str="") -> List[Token]:
    head, *tail = characters
    characters = tail
    
    WHITESPACE = " "
    NEWLINE = "\n"
    ENDOFSTATEMENT = "!"
    if head not in (WHITESPACE, NEWLINE, ENDOFSTATEMENT):
        sequence = sequence + head

    if head in (WHITESPACE, ENDOFSTATEMENT) or len(characters) == 0:
        token_combination = get_matching_token_combination(sequence)
        tokens.append(Token(
            token_combination.symbol,
            sequence
        ))

        sequence = ""
    
    if head == ENDOFSTATEMENT:
        token_combination = get_matching_token_combination(head)
        tokens.append(Token(
            token_combination.symbol,
            head
        ))

    if len(characters) == 0:
        tokens.append(Token(
            TokenSymbol.DIVERSE.EOF,
            ""
        ))
        
        return

    tokenize(characters, tokens, sequence)

def lexer(source_code: str) -> List[Token]:
    tokens = []
    tokenize(list(source_code), tokens)
    return tokens
    