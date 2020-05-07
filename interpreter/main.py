# This file is not conform the functional programming principles

from path import Path
from core.lexer.lexer import lexer
from core.parser.ast import create_ast
from core.interpreter.interpreter import interpret
import sys
import threading


def main() -> None:
    """
    @brief This function is used to start the program.
    @details
        This function executes the four steps of the interpreter.
        1. Getting the source file content 
        2. Create tokens from the source file content
        3. Create abstract syntax tree from the tokens
        4. Interpret the abstract syntax tree
    """

    source_file_path = Path.source_test

    source_file_content = None
    with open(source_file_path, 'r') as opened_file:
        source_file_content = opened_file.read()

    if source_file_content == None:
        return

    print("Lexing")
    tokens = lexer(source_file_content)

    print("Parsing")
    ast = create_ast(tokens)
    print(ast)

    print("Interpreting")
    result = interpret(ast)

    print(result)


sys.setrecursionlimit(0x100000)
threading.stack_size(256000000)  # set stack to 256mb
t = threading.Thread(target=main())
t.start()
t.join()
