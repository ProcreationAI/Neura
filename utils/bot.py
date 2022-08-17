from datetime import datetime
import configparser
import re
import os
import subprocess
import sys

from .constants import Bot


def logger(text: str):

    now = datetime.now()

    log_time = "{:02d}:{:02d}:{:02d}".format(now.hour, now.minute, now.second)

    return f"[{log_time}] {text}"


def get_config(parameter: str):

    try:

        cfg_file = configparser.ConfigParser()
        cfg_file.read("config.ini")

        value = dict(cfg_file["CONFIG"])[parameter.lower()]

        if parameter == "holder":

            return str(value)

        elif parameter == "time":
            
            value = int(value)
            
            datetime.fromtimestamp(value)

            return value if value > int(datetime.now().timestamp()) else int(datetime.now().timestamp())

        elif parameter in ["mint_rpc", "snipe_rpc"]:

            return value

        elif parameter == "advanced":

            return str(value).lower() == "y"
        
        elif parameter == "await_mints":
            
            return int(value)
        
        elif parameter == "webhook":
            
            return str(value)

        elif parameter == "discord":
            
            return str(value)
        
    except:
        
        pass

    return None


def get_hwid():
    
    try:
        
        return str(subprocess.check_output("wmic csproduct get uuid"), "utf-8").strip("UUID").strip()

    except:
        
        return None
    

def set_app_title(text: str):

    if Bot.USER_OS == "win32":

        os.system("title " + f"{text}")

    elif Bot.USER_OS == "darwin":

        sys.stdout.write(f"\x1b]2;{text}\x07")