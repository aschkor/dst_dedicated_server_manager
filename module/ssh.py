import time
from typing import Union
from . import configuration_file as cf
from . import worldgen as wg
import paramiko
#from . import mods as md
from . import constant


class ClusterToken:
    def __init__(self,owner: Union[str, None], key:str):
        self.owner = owner
        self.key = key

class Server:
    def __init__(self, configuration: Union[cf.Cluster, cf.Server], worldgen: Union[wg.Overworld, wg.Underworld]):
            #, mod: Union[md.Module, None] = None):
        self.configuration = configuration
        self.worldgen = worldgen
        #self.mod = mod
        

class Cluster:
    def __init__(self, cluster: cf.Cluster , master: Server, cave: Union[Server, None], token: Union[ClusterToken,None], manager ):
        self.cluster = cluster
        self.master = master
        self.cave = cave
        self.token = token
        self.manager = manager
        
class SshSession:
    def __init__(self, ip_address: str, username: str, password: str):
        self.__session = paramiko.SSHClient()
        self.__session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__session.connect(ip_address, username=username, password=password)

    def exec(self, cmd: str) -> Union[str,bytes, None]:
        _, rep, _ = self.__session.exec_command(cmd)
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


    def is_exist(self,path: str) -> bool:
        rep = self.exec(constant.CMD_FILE_EXSIST.format(path, path))
        if rep == 'false':
            rep = self.exec(constant.CMD_DIR_EXSIST.format(path, path))
        return rep == 'true'


    def list_files(self, path: str) -> list[str]:
        stdout = self.exec(constant.CMD_LIST.format(path))
        res:list[str] = []
        if stdout == None:
            return res
        for l in stdout.split('\n'):
            if len(l):
                res.append(l)
        return res


    def remove(self, path:str)-> None:
        self.exec(constant.CMD_REMOVE.format(path))


    def get_file_content(self, path: str) -> Union[str,bytes, None]:
        path = self.__escape_space(path)
        if not self.is_exist(path):
            return None
        rep = self.exec(constant.CMD_READ_FILE.format(path))
        if rep == None:
            return str()
        if isinstance(rep, bytes):
            return rep
        while rep.endswith('\n'):
            rep = rep[:len(rep) -1]
        return rep


    def __mkdir_ifn(self, path: str) -> None:
        if not self.is_exist(path):
            self.exec(constant.CMD_CREATE_DIR.format(self.__escape_space(path)))


    def create_file(self, path: str, content: str) -> None:
        content = content.replace('"','\\"')
        command = constant.CMD_CREATE_FILE.format(content,self.__escape_space(path))
        self.exec(command)
        

    def __create_server_dir_ifn(self,  cluster: Cluster) -> None:
        self.__mkdir_ifn(constant.CLUSTER_DIRECTORY + str(cluster.cluster.name()))
        self.__mkdir_ifn(constant.CLUSTER_DIRECTORY + str(cluster.cluster.name()) + constant.MASTER_NAME_DIR)

        if cluster.cave != None:
            self.__mkdir_ifn(constant.CLUSTER_DIRECTORY + str(cluster.cluster.name()) + constant.CAVE_NAME_DIR)


    def __create_or_update_server_conf(self, cluster_info: Cluster) -> None:
        path:str = constant.CLUSTER_DIRECTORY + str(cluster_info.cluster.name())
        self.create_file(path + '/cluster.ini', str(cluster_info.cluster))
        self.create_file(path + constant.MASTER_NAME_DIR + '/server.ini', str(cluster_info.master.configuration))
        if cluster_info.cave != None:
            self.create_file(path+ constant.CAVE_NAME_DIR + '/server.ini', str(cluster_info.cave.configuration))


    def __create_token(self, cluster: Cluster) -> None:
        if cluster.token == None:
            raise NameError('The cluster must have a token')
        path = constant.CLUSTER_DIRECTORY + str(cluster.cluster.name()) + '/cluster_token.txt'
        self.create_file(path, cluster.token.key)


    def __cluster_conf(self, path:str) -> cf.Cluster:
            cluster = cf.Cluster()
            content = self.get_file_content(path + '/cluster.ini')
            if content != None:
                cluster.load(str(content))
            return cluster

    def __server_conf(self, path:str) -> cf.Server:
            server = cf.Server()
            content = self.get_file_content(path + '/server.ini')
            if content != None:
                server.load(str(content))
            server.load(str())
            return server

    def __cave_worldgen(self, path:str) -> wg.Underworld:
        w = wg.Underworld()
        w.load(self.get_file_content(path + '/worldgenoverride.lua'))
        return w

    def __master_worldgen(self, path:str) -> wg.Overworld:
        w = wg.Overworld()
        w.load(self.get_file_content(path + '/worldgenoverride.lua'))
        return w

    def __create_worldgen(self, cluster: Cluster) -> None:
        if not cluster.master.worldgen.is_empty():
            self.create_file(constant.CLUSTER_DIRECTORY + str(cluster.cluster.name()) + '/Master/worldgenoverride.lua', str(cluster.master.worldgen))
        if cluster.cave != None and not cluster.cave.worldgen.is_empty():
            self.create_file(constant.CLUSTER_DIRECTORY + str(cluster.cluster.name()) + '/Cave/worldgenoverride.lua', str(cluster.cave.worldgen))


    def get_available_tokens(self) -> list[ClusterToken]:
        res:list[ClusterToken] = []
        for line in self.list_files(constant.TOKEN_DIR):
            content = str(self.get_file_content(constant.TOKEN_DIR + line))
            if content != None:
                content = content.strip()
                content = content.replace('\n','')
                res.append(ClusterToken(line, content))
        return res


    def get_server_token(self,cluster_path:str) -> Union[ClusterToken, None] :
        path = cluster_path + '/cluster_token.txt'
        content = str(self.get_file_content(path))
        if content == None:
            return None
        tokens = self.get_available_tokens()

        for tk in tokens:
            if content == tk.key:
                return tk
        return ClusterToken(None, content)


    def add_token(self, tk: ClusterToken) -> None:
        self.__mkdir_ifn(constant.TOKEN_DIR)
        self.create_file(constant.TOKEN_DIR + str(tk.owner), tk.key)

    
    def servers(self) -> list[Cluster]:
        res: list[Cluster] = [] 
        for line in self.list_files(constant.CLUSTER_DIRECTORY):
            if line == None:
                continue
            path = constant.CLUSTER_DIRECTORY + line
            master_dir = path + '/Master'
            cave_dir = path + '/Cave'
            cluster_conf = self.__cluster_conf(path)
            master_conf = self.__server_conf(master_dir)
            cave_conf = self.__server_conf(cave_dir)
            master_gen = self.__master_worldgen(master_dir)
            cave_gen = self.__cave_worldgen(cave_dir)
            tk = self.get_server_token(path)
            master = Server(master_conf, master_gen)
            cave = Server(cave_conf, cave_gen)
            res.append(Cluster(cluster_conf, master, cave, tk, None))
        return res

    def add_server(self, cluster: Cluster) -> None:
        name = cluster.cluster.name()
        if name == None:
            raise NameError('The cluster must have a name')
        self.__create_server_dir_ifn(cluster)
        self.__create_or_update_server_conf(cluster)
        self.__create_token(cluster)
        self.__create_worldgen(cluster)
        cluster.manager.to_str(name)

    def start_servers(self, cluster_name: str) -> None:
        self.exec (constant.CMD_START_SERVER.format('Master', self.__escape_space(cluster_name), 'Master'))
        self.exec (constant.CMD_START_SERVER.format('Cave', self.__escape_space(cluster_name), 'Cave'))
        while not self.has_started_cluster():
            print('sleep')
            time.sleep(1)

    def stop_servers(self):
        self.exec(constant.CMD_STOP_SERVER.format('Master'))
        self.exec(constant.CMD_STOP_SERVER.format('Cave'))
        while self.has_started_cluster():
            time.sleep(1)

    def has_started_cluster(self):
        res = self.exec(constant.CMD_SCREEN_LIST)
        if res == None:
            return False
        return -1 != res.find('Master')

    def rm_cluster(self,cluster_name) -> None:
        self.remove(constant.CLUSTER_DIRECTORY + self.__escape_space(cluster_name))

    def __escape_space(self, s: str)-> str:
        is_esc = False
        res = ''
        for c in s:
            if c == ' ' and not is_esc:
                res = res + '\ '
            else:
                res = res + c

            is_esc = c == '\\'

        return res


#    def availabled_mod(self) -> md.AvailabledModules:
#        mods = md.AvailabledModules(self)
#        mods.load(f)
#        return mods
#
#        
#    def installed_mod(self, cluster_name: str) -> list[md.Module]:
#        master = []
#        mod_dir = constant.GAME_DIR + 'ugc_mods/' + cluster_name + '/{}/content/322330/'
#        for mod_id in self.__list_files(mod_dir.format('Master')):
#            master.append(md.read_instaled_module(mod_id, self.get_file_content(mod_dir.format('Master') + mod_id + '/modinfo.lua')))
#        cave = []
#        for mod_id in self.__list_files(mod_dir.format('Cave')):
#            cave.append(md.read_instaled_module(mod_id, self.get_file_content(mod_dir.format('Master') + mod_id + '/modinfo.lua')))
#
#        for c in cave:
#            add = True
#            for m in master:
#                if c == m :
#                    add = False
#                    break
#            if add:
#                master.append(c)
#
#        return master
#    def write_module_config(self, cluster_name, file) -> None:
#        path = constant.CLUSTER_DIRECTORY + cluster_name + '/{}/modoverride.lua'
#        self.__create_file(path.format('Master'), file)
#        self.__create_file(path.format('Cave'), file)
#
#
#
#


