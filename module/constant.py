from pathlib import PurePosixPath as Path
GAME_DIR = Path('~/Steam/steamapps/common/Don\\\'t Starve Together Dedicated Server')
EXECUTABLE = Path('dontstarve_dedicated_server_nullrenderer_x64')
CLUSTER_DIRECTORY = Path('~/.klei/DoNotStarveTogether')
CAVE_NAME_DIR = Path('Cave')
MASTER_NAME_DIR = Path('Master')
LEGACY_MODS_DIR = GAME_DIR / 'mods'
CONF_DIR = Path('~/.config/dst_config')
TOKEN_DIR = CONF_DIR / 'token'
STEAM_GAME_ID = '322330'
CMD_FILE_EXSIST = '[ -f {} ] && echo "true" ; [ ! -f {} ] && echo "false"'
CMD_DIR_EXSIST = '[ -d {} ] && echo "true" ; [ ! -f {} ] && echo "false"'
CMD_LIST = 'ls {}'
CMD_REMOVE = 'rm -r {}'
CMD_READ_FILE = 'cat {}'
CMD_CREATE_DIR = 'mkdir -p {}'
CMD_CREATE_FILE = 'echo \'{}\' > {}'
CMD_START_SERVER = 'cd '+str(GAME_DIR/'bin64').replace(' ','\ ') + '; screen -dmS {} ./dontstarve_dedicated_server_nullrenderer_x64 -cluster {} -shard {}'
CMD_INSTALL_MODS = 'cd '+str(GAME_DIR/'bin64').replace(' ','\ ') + '; ./dontstarve_dedicated_server_nullrenderer_x64 -cluster {} -only_update_server_mods'
CMD_STOP_SERVER = 'screen -S {} -p 0 -X stuff "c_shutdown(true)^M"'
CMD_SCREEN_LIST = 'screen -list'
UGC_DIR = GAME_DIR / 'ugc_mods' 
INSTALL_CONFIG_FILE_MOD_PATH = LEGACY_MODS_DIR / 'dedicated_server_mods_setup.lua'

def ugc_mods_path(cluster_name: str) -> Path:
    return UGC_DIR / cluster_name / 'Master' / 'content' / STEAM_GAME_ID
