from typing import Union
from . import ssh
from .slpp import slpp
from . import constant
import zipfile
import tempfile
import os
import lupa
from lupa import LuaRuntime


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
        if new_value == None:
            self.__selected_value = None
            return
        if self.default == new_value.data:
            self.__selected_value = None
            return
        self.__selected_value = new_value

            
        
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

class Credential:
    def __init__(self,username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return '{} {}'.format(self.username, self.password)


class ModulesManager:
    def __init__(self, ssh_session: ssh.SshSession):
        self.__installed_module = []
        self.__ssh = ssh_session
        self.__update_installed_module()
        self.__server_modules = []


    def __module_info(self, module_id: str) -> Module:
        path = constant.MOD_INFO_PATH + module_id + '/modinfo.lua'
        file = self.__ssh.get_file_content(path)
        if file == None:
            return Module(None, module_id, None, None)
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



        mod = Module(lua.get('name'), module_id, lua.get('description'), options)
        return mod
        
    def __update_installed_module(self) -> None:
        res = str(self.__ssh.get_file_content(constant.GAME_DIR+'mods/dedicated_server_mods_setup.lua'))
        if res == None:
            return
        self.__installed_module.clear()
        for line in res.splitlines():
            if line.strip().startswith('ServerModSetup'):
                self.__installed_module.append(line.split('"')[1])
        

    def all_available_modules(self) -> list[Module]:
        res = []
        for name in self.__installed_module:
            res.append(self.__module_info(name))
        return res

    def add_available_module(self, module_id: str) -> None:
        for n in self.__installed_module:
            if n == module_id:
                return
        self.__installed_module.append(module_id)


    def remove_available_module (self, module: Module) -> None:
        for m in self.all_available_modules():
            if m == module:
                self.__ssh.remove(constant.MOD_INFO_PATH+module.identity)
                self.__installed_module.remove(module.identity)
                self.__update_dedicated_mod_conf_file()
                return

    def __extract(self, zip_content:bytes)-> str:
        f = tempfile.TemporaryFile()
        f.write(zip_content)
        zipfile.ZipFile(f).extract('modinfo.lua')
        res = open('modinfo.lua').read()
        os.remove('modinfo.lua')
        f.close()
        return res


    def __update_dedicated_mod_conf_file(self) -> None:
        res:str = ''
        for m in self.__installed_module:
            res += 'ServerModSetup("{}")\n'.format(m)
        self.__ssh.create_file(constant.GAME_DIR + 'mods/dedicated_server_mods_setup.lua', res)

    def __update_cached_module(self, cr: Credential) -> None:
        cmd = ''
        for m in self.__installed_module:
            cmd += '+workshop_download_item {} {} validate '.format(constant.STEAM_GAME_ID, m)

        self.__ssh.remove(constant.CONF_DIR+'module')
        self.__ssh.exec('steamcmd +force_install_dir {} +"login {}" {} +quit'.format(constant.CONF_DIR+'module/', str(cr), cmd))
        
        for mod in self.__ssh.list_files(constant.MOD_INFO_PATH):
            for file in self.__ssh.list_files(constant.MOD_INFO_PATH+mod):
                if file != 'modinfo.lua' and not file.endswith('legacy.bin'):
                    self.__ssh.remove(constant.MOD_INFO_PATH+mod+'/'+file)
                elif file.endswith('legacy.bin'):
                    content = self.__extract(bytes(self.__ssh.get_file_content(constant.MOD_INFO_PATH+mod+'/'+file)))
                    self.__ssh.create_file(constant.MOD_INFO_PATH+mod+'/modinfo.lua', content)
                    self.__ssh.remove(constant.MOD_INFO_PATH+mod+'/'+file)
        
        
    def write_available_module(self, cr: Credential):
        self.__update_dedicated_mod_conf_file()
        self.__update_cached_module(cr)
            


    def install_mod(self, cluster_name:str) -> None:
        cmd = 'cd ' + constant.GAME_DIR + 'bin64 ; ./dontstarve_dedicated_server_nullrenderer_x64 -cluster ' + cluster_name + ' -shard {} -only_update_server_mods'
        self.__ssh.exec(cmd.format('Master'))
        if self.__ssh.is_exist(constant.CLUSTER_DIRECTORY + cluster_name + '/Cave'):
            self.__ssh.exec(cmd.format('Cave'))
        

    def add_server_module(self, module: Module) -> None:
        for m in self.__server_modules:
            if m == module:
                return
        self.__server_modules.append(module)

    def remove_server_module(self, module: Module) -> None:
        pass
        for m in self.__server_modules:
            if m == module:
                self.__server_modules.remove(module)

    def to_str(self, cluster_name)-> None:
        res = {}
        for mod in self.__server_modules:
            configuration = {}
            for opt in mod.options:
                if opt.value() != None:
                    configuration[opt.name] = opt.value().data
            all_config = {}
            if len(configuration):
                all_config = {'enabled':True, 'configuration_options' : configuration}
            else:
                all_config = {'enabled':True}

            res["workshop-{}".format(mod.identity)] =  all_config
        if not len(res):
            return
        lua = 'return ' + slpp.slpp.encode(res)
        self.__ssh.create_file(constant.CLUSTER_DIRECTORY + cluster_name + '/Master/modoverrides.lua', lua)
        self.__ssh.create_file(constant.CLUSTER_DIRECTORY + cluster_name + '/Cave/modoverrides.lua', lua)




