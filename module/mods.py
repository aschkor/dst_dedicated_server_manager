from typing import Union
from .import ssh
from . import constant
from pathlib import PurePosixPath as Path
from lupa import LuaRuntime
import random

try:
    from lupa import LuaRuntime
except:
    print('install lupa module')
    import os
    try:
        os.system('python3 -m pip install lupa')
    except:
        try:
            os.system('python -m pip install lupa')
        except:
            print('Pip might not be installed, please install pip')
            import sys
            sys.exit()
    from lupa import LuaRuntime

try:
    import slpp
except:
    print('install slpp module')
    import os
    try:
        os.system('python3 -m pip install slpp')
    except:
        try:
            os.system('python -m pip install slpp')
        except:
            print('Pip might not be installed, please install pip')
            import sys
            sys.exit()
    import slpp
# Copied from https://github.com/dly2424/DST_Dedicated_Mod_Manager
table_parse_function = """
function printTable(t, f)
   new_string = ''
   local function printTableHelper(obj, cnt)
      local cnt = cnt or 0
      if type(obj) == "table" then
         new_string = new_string .. "\\n" .. string.rep("\\t", cnt) .. "{\\n"
         cnt = cnt + 1
         for k,v in pairs(obj) do
            if type(k) == "string" then
               new_string = new_string .. string.rep("\\t",cnt) .. '["'..k..'"]' .. ' = '
            end
            if type(k) == "number" then
               new_string = new_string .. ''
            end
            printTableHelper(v, cnt)
            new_string = new_string .. ",\\n"
         end
         cnt = cnt-1
         new_string = new_string .. string.rep("\\t", cnt) .. "}"
      elseif type(obj) == "string" then
         new_string = new_string .. string.format("%q", obj)
      else
         new_string = new_string .. tostring(obj)
      end 
	  return new_string
   end
   if f == nil then
      var = printTableHelper(t)
	  return var
   else
      io.output(f)
      io.write("return")
      printTableHelper(t)
      io.output(io.stdout)
   end
end
new_string2 = printTable(configuration_options)
"""
# End of the copy

_modinfo = 'modinfo.lua'
_legacy_mod_name = 'workshop-{}'
    
class Value:
    def __init__(self, data, description: str):
        self.data = data
        self.description = description
        
class Option:
    def __init__(self, name:str, label:Union[str, None], hover:Union[str, None], default, available_value: list[Value]):
        self.name = name
        self.label = label
        self.hover = hover
        self.default = default
        self.available_value = available_value
        self.__selected_value = None

    def value(self) -> Union[None, Value]:
        return self.__selected_value


    def select_value(self, new_value: Union[Value, None]) -> None :
        if new_value is None:
            self.__selected_value = None
            return
        if self.default == new_value.data:
            self.__selected_value = None
            return
        self.__selected_value = new_value

    def dict(self):
        if self.__selected_value is None:
            return None
        return {self.name: self.__selected_value.data}

        
class Module:
    def __init__(self, name: Union[str, None], identity: str, description: Union[str, None] ,options):
        self.name = name
        self.identity = identity
        self.options = options
        self.description = None
        if description != None:
            self.description = description.replace('\n',' ')

    def __eq__(self, other):
        return self.identity == other.identity

    def dict(self):
        value = {}
        for opt in self.options:
            val = opt.dict()
            if val is not None:
                value.update(val)

        options = {'enabled':True}
        if len(value):
            options.update({'configuration_options': value})
        return {'{}'.format(_legacy_mod_name.format(self.identity)):  options}
        

def add(module_id: str) -> None:
    names = __get_installed_module()
    names.append(module_id)
    ssh.create_file(constant.INSTALL_CONFIG_FILE_MOD_PATH, __format_dedi_file(names))

def remove(module_id:str) -> None:
    names = __get_installed_module()
    names.remove(module_id)
    ssh.create_file(constant.INSTALL_CONFIG_FILE_MOD_PATH, __format_dedi_file(names))

    if ssh.is_exist(constant.LEGACY_MODS_DIR / _legacy_mod_name.format(module_id)):
        ssh.remove(constant.LEGACY_MODS_DIR / _legacy_mod_name.format(module_id))
    
def installed() -> list[Module]:
    cluster_name = __get_free_cluster_name()
    _ = __download(cluster_name)
    ugc = constant.ugc_mods_path(cluster_name)

    res = []
    for name in __get_installed_module():
        if ssh.is_exist(ugc / name / _modinfo):
            res.append(__module_info(ugc / name))
        elif ssh.is_exist(constant.LEGACY_MODS_DIR / _legacy_mod_name.format(name) / _modinfo) :
            res.append(__module_info(constant.LEGACY_MODS_DIR / _legacy_mod_name.format(name)))
        else:
            raise RuntimeError('Impossible to find the {} of module {}'.format(_modinfo, name))
    return res


def install(cluster_name: str, modules: list[Module], is_master:bool = True):
    if not len(modules):
        return
    res = {}
    for m in modules:
        res.update(m.dict())
    path = constant.CLUSTER_DIRECTORY / cluster_name
    if is_master:
        path = path / constant.MASTER_NAME_DIR
    else:
        path = path / constant.CAVE_NAME_DIR
    path = path / 'modoverrides.lua'
    ssh.create_file(path, 'return ' + slpp.slpp.encode(res))


def __get_installed_module() -> list[str]:
    conf_file = ssh.get_file_content(constant.INSTALL_CONFIG_FILE_MOD_PATH)
    if conf_file is None:
        return []
    res = []
    for line in conf_file.splitlines():
        if line.strip().startswith('ServerModSetup'):
            name = line.split('"')[1]
            res.append(name)
    return res


def __format_dedi_file(modules_id: list[str]) -> str:
    res = ''
    for m in modules_id:
        res += 'ServerModSetup(\"{}\")\n'.format(m)
    return res
    

def __module_info(path: Path) -> Module:
    path = path / _modinfo
    module_id = path.parent.stem
    if module_id.startswith('workshop-'):
        module_id = module_id.split('-')[1]

    file = ssh.get_file_content(path)
    if file is None:
        raise RuntimeError('Impossible to read {}'.format(path))
    l = LuaRuntime(unpack_returned_tuples=True)
    l.execute(file)
    l.execute(table_parse_function)
    lua = slpp.slpp.decode('{\n' + file + '\n}')
    option = slpp.slpp.decode(l.eval('new_string2'))
    options:list[Option] = []
    if option != None:
        for opt in option:
            values = []
            value = opt.get('options')
            if value != None:
                for v in value:
                    values.append(Value(v.get('data'), v.get('description')))
            options.append(Option(opt.get('name'), opt.get('label'), opt.get('hover'), opt.get('default'), values))
    return Module(lua.get('name'), module_id, lua.get('description'), options)

def __get_free_cluster_name() -> str:
    res = chr(random.randint(ord('A'), ord('Z')))
    while ssh.is_exist(constant.CLUSTER_DIRECTORY / res):
        res = res + chr(random.randint(ord('A'), ord('Z'))) 
    return res


class __download:
    def __init__(self, cluster_name:str):
        self.__cluster_name = cluster_name
        ssh.execute(constant.CMD_INSTALL_MODS.format(self.__cluster_name.replace(' ', '\ ')))

    def __del__(self):
        ssh.remove(constant.CLUSTER_DIRECTORY / self.__cluster_name)
        ssh.remove(constant.UGC_DIR / self.__cluster_name)

        
