from typing import Union
import time
from . import ssh
from . import constant
from . import configuration_file as cf
from . import worldgen as wg
from . import mods as md
from . import token as tk
try:
    from pathlib import PurePosixPath as Path
except:
    print('install pathlib module')
    import os
    try:
        os.system('python3 -m pip install pathlib')
    except:
        try:
            os.system('python -m pip install pathlib')
        except:
            print('Pip might not be installed, please install pip')
            import sys
            sys.exit()
    from pathlib import PurePosixPath as Path


class Server:
    def __init__(self, settings: cf.Server, world_settings: wg.WorldGen, mods: list[md.Module]):
        self.settings = settings
        self.world_settings = world_settings
        self.mods = mods

class Cluster:
    def __init__(self, settings: cf.Cluster, token:tk.Token, master: Server, cave: Union[Server, None]):
        self.settings = settings
        self.token = token
        self.master = master
        self.cave = cave

def is_started() -> bool:
    res = ssh.execute(constant.CMD_SCREEN_LIST)
    if res is None:
        return False
    return -1 != res.find(str(constant.MASTER_NAME_DIR)) or -1 != res.find(str(constant.CAVE_NAME_DIR))
    
def stop():
    ssh.execute(constant.CMD_STOP_SERVER.format(constant.MASTER_NAME_DIR))
    ssh.execute(constant.CMD_STOP_SERVER.format(constant.CAVE_NAME_DIR))
    while is_started():
        time.sleep(1)

def remove(cluster_name:Path):
    ssh.remove(constant.CLUSTER_DIRECTORY / cluster_name)
    ssh.remove(constant.UGC_DIR / cluster_name)

def start(cluster_name:Path):
    name = str(cluster_name).replace(' ', '\ ')
    ssh.execute(constant.CMD_START_SERVER.format(constant.MASTER_NAME_DIR, name, constant.MASTER_NAME_DIR))
    ssh.execute(constant.CMD_START_SERVER.format(constant.CAVE_NAME_DIR, name, constant.CAVE_NAME_DIR))

def add(cluster: Cluster):
    name = cluster.settings.name() 
    if name is None:
        raise RuntimeError('The cluster has no name')
    ssh.mkdir_ifn(constant.CLUSTER_DIRECTORY / name)
    ssh.mkdir_ifn(constant.CLUSTER_DIRECTORY / name / constant.MASTER_NAME_DIR)
    ssh.mkdir_ifn(constant.CLUSTER_DIRECTORY / name / constant.CAVE_NAME_DIR)
    cluster.settings.install()
    cluster.token.install(name)
    cluster.master.settings.install(name)
    md.install(name, cluster.master.mods, True)
    if cluster.cave is None:
        return
    cluster.cave.settings.install(name)
    md.install(name, cluster.cave.mods, False)

def clusters() -> list[Cluster]:
    res = []
    for file in ssh.list_files(constant.CLUSTER_DIRECTORY):
        master = Server(cf.Server(file), wg.Overworld(file), [])
        cave = None
        if ssh.is_exist(constant.CLUSTER_DIRECTORY / constant.CAVE_NAME_DIR):
            cave = Server(cf.Server(file, False), wg.Underworld(file), [])
        res.append(Cluster(cf.Cluster(file),tk.Token(cluster_name = file), master, cave))
    return res
