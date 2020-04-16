import re
from typing import List
from enum import Enum
import copy

class TokenSymbol(Enum):
    WHITESPACE  = "WHITESPACE"
    PLUS        = "PLUS"
    INTEGER     = "INTEGER"

class TokenCombination:
    def __init__(self, symbol: TokenSymbol, regex: str):
        self.symbol = symbol
        self.regex = regex

    def __str__(self):
        return self.symbol.value + " " + self.regex

class Token:
    def __init__(self, symbol: TokenSymbol, value: str):
        self.symbol = symbol
        self.value = value

    def __str__(self):
        return self.symbol.value + " " + self.value

def get_matching_token_combination(sequence):
    token_type_combinations = [
        TokenCombination(TokenSymbol.WHITESPACE, "\s"),
        TokenCombination(TokenSymbol.PLUS, "\+"),
        TokenCombination(TokenSymbol.INTEGER, "\d+"),
    ]

    token_types = list(filter(lambda x: re.match(x.regex, sequence), token_type_combinations))

    if len(token_types) == 1:
        return token_types[0]
    if len(token_types) > 1:
        for token in token_types:
            print(token)
    return None

def tokenize(characters: List[str], tokens=[], sequence: str = "") -> List[Token]:
    head, *tail = characters
    characters = tail
    
    WHITESPACE = " "

    if head != WHITESPACE:
        sequence = sequence + head

    if head == WHITESPACE or len(characters) == 0:
        token_combination = get_matching_token_combination(sequence)
        tokens.append(Token(
            token_combination.symbol,
            sequence
        ))

        sequence = ""
        
    if len(characters) == 0:
        return

    tokenize(characters, tokens, sequence)

def lexer(source_code: str) -> List[Token]:
    tokens = []
    tokenize(list(source_code), tokens)
    return tokens
    