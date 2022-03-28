import argparse
from typing import Union
import module.ssh as ssh
import module.configuration_file as configuration_file
import module.worldgen as worldgen
import module.mods as mods
import module.cluster as cluster
import module.token as token
import sys

def main_menu() -> bool:
    options = ["Start exisiting cluster","Create new shard cluster","Remove cluster", "Add token","Manage modules"]
    if cluster.is_started():
        options[0] = "Stop current cluster"
    choice = int_menu(options)
    if choice == 0:
        return False
    if choice == 1 :
        if not cluster.is_started():
            start_cluster()
            return False
        else:
            print("Please wait for the cluster to stop")
            cluster.stop()
    elif choice == 2:
        create_cluster()
    elif choice == 3:
        remove_cluster()
    elif choice == 4:
        add_token()
    elif choice == 5:
        manage_module()
    return True
    

def manage_module() -> None:

    menu = create_menu(["Installed module", "Install module", "Uninstall module"])
    while True :
        res = int_input(dict_to_str(menu), len(menu))
        if res == 0:
            return
        if res == 1:
            view_module()
        if res == 2:
            add_module()
        if res == 3:
            rm_module()

def int_menu(choices: list[str]) -> int:
    menu = create_menu(choices)
    return int_input(dict_to_str(menu), len(choices))

def rm_module()-> None:
    modules = all_mods()
    res = int_menu(get_module_list_name(modules))
    if res == 0:
        return
    mods.remove(modules[res - 1].identity)


def add_module() -> None:
    while True:
        res = input_value('Enter module Id (Enter 0 to return). See https://steamcommunity.com/sharedfiles/filedetails/?id=764296557 to know how get the module identity')
        if res == '0':
            return
        mods.add(res)
    
def get_module_list_name(modules: list[mods.Module]) -> list[str]:
    res = []
    for module in modules:
        line = ''
        if module.name != None:
            if len(module.name):
                line = module.name
        if module.description != None:
            if len(module.description):
                    if len(line):
                        line = line + ": {}".format(module.description)
                    else:
                        line = module.description
        if len(line):
            if not line.endswith('.'):
                line = line + '.'
            line = line + ' Identity: {}'.format(module.identity)
        else:
            line = module.identity
        res.append(line)
    return res

def all_mods() -> list[mods.Module]:
    print('Retrieve available modules. Please wait...')
    return mods.installed()


def view_module() -> None:
    res = get_module_list_name(all_mods())
    line = ''
    for l in res:
        line = line + l + '\n\n'
    print(line)
    

def get_clusters() -> list[cluster.Cluster]:
    print('Retrieve available cluster, please wait...')
    return cluster.clusters()
    

def remove_cluster() -> None:
    names = []
    for cl in get_clusters():
        if cl.settings.name():
            names.append(cl.settings.name())
    choice = int_menu(names)
    if choice == 0:
        return
    cluster.remove(names[choice -1])


def select_module(names) -> list[int]:
    select = []
    menu = create_menu(names)
    while(True):
        choice = int_input(dict_to_str(menu,select), len(names))
        if choice == 0:
            return select
        if select.count(choice):
            select.remove(choice)
        else:
            select.append(choice)

def configure_value(option):
    names = []
    for v in option.available_value:
        names.append(v.description)
    menu = create_menu(names)
    print('Select a value')
    choice = int_input(dict_to_str(menu), len(names))
    if choice == 0:
        return
    option.select_value(option.available_value[choice -1])


def configure_option(options):
        names = []
        for opt in options:
            n = ''
            if opt.label != None:
                n = opt.label
            if opt.hover != None:
                n = n + '. description {}'.format(opt.hover)
            if not len(n):
                n = opt.name
            names.append(n)

        menu = create_menu(names)
        while(True):
            print('Select a module to configure')
            choice = int_input(dict_to_str(menu), len(names))
            if choice == 0:
                break
            opt = options[choice -1]
            print('You have selected {}'.format(names[choice -1]))
            configure_value(opt)


def configure_module(modules) -> None:
    selected_name = get_module_list_name(modules)
    selected_menu = create_menu(selected_name)
    while(True):
        choice = int_input(dict_to_str(selected_menu), len(selected_name))
        if choice == 0:
            break
        options = modules[choice - 1].options
        configure_option(options)



def add_mods() -> list[mods.Module]:
    menu = create_menu(['Add module'])
    res = int_input(dict_to_str(menu), 1)

    if res == 0:
        return []

    modules = all_mods()
    names = get_module_list_name(modules)
    selected_module = []
    for s in select_module(names):
        selected_module.append(modules[s - 1])
    if len(selected_module):
        configure_module(selected_module)
    return selected_module


