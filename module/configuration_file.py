from enum import Enum
from io import StringIO
import configparser
from typing import Union
import ipaddress

class Options(Enum):
    def __str__(self):
        return self.value[0]

class Intention(Options):
    COOPERATIVE = 'cooperative',
    COMPETITIVE = 'competitive',
    SCOCIAL = 'scocial',
    MADNESS = 'madness'

    def __str__(self):
        return self.value[0]


class Mode(Options):
    SURVIVAL = 'survival',
    ENDLESS = 'endless',
    WILDERNESS = 'wilderness'
    def __str__(self):
        return self.value[0]


class TickRate(Options):
    NORMAL = 15,
    QUICK = 30,
    QUICKER = 45,
    MAX = 60
    def __str__(self):
        return str(self.value[0])


class KeyInfo:
    def __init__(self, name, category, default = None):
        self.name = name
        self.default = default
        self.category = category


class Categories(Enum):
    MISC = 'MISC',
    SHARD = 'SHARD',
    STEAM = 'STEAM',
    NETWORK = 'NETWORK',
    GAMEPLAY = 'GAMEPLAY',
    ACCOUNT = 'ACCOUNT',

    def __str__(self):
        return self.value[0]

class Key(Enum):
    def __str__(self):
        return self.value[0].name


def check_len(value, var_name: str):
    if not len(value):
        raise NameError(var_name + ' cannot be empty')
    
def check_positiv(value, var_name: str):
    if value <= 0 :
        raise NameError(var_name + ' must be positif')

def check_strict_positiv(value, var_name: str):
    if value < 0 :
        raise NameError(var_name + ' must be superior to 0')
def check_ip(value):
    ipaddress.ip_address(value)

class ClusterKey(Key):
    MAX_SNAPSHOTS = KeyInfo('max_snapshots', Categories.MISC, 6),
    CONSOLE_ENABLED = KeyInfo('console_enabled', Categories.MISC, True),
    SHARD_ENABLED = KeyInfo('shard_enabled', Categories.SHARD, False),
    BIND_IP = KeyInfo('bind_ip', Categories.SHARD, '127.0.0.1'),
    MASTER_IP = KeyInfo('master_ip', Categories.SHARD, None),
    MASTER_PORT = KeyInfo('master_port', Categories.SHARD, 10888),
    CLUSTER_KEY = KeyInfo('cluster_key', Categories.SHARD, None), 
    STEAM_GROUP_ONLY = KeyInfo('steam_group_only', Categories.STEAM, False),
    STEAM_GROUP_ID = KeyInfo('steam_group_id', Categories.STEAM, 0),
    STEAM_GROUP_ADMINS = KeyInfo('steam_group_admin', Categories.STEAM, False),
    OFFLINE = KeyInfo('offline_cluster', Categories.NETWORK, False),
    TICK_RATE = KeyInfo('tick_rate', Categories.NETWORK, TickRate.NORMAL),
    WHITELIST_SLOTS = KeyInfo('whitelist_list', Categories.NETWORK, 0),
    PASSWORD = KeyInfo('cluster_password', Categories.NETWORK, None),
    NAME = KeyInfo('cluster_name', Categories.NETWORK),
    DESCRIPTION = KeyInfo('cluster_description', Categories.NETWORK, str()),
    LAN_ONLY = KeyInfo('lan_only_cluster', Categories.NETWORK, False),
    INTENTION = KeyInfo('cluster_intention', Categories.NETWORK, Intention.COOPERATIVE),
    AUTOSAVER_ENABLED = KeyInfo('autosave_enabled', Categories.NETWORK, True),
    MAX_PLAYERS = KeyInfo('max_player', Categories.GAMEPLAY, 16),
    PVP = KeyInfo('pvp', Categories.GAMEPLAY, False),
    GAME_MODE = KeyInfo('game_mode', Categories.GAMEPLAY, Mode.SURVIVAL),
    PAUSE_WHEN_EMPTY = KeyInfo('pause_when_empty', Categories.GAMEPLAY, False),
    VOTE_ENABLED = KeyInfo('vote_enabled', Categories.GAMEPLAY, True),

