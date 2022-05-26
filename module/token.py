from .import ssh
from . import constant
from typing import Union
from pathlib import PurePosixPath as Path

class Token():
    def __init__(self, content = None, owner = None, cluster_name = None):
        self.content = None
        self.owner = None
        if cluster_name is None:
            self.content = content
            self.owner = owner
        else:
            content = ssh.get_file_content(constant.CLUSTER_DIRECTORY / cluster_name / 'cluster_token.txt')
            if content is None:
                return 
            token = Token(content)
            for tk in tokens():
                if token == tk:
                    self.content = tk.content
                    self.owner = tk.owner


    def __install(self, path:Path):
        if self.content is None:
            raise RuntimeError('Cannot install an empty token')
        ssh.create_file(path, self.content)


    def install(self, cluster_name: str):
        path = constant.CLUSTER_DIRECTORY / cluster_name / 'cluster_token.txt'
        self.__install(path)

    def add_to_available_token(self) -> bool:
        if self.owner is None:
            raise RuntimeError('Token must have an owner')
        path = constant.TOKEN_DIR + self.owner
        if not ssh.is_exist(path):
            self.__install(path)
            return True
        return False

    def __eq__(self, other):
        return self.content == other.content


    def __str__(self):
        if self.owner is None:
            return str()
        return self.owner


def tokens() -> list[Token]:
    res = []
    for line in ssh.list_files(constant.TOKEN_DIR):
        token = __read(constant.TOKEN_DIR / line, line)
        if token is None:
            continue
        res.append(token)
    return res


def __read(path:Path, name: Union[str, None] = None) -> Union[Token, None]:
    content = ssh.get_file_content(path)
    if content is None:
        return None
    return Token(content, name)
