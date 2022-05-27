# Don't Stave Together dedicated server manager

Welcome to the Don't Starve Together dedicated server manager.
This script will allow you to manage your server easily from your pc.

Currently, the script run on windows and linux but the server must be a linux.

## Quick Start

### Dependency

#### Client

You need to have python3 and pip intalled on your pc.
The script will automacically install missing python module.

#### server

On the server you need to have installed steamcmd, screen and the binary of Don't Starve Together dedicated server at ~/Steam/steamapps/common/Dont't Starve Together Dedicated Server/bin64.

### Run

To start, you need to pass ip address and the user to connect the server : 
```
python3 cmd.py -u <user> -p <password> -i <ip_address>
```

## Inspiration

Mods management was greatly inspired by [dly2424 DST_Dedicated_Mod_Manager](https://github.com/dly2424/DST_Dedicated_Mod_Manager).
If you look for a mods manager only, see [this](https://github.com/dly2424/DST_Dedicated_Mod_Manager) repository.
