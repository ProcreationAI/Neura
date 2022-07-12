from datetime import datetime
from urllib.parse import quote
import base58
import configparser
import requests
import re
from solana.publickey import PublicKey
import struct
import json
import cloudscraper

try:
    import helheim
except:
    pass

from .constants import *


def injection(session, response):

    if helheim.isChallenge(session, response):

        return helheim.solve(session, response)
    
    else:
        
        return response

def create_cf_tls_session(captcha: bool = True, platform: str = "windows", browser: str = "chrome", tls: bool = True):
    
    if not captcha:
        
        session = cloudscraper.create_scraper()
        
    else:
        
        session = cloudscraper.create_scraper(
            browser={
                'browser': browser,
                'mobile': False,
                'platform': platform
            },
            requestPostHook=injection,
            captcha={
                'provider': "vanaheim" 
            }
        )

    if tls:
            
        session.bifrost_clientHello = 'chrome'

        helheim.bifrost(session, Paths.BIFROST_PATH)
    
    return session

def get_metadata_account(mint_key):

    metadata_program_id = PublicKey(
        'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s')

    return PublicKey.find_program_address(
        [b'metadata', bytes(metadata_program_id), bytes(PublicKey(mint_key))],
        metadata_program_id
    )[0]


def unpack_metadata_account(data):

    assert(data[0] == 4)
    i = 1
    source_account = base58.b58encode(
        bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
    i += 32
    mint_account = base58.b58encode(
        bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
    i += 32
    name_len = struct.unpack('<I', data[i:i+4])[0]
    i += 4
    name = struct.unpack('<' + "B"*name_len, data[i:i+name_len])
    i += name_len
    symbol_len = struct.unpack('<I', data[i:i+4])[0]
    i += 4
    symbol = struct.unpack('<' + "B"*symbol_len, data[i:i+symbol_len])
    i += symbol_len
    uri_len = struct.unpack('<I', data[i:i+4])[0]
    i += 4
    uri = struct.unpack('<' + "B"*uri_len, data[i:i+uri_len])
    i += uri_len
    fee = struct.unpack('<h', data[i:i+2])[0]
    i += 2
    has_creator = data[i]
    i += 1
    creators = []
    verified = []
    share = []
    if has_creator:
        creator_len = struct.unpack('<I', data[i:i+4])[0]
        i += 4
        for _ in range(creator_len):
            creator = base58.b58encode(
                bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
            creators.append(creator.decode("utf-8").strip("\x00"))
            i += 32
            verified.append(data[i])
            i += 1
            share.append(data[i])
            i += 1
    primary_sale_happened = bool(data[i])
    i += 1
    is_mutable = bool(data[i])
    
    metadata = {
        "update_authority": source_account.decode("utf-8").strip("\x00"),
        "mint": mint_account.decode("utf-8").strip("\x00"),
        "data": {
            "name": bytes(name).decode("utf-8").strip("\x00"),
            "symbol": bytes(symbol).decode("utf-8").strip("\x00"),
            "uri": bytes(uri).decode("utf-8").strip("\x00"),
            "seller_fee_basis_points": fee,
            "creators": creators,
            "verified": verified,
            "share": share,
        },
        "primary_sale_happened": primary_sale_happened,
        "is_mutable": is_mutable,
    }
    return metadata



def get_uri_metadata(uri: str):
    
    try:
        
        return requests.get(uri).json()
    
    except:
        
        return None


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

            return str(value) == "y"
            
        elif parameter == "auto_timer":
            
            return str(value) == "y"
        
        elif parameter == "await_mints":
            
            return int(value)
            
    except:
        
        pass

    return None


def create_tls_payload(url: str, method: str, headers: dict, params: dict | list = None, proxy: dict = None, cookies: dict = None) -> dict:

    if proxy:

        proxy_tls = {
            "scheme": "http",
            "host": proxy["host"],
            "useProxy": True,
            "username": proxy["user"],
            "password": proxy["pass"]
        }

    else:

        proxy_tls = {
            "scheme": "http",
            "host": "localhost:8888",
            "useProxy": False
        }
        
    headers_tls = {key: [value] for key, value in headers.items()}

    cookies_tls = []
    
    if cookies:
        
        for key, value in cookies.items():
            
            cookies_tls.append(f"{key}={value}")
            
        headers_tls["cookie"] = cookies_tls
        
    headers_tls["klient_header_order"] = list(headers.keys())
    headers_tls["klient_pseudo_header_order"] = [":method", ":authority", ":scheme", ":path"]

    return {

        "proxy": proxy_tls,
        "client": {
            "clientHello": 6,
            "forceAttemptHTTP2": True,
            "maxIdleConnsPerHost": 1024,
            "h2Settings": [
                {"ID": 1,  "Val": 65536},
                {"ID": 3,  "Val": 1000},
                {"ID": 4,  "Val": 6291456},
                {"ID": 6,  "Val": 262144}
            ],
            "h2Increment": {
                "StreamId": 0,
                "Increment": 15663105
            }
        },
        "request": {
            "header": headers_tls,
            "url": url,
            "method": method.upper(),
            "body": json.dumps(params) if params else ""
        }
    }


def get_lamports_from_listing_data(data: str, left_offset: int, right_offset: int) -> int:
    
    """
    me: 20, 32
    cc: 22, 16
    ff: 16, 0
    """
    
    right_offset = - right_offset if right_offset else right_offset
    
    data = data[left_offset:right_offset]

    return int.from_bytes(bytes.fromhex(data), "little")


def sol_to_lamports(sol: int | float) -> int:
    
    return int(sol*(10**9))

def lamports_to_sol(lamports: int) -> float:
    
    return lamports/(10**9)