from path import path
from lexer.lexer import lexer

class file_input:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_content = self.get_file_content()

    def get_file_content(self) -> str:
        with open(self.file_path, 'r') as opened_file:
            data = opened_file.read()
        return data

    def __str__(self):
        return \
            "File path: " + self.file_path + "\n" \
            + self.file_content


source_file_path = path.source + "main.ym"
source_file = file_input(source_file_path)
tokens = lexer(source_file.get_file_content())
for token in tokens:
    print(token)

        