def create_cluster() -> None:
    name = in_name()
    if name is None:
        return
    description = in_description()
    if description is None:
        return
    password = in_password()
    if password is None:
        return
    token = token_menu()
    if token is None:
        return
    modules = add_mods()

    cl = configuration_file.Cluster()
    cl.set_name(name)
    cl.set_password(password)
    cl.set_master_ip('127.0.0.1')
    cl.set_shard_enabled(True)
    cl.set_cluster_key('YouAreJustASlave')
    cl.set_password(password)
    cl.set_pause_when_empty(True)
    master = configuration_file.Server()
    master.set_master_enabled(True)
    gen = worldgen.Underworld()
    gen.set(worldgen.Global.GENERATION_PRESET, worldgen.Preset.CAVE)
    gen.set(worldgen.Global.SETTING_PRESET,worldgen.Preset.CAVE)
    cave = configuration_file.Server()
    cave.set_authentication_port(8767)
    cave.set_master_port(27017)
    cave.set_port(11000)
    cave.set_master_enabled(False)
    cluster.add(cluster.Cluster(cl, token ,cluster.Server(master, worldgen.Overworld(), modules), cluster.Server(cave, gen, modules)))


def is_token_already_exits(name: str) -> bool:
    tks = token.tokens()
    for tk in tks:
        if tk.owner == name:
            return True
    return False

    

def add_token() ->   None:
    path = input_value('Enter token path (enter 0 to return)')
    if path == '0':
        return 
    content = ''
    with open(path,'r') as f:
        content = f.read()

    name = input_value('Enter the name of the token owner (enter 0 to return)')
    if name == '0':
        return 
    if is_token_already_exits(name):
        print("The token {} already exist".format(name))
        name = ''
        
    tk = token.Token(name, content)
    tk.add_to_available_token()


def token_menu() -> Union[token.Token, None]:
    while True:
        print('Available token')
        choice = int_menu(['Add new token', 'Use exisiting token'])
        if choice == 0:
            return None
        if choice == 1:
            token = add_token()
        elif choice == 2:
            return select_token()

    
def select_token() -> Union[token.Token, None]:
    tks = token.tokens()
    tokens_name = []
    for tk in tks:
        tokens_name.append(tk.owner)
    menu = create_menu(tokens_name)
    res = int_input(dict_to_str(menu), len(menu))
    if res == 0:
        return None
    return tks[ res -1]

def start_cluster() -> None:
    clusters = get_clusters()
    cluster_infos = []
    cluster_names = []

    for clus in clusters :
        if clus.settings.name() is None or clus.token is None:
            continue
        if clus.token.content is None:
            continue

        info = str(clus.settings.name())
        cluster_names.append(info)
        if clus.settings.password():
            info = info + ', password {}'.format(clus.settings.password())
        if clus.settings.description():
            info = info + ', description: {}'.format(clus.settings.description())
        if clus.token.owner:
            info = info + ', owner: {}'.format(clus.token.owner)
        cluster_infos.append(info)
        
    menu = create_menu(cluster_infos)
    print("Choose a cluster to start:")
    choice = int_input(dict_to_str(menu), len(clusters))
    if choice == 0:
        main_menu()
        return
    cluster.start(cluster_names[choice-1])


def format_enum(enum) -> str:
    return enum.name.lower().capitalize().replace('_',' ')


def enum_to_str(enum) -> list[str]:
    res: list[str] = []
    for e in enum:
        res.append(format_enum(e))
    return res


def get_enum_value(enum, index):
    i = 0
    for e in enum:
        if i == index:
            return e
        i = i +1
    return None


def create_menu(options: list[str], has_return:bool = True):
    res = {}
    if has_return:
        res = {0 : 'return'}
    i = 1
    for e in options:
        res.update({i : e})
        i = i + 1
    return res


def dict_to_str(dic, highlight:list[int] =  []) -> str:
    res:str = ''
    i = 0 
    for key, value in dic.items():
        if highlight.count(i):
            res += '* '+str(key) + ' -> ' + value + '\n'
        else:
            res += str(key) + ' -> ' + value + '\n'
        i = i + 1
    return res


def input_value(consign, required: bool = True):
        try:
            res = input(consign + '\n').strip()
            if required and not len(res):
                return input_value(consign, required)
        except KeyboardInterrupt:
            sys.exit()
        return res

def int_input(consign , choice_number: int, required: bool = True) -> int:
    try:
        res = int(input_value(consign, required))
        if res >= 0 and res <= choice_number:
            return res
        return int_input(consign, choice_number, required)
    except:
        print ('The value must be an integer')
        return int_input(consign, choice_number, required)

def in_name() -> Union[str, None]:
    res = input_value('Enter the cluster name (enter 0 to return)')
    if res == '0':
        return None
    print('Name checking avaibility')
    clusters = get_clusters()
    for cluster in clusters:
        if res == cluster.settings.name():
            print('This name is not available')
            return in_name()
    return res

def in_description() -> Union[str, None]:
    res = input_value('Enter a description (optional, enter an empty string to ignore or 0 to return)', False)
    if res == '0':
        return None
    return res

def in_password() -> Union[str, None]:
    res =  input_value('Enter a password (optional, enter an empty string to ignore or 0 to return)', False)
    if res == '0':
        return None
    return res

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Dont starve together dedicated server manager')

    parser.add_argument('--ip_address', '-i', required=True, help = 'Dedicated server ip address')
    parser.add_argument('--username', '-u', required=True, help = 'Server username')
    parser.add_argument('--password', '-p', required=True, help = 'Password of the server user')
    args = parser.parse_args()
    print('Welcome to the Don\'t Starve Together dedicated server manager')
    print('Please wait to the server connexion...')
    
    ssh.SshSession(args.ip_address, args.username, args.password)
    
    while(main_menu()):
        pass
