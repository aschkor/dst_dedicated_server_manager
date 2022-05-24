import argparse
from typing import Union
import module.ssh as ssh
import module.configuration_file as configuration_file
import module.worldgen as worldgen
import module.mods as mods
import sys

def main_menu(ssh: ssh.SshSession) -> bool:
    options = ["Start exisiting cluster","Create new shard cluster","Remove cluster", "Add token","Manage modules"]
    if ssh.has_started_cluster():
        options[0] = "Stop current cluster"

    menu = create_menu(options)
    choice = int_input(dict_to_str(menu), len(options))
    if choice == 0:
        return False
    if choice == 1 :
        if not ssh.has_started_cluster():
            start_cluster(ssh)
            return False
        else:
            print("Please wait for the cluster to stop")
            ssh.stop_servers()
    elif choice == 2:
        create_cluster(ssh)
    elif choice == 3:
        remove_cluster(ssh)
    elif choice == 4:
        add_token(ssh)
    elif choice == 5:
        manage_module(ssh)
    return True
    

def manage_module(ssh_session: ssh.SshSession) -> None:

    menu = create_menu(["Installed module", "Install module", "Uninstall module"])
    while True :
        res = int_input(dict_to_str(menu), len(menu))
        if res == 0:
            return
        if res == 1:
            view_module(ssh_session)
        if res == 2:
            add_module(ssh_session)
        if res == 3:
            rm_module(ssh_session)

def rm_module(ssh_session: ssh.SshSession)-> None:
    manager = mods.ModulesManager(ssh_session)
    modules = manager.all_available_modules()
    names = get_module_list_name(modules)
    menu = create_menu(names)
    res = int_input(dict_to_str(menu), len(menu))
    if res == 0:
        return
    manager.remove_available_module(modules[res - 1])


def add_module(ssh_session: ssh.SshSession) -> None:
    manager = mods.ModulesManager(ssh_session)
    user = input_value('Enter your steam username')
    password = input_value('Enter your steam password')
    while True:
        res = input_value('Enter module Id (Enter 0 to return)')
        if res == '0':
            manager.write_available_module(mods.Credential(user,password))
            return
        #guard_code = input_value('Enter your steam guard code')
        manager.add_available_module(res)
    
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

def view_module(ssh_session: ssh.SshSession) -> None:
    manager = mods.ModulesManager(ssh_session)
    res = get_module_list_name(manager.all_available_modules())
    line = ''
    for l in res:
        line = line + l + '\n\n'
    print(line)
    

def get_clusters(ssh_session: ssh.SshSession) -> list[ssh.Cluster]:
    print('Retrieve available cluster, please wait...')
    return ssh_session.servers()
    

def remove_cluster(ssh_session: ssh.SshSession) -> None:
    names = []
    for cluster in get_clusters(ssh_session):
        if cluster.cluster.name():
            names.append(cluster.cluster.name())
    menu = create_menu(names)
    choice = int_input(dict_to_str(menu), len(names))
    if choice == 0:
        return
    ssh_session.rm_cluster(names[choice -1])


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
    return select

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



def add_mods(ssh_session: ssh.SshSession) -> Union[mods.ModulesManager, None]:
    menu = create_menu(['Add module'])
    res = int_input(dict_to_str(menu), 1)

    if res == 0:
        return None

    manager = mods.ModulesManager(ssh_session)
    modules = manager.all_available_modules()
    names = get_module_list_name(modules)
    selected_module = []
    for s in select_module(names):
        selected_module.append(modules[s - 1])
    configure_module(selected_module)
    for m in selected_module:
        manager.add_server_module(m)
    return manager


def create_cluster(ssh_session: ssh.SshSession) -> None:
    name = in_name(ssh_session)
    if name == None:
        return
    description = in_description()
    if description == None:
        return
    password = in_password()
    if password == None:
        return
    token = token_menu(ssh_session)
    if token == None:
        return
    manager = add_mods(ssh_session)

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
    gen.set_preset_generation(worldgen.Preset.CAVE)
    gen.set_preset_settings(worldgen.Preset.CAVE)
    cave = configuration_file.Server()
    cave.set_authentication_port(8767)
    cave.set_master_port(27017)
    cave.set_port(11000)
    cave.set_master_enabled(False)
    ssh_session.add_server(ssh.Cluster(cl, ssh.Server(master, worldgen.Overworld()), ssh.Server(cave, gen), token, manager))