class ServerKey(Key):
    IS_MASTER = KeyInfo('is_master', Categories.SHARD),
    NAME = KeyInfo('name', Categories.SHARD),
    AUTHENTICATION_PORT = KeyInfo('autentication_port', Categories.STEAM, 8766),
    MASTER_PORT = KeyInfo('master_server_port', Categories.STEAM, 27016),
    PORT = KeyInfo('server_port', Categories.NETWORK, 10999),

def to_bool(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, int) or isinstance(value, float):
        return bool(value)

    if value.lower() == 'true':
        return True

    return False


class ConfigurationFile:
    def __init__(self):
        self.__config = configparser.ConfigParser()
        

    def load(self, config_file: str) -> None:
        self.__config.read_string(config_file)

    def __is_exist(self, key) -> bool:
            return self.__config.has_option(str(key.value[0].category), str(key.value[0].name))
        
    def __is_default(self, key, value) -> bool:
        return key.value[0].default == value


    def __rm(self, key):
        cat = str(key.value[0].category)
        self.__config.remove_option(cat, str(key.value[0].name))
        if not len(self.__config[cat]):
            self.__config.remove_section(cat)

    def __add(self, key, value):
        cat = str(key.value[0].category)
        if not self.__config.has_section(cat):
            self.__config.add_section(cat)

        self.__config.set(cat, str(key), str(value))

    def __get(self, key):
        return self.__config.get(str(key.value[0].category), str(key.value[0].name))


    def remove_option(self, key) -> None:
        self.add_option(key, None)


    def get_option(self, key):
        if self.__is_exist(key):
            return self.__get(key)
        return key.value[0].default


    def add_option(self,key, value) -> None:
        if value == None:
            if self.__is_exist(key):
                self.__rm(key)
            return

        if isinstance(value, str):
            if not len(value):
                self.__rm(key)
                return

        if self.__is_exist(key) and self.__is_default(key, value):
            self.__rm(key)
            return

        if self.__is_default(key, value):
            return

        self.__add(key,value)
            

    def __str__(self):
        res = StringIO()
        self.__config.write(res)
        return res.getvalue()


