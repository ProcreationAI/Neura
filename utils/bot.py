from datetime import datetime
import configparser
import re

from .constants import *

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

            if re.match("^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$", value):

                datetime.strptime(value, "%H:%M:%S")

                return value

        elif parameter in ["sol_rpc", "eth_rpc"]:

            return value

        elif parameter == "advanced":

            return str(value).lower() == "y"
            
        elif parameter == "auto_timer":
            
            return str(value).lower() == "y"
        
        elif parameter == "await_mints":
            
            return int(value)
        
        elif parameter == "webhook":
            
            return str(value)
            
    except:
        
        pass

    return None