def is_token_already_exits(name: str, ssh: ssh.SshSession) -> bool:
    tokens = ssh.get_available_tokens()
    for token in tokens:
        if token.owner == name:
            return True
    return False

    

def add_token(ssh_session: ssh.SshSession) ->  Union[ssh.ClusterToken, None]:
    path = input_value('Enter token path (enter 0 to return)')
    if path == '0':
        return 
    content = ''
    with open(path,'r') as f:
        content = f.read()

    name = input_value('Enter the name of the token owner (enter 0 to return)')
    if name == '0':
        return 
    if is_token_already_exits(name, ssh_session):
        print("The token {} already exist".format(name))
        name = ''
        
    token = ssh.ClusterToken(name, content)
    ssh_session.add_token(token)
    return token


def token_menu(ssh_session: ssh.SshSession) -> Union[ssh.ClusterToken, None]:
    print('Available token')
    menu = create_menu(['Add new token', 'Use exisiting token'])
    choice = int_input(dict_to_str(menu), len(menu))
    token = None

    if choice == 0:
        return None
    if choice == 1:
        token = add_token(ssh_session)
    elif choice == 2:
        token = available_token(ssh_session)
    else:
        return token_menu(ssh_session)
    if token == None:
        return token_menu(ssh_session)

    return token

    
def available_token(ssh_session: ssh.SshSession) -> Union[ssh.ClusterToken, None]:
    tokens = ssh_session.get_available_tokens()
    tokens_name = []
    for token in tokens:
        tokens_name.append(token.owner)
    menu = create_menu(tokens_name)
    res = int_input(dict_to_str(menu), len(menu))
    if res == 0:
        return None
    return tokens[ res -1]

def start_cluster(ssh_session: ssh.SshSession) -> None:
    clusters = get_clusters(ssh_session)
    cluster_infos = []
    cluster_names = []

    for cluster in clusters :
        if cluster.cluster.name() == None or cluster.token == None:
            continue
        if cluster.token.key == None:
            continue

        info = str(cluster.cluster.name())
        cluster_names.append(info)
        if cluster.cluster.password():
            info = info + ', password {}'.format(cluster.cluster.password())
        if cluster.cluster.description():
            info = info + ', description: {}'.format(cluster.cluster.description())
        if cluster.token.owner:
            info = info + ', owner: {}'.format(cluster.token.owner)
        cluster_infos.append(info)
        
    menu = create_menu(cluster_infos)
    print("Choose a cluster to start:")
    choice = int_input(dict_to_str(menu), len(clusters))
    if choice == 0:
        main_menu(ssh_session)
        return
    ssh_session.start_servers(cluster_names[choice-1])


def default_shard_cluster(name, password ,token) -> ssh.Cluster:
    cl = configuration_file.Cluster()
    cl.set_name(name)
    cl.set_password(password)
    cl.set_master_ip('127.0.0.1')
    cl.set_shard_enabled(True)
    cl.set_cluster_key('YouAreJustASlave')
    master = configuration_file.Server()
    master.set_master_enabled(True)
    gen = worldgen.Underworld()
    gen.set_preset_generation(worldgen.Preset.CAVE)
    gen.set_preset_settings(worldgen.Preset.CAVE)
    cave = configuration_file.Server()
    cave.set_authentication_port(8767)
    cave.set_master_port(27017)
    cave.set_port(11000)
    cave.set_master_enabled(False)
    return ssh.Cluster(cl, ssh.Server(master, worldgen.Overworld()), ssh.Server(cave, gen), token)


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

def in_name(ssh_session: ssh.SshSession) -> Union[str, None]:
    res = input_value('Enter the cluster name (enter 0 to return)')
    if res == '0':
        return None
    print('Name checking avaibility')
    clusters = get_clusters(ssh_session)
    for cluster in clusters:
        if res == cluster.cluster.name():
            print('This name is not available')
            return in_name(ssh_session)
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
    session = ssh.SshSession(args.ip_address, args.username, args.password)
    
    while(main_menu(session)):
        pass