class Cluster(ConfigurationFile):
    def __init__(self):
        super().__init__()


    def __rm_ifn(self, key: ClusterKey, value) -> bool:
        if value == None:
            self.remove_option(key)
            return True
        if isinstance(value, str):
            if not len(value):
                self.remove_option(key)
                return True
        return False


    def max_snapshots(self) -> int:
        return int(self.get_option(ClusterKey.MAX_SNAPSHOTS))


    def is_console_enabled(self) -> bool:
        return to_bool(self.get_option(ClusterKey.CONSOLE_ENABLED))
        

    def is_shard_enabled(self) -> bool:
        return to_bool(self.get_option(ClusterKey.SHARD_ENABLED))


    def bind_ip(self) -> str:
        return self.get_option(ClusterKey.BIND_IP)


    def master_ip(self) -> Union[str, None]:
        return self.get_option(ClusterKey.MASTER_IP)


    def master_port(self) -> int:
        return int(self.get_option(ClusterKey.MASTER_PORT))


    def cluster_key(self) -> Union[str, None]:
        return self.get_option(ClusterKey.CLUSTER_KEY)


    def is_steam_group_only(self) -> bool:
        return to_bool(self.get_option(ClusterKey.STEAM_GROUP_ONLY))


    def steam_group_id(self) -> int:
        return int(self.get_option(ClusterKey.STEAM_GROUP_ID))


    def is_steam_group_admins(self) -> bool :
        return to_bool(self.get_option(ClusterKey.STEAM_GROUP_ADMINS))
    

    def is_cluster_offline(self) -> bool:
        return to_bool(self.get_option(ClusterKey.OFFLINE))


    def tick_rate(self) -> TickRate:
        res = self.get_option(ClusterKey.TICK_RATE)
        if isinstance(res, TickRate):
            return res
        return TickRate(res)


    def whitelist_sots(self) -> int:
        return int(self.get_option(ClusterKey.WHITELIST_SLOTS))


    def password(self) -> Union[str, None]:
        return self.get_option(ClusterKey.PASSWORD)


    def name(self) -> Union[str, None]:
        return self.get_option(ClusterKey.NAME)


    def description(self) -> Union[str, None]:
        return self.get_option(ClusterKey.DESCRIPTION)


    def is_lan_only(self) -> bool:
        return to_bool(self.get_option(ClusterKey.LAN_ONLY))


    def intention(self) -> Intention:
        res = self.get_option(ClusterKey.INTENTION)
        if isinstance(res, Intention):
            return res
        return Intention(res)


    def is_autosaver_enabled(self) -> bool:
        return to_bool(self.get_option(ClusterKey.AUTOSAVER_ENABLED))


    def is_pvp_enabled(self) -> bool:
        return to_bool(self.get_option(ClusterKey.PVP))


    def game_mode(self) -> Mode:
        res = self.get_option(ClusterKey.GAME_MODE)
        if isinstance(res, Mode):
            return res
        return Mode(res)


    def is_pause_when_emty_enabled(self) -> bool:
        return to_bool(self.get_option(ClusterKey.PAUSE_WHEN_EMPTY))


    def is_vote_enabled(self) -> bool:
        return to_bool(self.get_option(ClusterKey.VOTE_ENABLED))


    def set_max_snapshots(self, max_snapshots: Union[int, None]) -> None:
        if isinstance(max_snapshots, int):
            check_positiv(max_snapshots, 'The maximum snapshots')
        self.add_option(ClusterKey.MAX_SNAPSHOTS, max_snapshots)


    def set_console_enabled(self, console_enabled: Union[bool, None]) -> None:
        self.add_option(ClusterKey.CONSOLE_ENABLED, console_enabled)


    def set_shard_enabled(self, shard_enabled: Union[bool, None]) -> None:
        self.add_option(ClusterKey.SHARD_ENABLED, shard_enabled)


    def set_bind_ip(self, bind_ip: Union[str, None]) -> None:
        if isinstance(bind_ip, str):
            check_ip(bind_ip)
            bind_ip = bind_ip.strip()
        self.add_option(ClusterKey.BIND_IP, bind_ip)


    def set_master_ip(self, master_ip: str) -> None:
        if isinstance(master_ip, str):
            check_ip(master_ip)
            master_ip = master_ip.strip()
        self.add_option(ClusterKey.MASTER_IP, master_ip)


    def set_master_port(self, master_port: Union[int, None]) -> None:
        if isinstance(master_port, int):
            check_positiv(master_port, 'The master port')
        self.add_option(ClusterKey.MASTER_PORT, master_port)


    def set_cluster_key(self, cluster_key: Union[str, None]) -> None:
        if isinstance(cluster_key, str):
            cluster_key = cluster_key.strip()
        self.add_option(ClusterKey.CLUSTER_KEY, cluster_key)


    def set_steam_group_only(self, steam_group_only: Union[bool, None]) -> None:
        self.add_option(ClusterKey.STEAM_GROUP_ONLY, steam_group_only)


    def set_steam_group_id(self, steam_group_id: Union[bool, None]) -> None:
        self.add_option(ClusterKey.STEAM_GROUP_ID, steam_group_id)


    def set_steam_group_admin(self, steam_group_admins: Union[bool, None]) -> None:
        self.add_option(ClusterKey.STEAM_GROUP_ADMINS, steam_group_admins)


    def set_offline_enabled(self, offline_enabled: Union[bool, None]) -> None:
        self.add_option(ClusterKey.OFFLINE, offline_enabled)


    def set_tick_rate(self, tick_rate: Union[TickRate, None]) -> None:
        self.add_option(ClusterKey.TICK_RATE, tick_rate)


    def set_withelist_slots(self, slots: Union[int, None]) -> None:
        if isinstance(slots, int):
            check_positiv(slots, 'The number of withelist slots')
        self.add_option(ClusterKey.WHITELIST_SLOTS, slots)


    def set_password(self, password: Union[str, None]) -> None:
        if isinstance(password, str):
            password = password.strip()
        self.add_option(ClusterKey.PASSWORD, password)


    def set_name(self, name: str) -> None:
        name = name.strip()
        check_len(name, 'The cluster name')
        self.add_option(ClusterKey.NAME, name)

    
    def set_description(self, description: Union[str, None]) -> None:
        if isinstance(description, str):
            description = description.strip()
        self.add_option(ClusterKey.DESCRIPTION, description)


    def set_lan_only(self, lan_only: Union[bool, None]) -> None:
        self.add_option(ClusterKey.LAN_ONLY, lan_only)


    def set_intention(self, intention: Union[Intention, None]) -> None:
        self.add_option(ClusterKey.INTENTION, intention)


    def set_autosaver_enabled(self, autosaver: Union[bool, None]) -> None:
        self.add_option(ClusterKey.AUTOSAVER_ENABLED, autosaver)


    def set_max_player(self, max_player: Union[int, None]) -> None:
        if isinstance(max_player, int):
            check_strict_positiv(max_player, 'The number maximum of player')
        self.add_option(ClusterKey.MAX_PLAYERS, max_player)


    def set_pvp_enabled(self, pvp: Union[bool, None]) -> None:
        self.add_option(ClusterKey.PVP, pvp)


    def set_game_mode(self, game_mode: Union[Mode, None]) -> None:
        self.add_option(ClusterKey.GAME_MODE, game_mode)


    def set_pause_when_empty(self, pause_when_empty: Union[bool, None]) -> None:
        self.add_option(ClusterKey.PAUSE_WHEN_EMPTY, pause_when_empty)


    def set_vote_enabled(self, vote_enabled: Union[bool, None]) -> None:
        self.add_option(ClusterKey.VOTE_ENABLED, vote_enabled)
    
    
    def check_master_ip(self) -> bool:
        if not self.is_shard_enabled():
            return True

        ip = self.master_ip()
        if ip == None:
            return False
        return bool(len(ip))


    def check_cluster_key(self) -> bool:
        if not self.is_shard_enabled():
            return True
        key = self.cluster_key()
        if key == None:
            return False
        return bool(len(key))


    def check_name(self) -> bool:
        name = self.name()
        if name == None:
            return False
        return bool(len(name))
    

