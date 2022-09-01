import json
import cloudscraper
import subprocess
import time
import requests

try:
    import helheim
except:
    pass

from .constants import Paths, Keys

def injection(session, response):

    if helheim.isChallenge(session, response):

        return helheim.solve(session, response)
    
    else:
        
        return response

def create_helheim_session(captcha: bool = True, platform: str = "windows", browser: str = "chrome", tls: bool = True):
    
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


def start_tls():

    subprocess.Popen(
        [Paths.TLS_PATH],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(0.5)
    
    headers = {
        "Authorization": Keys.TLS_KEY
    }

    requests.post('http://127.0.0.1:3000/authenticate', headers=headers, timeout=4)
    
