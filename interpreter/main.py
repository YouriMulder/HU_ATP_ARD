from path import path
from core.lexer.lexer import lexer
from core.parser.ast import create_ast
from core.interpreter.interpreter import interpret
import sys
import threading

class file_input:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_content = self.get_file_content()

    def get_file_content(self) -> str:
        with open(self.file_path, 'r') as opened_file:
            data = opened_file.read()
        return data

    def __str__(self) -> str:
        return \
            "File path: " + self.file_path + "\n" \
            + self.file_content

def main():
    source_file_path = path.source + "turing.ym"
    source_file = file_input(source_file_path)
    print("Tokenize")
    tokens = lexer(source_file.get_file_content())
    print("ast")
    ast = create_ast(tokens)
    print("interpret")
    result = interpret(ast) 
    print(result)

sys.setrecursionlimit(0x100000)
threading.stack_size(256000000) #set stack to 256mb
t = threading.Thread(target=main())
t.start()
t.join()