class Server(ConfigurationFile):
    def __init__(self):
        super().__init__()


    def is_master(self) -> Union[bool, None]:
        master = self.get_option(ServerKey.IS_MASTER)
        if master == None:
            return None
        return to_bool(master)


    def name(self) -> Union[str, None]:
        if self.is_master():
            return '[SHDMASTER]'
        return self.get_option(ServerKey.NAME)


    def authentication_port(self) -> int: 
        return int(self.get_option(ServerKey.AUTHENTICATION_PORT))


    def master_port(self) -> int:
        return int(self.get_option(ServerKey.MASTER_PORT))


    def port(self) -> int:
        return int(self.get_option(ServerKey.PORT))


    def set_master_enabled(self, is_master: Union[bool, None]) -> None:
        self.add_option(ServerKey.IS_MASTER, is_master)
        if self.is_master():
            self.remove_option(ServerKey.NAME)


    def set_authentication_port(self, port: Union[int, None]) -> None:
        if port != None:
            check_positiv(port, 'The authentication port')
        self.add_option(ServerKey.AUTHENTICATION_PORT, port)


    def set_name(self, name: Union[str, None]) -> None:
        if self.is_master():
            return
        if isinstance(name, str):
            name = name.strip()
            check_len(name, 'The name of the slave server ')
        self.add_option(ServerKey.NAME, name)


    def set_master_port(self, port: Union[int, None]) -> None:
        if port != None:
            check_positiv(port, 'The master port')
        self.add_option(ServerKey.MASTER_PORT, port)


    def set_port(self, port: Union[int, None]) -> None:
        if port != None:
            check_positiv(port, 'The server port')
        self.add_option(ServerKey.PORT, port)


    def check_name(self) -> bool:
        is_master = self.is_master() 
        if None == is_master :
            return True
        if is_master:
            return True

        name = self.name()
        if name == None:
            return False
        return bool(len(name))

    def check_is_master(self, cluster: Cluster) -> bool:
        if not cluster.is_shard_enabled():
            return True
        return None != self.is_master()
