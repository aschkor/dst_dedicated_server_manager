from typing import Union
from pathlib import PurePosixPath as Path
from . import constant
import paramiko


class SshSession(object):
    __instance = None

    def __new__(cls, ip_address: Union[str, None] = None, username: Union[str, None] = None, password: Union[str, None] = None):
        if cls.__instance is None:
            if ip_address is None or username is None or password is None:
                raise RuntimeError('No username or ip address or password for connect to the server')
            cls.__instance = super(SshSession, cls).__new__(cls)
            cls._session = paramiko.SSHClient()
            cls._session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cls._session.connect(ip_address, username=username, password=password)
        return cls

def execute(cmd: str) -> Union[str,bytes, None]:
    _, rep, _ = SshSession()._session.exec_command(cmd)
    rep = rep.read()
    try: 
        rep = rep.decode('utf-8')
    except:
        try:
            rep = rep.decode('cp1252')
        except:
            return rep

    if rep.endswith('\n'):
        rep = rep[:len(rep) -1]

    if len(rep): 
        return rep
    return None


def is_exist(path:Path) -> bool:
    rep = execute(constant.CMD_FILE_EXSIST.format(str(path).replace(' ','\ '), str(path).replace(' ','\ ')))
    if rep == 'false':
        rep = execute(constant.CMD_DIR_EXSIST.format(str(path).replace(' ','\ '), str(path).replace(' ', '\ ')))
    return rep == 'true'


def list_files(path:Path) -> list[str]:
    stdout = execute(constant.CMD_LIST.format(str(path).replace(' ', '\ ')))
    res:list[str] = []
    if stdout is None:
        return res
    for l in stdout.split('\n'):
        if len(l):
            res.append(l)
    return res


def remove( path:Path)-> None:
    execute(constant.CMD_REMOVE.format(str(path).replace(' ', '\ ')))

def __read_file(path: Path)  -> Union[str,bytes,None]:
    if not is_exist(path):
        return None
    return execute(constant.CMD_READ_FILE.format(str(path).replace(' ', '\ ')))

def get_binary_file(path:Path) -> Union[bytes,None]:
    rep = __read_file(path)
    if rep is None:
        return None
    if isinstance(rep, bytes):
        return rep
    raise RuntimeError('The file is not a binay. Use SshSession::get_file_content function instead')

def get_file_content(path:Path) -> Union[str,None]:
    rep = __read_file(path)
    if rep is None:
        return None
    rep = str(rep)
    if isinstance(rep, bytes):
        raise RuntimeError('The file is in binary format. Use SshSession::get_binary_file instead')
    while rep.endswith('\n'):
        rep = rep[:len(rep) -1]
    return rep


def mkdir_ifn( path:Path) -> None:
    if not is_exist(path):
        execute(constant.CMD_CREATE_DIR.format(str(path).replace(' ', '\ ')))


def create_file(path: Path, content: str) -> None:
    command = constant.CMD_CREATE_FILE.format(content,str(path).replace(' ', '\ '))
    execute(command)
