from base64 import b64decode, b64encode
import json
from anchorpy import Wallet
from base58 import b58decode
import requests
from urllib.parse import urlsplit, quote
from datetime import datetime
import re
from solana.keypair import Keypair
from solana.transaction import Transaction

from utils.bypass import create_tls_payload
from utils.solana import sol_to_lamports


SLIPPAGE = 5
BIFROST_SIGNER = "BFMGKvziBENLDdpFs3y75d9myFYF9ZqhTyxqet9ohB4N"

class BifrostAuth():
    
    def __init__(self, mint_site: str) -> None:
        
        self.session = requests.Session()
        
        self.mint_site = mint_site
        
        
    def get_mint_site(self) -> bool:
        
        url = self.mint_site
        
        headers = {
            'Host': 'bifrost.blocksmithlabs.io',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'es-ES,es;q=0.9',
        }

        self.session.headers = headers
        
        try:
                
            res = self.session.get(url)
            
            return res.status_code == 200
        
        except:
            
            return False
    
    
    def generate_auth_session(self) -> bool:
        
        url = "https://bifrost.blocksmithlabs.io/api/auth/session"
        
        headers = {
            'Host': 'bifrost.blocksmithlabs.io',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.mint_site,
            'accept-language': 'es-ES,es;q=0.9',
        }
        
        self.session.headers = headers
        
        try:
                
            res = self.session.get(url)
            
            return res.status_code == 200
        
        except:
            
            return False
    
    
    def generate_dc_signin(self) -> str | None:
        
        url = "https://bifrost.blocksmithlabs.io/api/auth/signin/discord?"

        headers = {
            'Host': 'bifrost.blocksmithlabs.io',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://bifrost.blocksmithlabs.io',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.mint_site,
            'accept-language': 'es-ES,es;q=0.9',
        }

        self.session.headers = headers
        
        csrf_cookie = self.session.cookies.get("__Host-next-auth.csrf-token")
        
        if not csrf_cookie:
            
            return None

        csrf_token = csrf_cookie.split("%")[0]
        
        data = f'csrfToken={csrf_token}&callbackUrl={quote(self.mint_site)}&json=true'
        
        try:
                
            res = self.session.post(url, data=data)

            return res.json().get("url")
            
        except:
            
            return None
    
    def authorize_discord(self, signin_url: str, dc_auth_token: str) -> str | None:
        
        state = signin_url.split("state=")[1]
        client_id = re.findall("client_id=(.*?)&", str(signin_url))[0]

        url = "https://discord.com/api/v9/oauth2/authorize"
            
        headers = {
            'Host': 'discord.com',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'authorization': dc_auth_token,
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-discord-locale': 'es-ES',
            'sec-ch-ua-platform': '"macOS"',
            'accept': '*/*',
            'origin': 'https://discord.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': signin_url,
            'accept-language': 'es-ES,es;q=0.9',
        }
        
        self.session.headers = headers

        params = {
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': 'https://bifrost.blocksmithlabs.io/api/auth/callback/discord',
            'scope': 'identify guilds',
            'state': state,
        }

        payload = {
            'permissions': '0',
            'authorize': True,
        }
        
        try:
                
            res = self.session.post(url, params=params, json=payload)

            return res.json().get("location")
        
        except:
            
            return None
        
        
    def discord_auth_callback(self, auth_url: str) -> bool:
        
        url = "https://bifrost.blocksmithlabs.io/api/auth/callback/discord"
        
        state = auth_url.split("state=")[1]
        code = re.findall("code=(.*?)&", str(auth_url))[0]

        headers = {
            'Host': 'bifrost.blocksmithlabs.io',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://discord.com/',
            'accept-language': 'es-ES,es;q=0.9',
        }

        self.session.headers = headers
        
        params = {
            'code': code,
            'state': state,
        }

        try:
                
            res = self.session.get(url, params=params)

            return res.status_code == 200
        
        except:
            
            return False


class BifrostLaunchpad():
    
    
    def __init__(self, bf_auth: BifrostAuth, privkey: str = None) -> None:
        
        self.payer = Keypair.from_secret_key(b58decode(privkey)) if privkey else Keypair().generate()
        
        self.mint_account = Keypair().generate()

        self.session = bf_auth.session
        
        self.mint_site = bf_auth.mint_site


    @staticmethod
    def get_max_price(bonding_price: float) -> float:
        
        return bonding_price * (1 + (SLIPPAGE/100))
    
    @staticmethod
    def get_collection_info(url: str) -> dict | None:

        split_url = urlsplit(url)

        symbol = split_url.path.split("/")[-1]
        
        url = f"https://bifrost.blocksmithlabs.io/api/project/info/{symbol}"
        
        headers = {
            'authority': 'bifrost.blocksmithlabs.io',
            'accept': '*/*',
            'accept-language': 'es-ES,es;q=0.9',
            'referer': url,
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }

        payload = create_tls_payload(
            url=url,
            method="GET",
            headers=headers
        )
        
        try:
            
            collection = requests.post("http://127.0.0.1:3000", json=payload).json()

            collection = json.loads(collection["body"])["data"]
            
            stage = collection["mintPhases"][-1]

            start_time = int(datetime.fromisoformat(stage["startDate"][:-1]).timestamp())

            price = stage["price"]
            
            return {
                
                "name": collection["name"],
                "price": sol_to_lamports(price),
                "supply": collection["supply"],
                "cmid": collection["candyMachineId"],
                "date": start_time,
            }
            
        except:
                        
            return None
    
    def get_cm_state(self, cmid: str) -> dict | None:
        
        url = f'https://bifrost.blocksmithlabs.io/api/solana/cm-state?id={cmid}'
        
        headers = {
            'Host': 'bifrost.blocksmithlabs.io',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.mint_site,
            'accept-language': 'es-ES,es;q=0.9',
        }

        self.session.headers = headers
        
        try:
                
            res = self.session.get(url).json()

            return res["state"] if res["success"] else None
        
        except:
            
            return None
        
    def get_bonding_info(self, token_mint: str) -> dict | None:

        url = "https://bifrost.blocksmithlabs.io/api/solana/bonding-info"
        
        headers = {
            'Host': 'bifrost.blocksmithlabs.io',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.mint_site,
            'accept-language': 'es-ES,es;q=0.9',
        }

        params = {
            'mint': token_mint,
            'index': '0',
        }

        self.session.headers = headers
        
        try:
            
            res = self.session.get(url, params=params).json()

            return res["tokenBonding"] if res["success"] else None
        
        except:
                        
            return None
    
    def get_bonding_price(self, token_bonding: str) -> float | None:
        
        url = "https://bifrost.blocksmithlabs.io/api/solana/bonding-price"

        headers = {
            'Host': 'bifrost.blocksmithlabs.io',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.mint_site,
            'accept-language': 'es-ES,es;q=0.9',
        }
        
        self.session.headers = headers

        params = {
            'tokenBondingKey': token_bonding,
        }

        try:
                
            res = self.session.get(url, params=params)
            
            return res.json().get("price")
        
        except:
            
            return None

    def get_transactions(self, cmid: str, token_bonding: str, max_price: float) -> list | None:
        
        url = "https://bifrost.blocksmithlabs.io/api/solana/mint-info"

        headers = {
            'Host': 'bifrost.blocksmithlabs.io',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'es-ES,es;q=0.9',
            "referer": self.mint_site
        }

        self.session.headers = headers
                
        params = {
            'id': cmid,
            'payer': str(self.payer.public_key),
            'mint': str(self.mint_account.public_key),
            'tokenBonding': token_bonding,
            'maxPrice': str(max_price),
        }

        try:
                
            res = self.session.get(url, params=params)

            return res.json().get("txs")
        
        except:
            
            return None
    
    
    def sign_transactions(self, txs: list) -> list:
        
        signed_txs = []
        
        for tx in txs:
            
            recovered_tx = Transaction.deserialize(b64decode(tx))
            
            recovered_tx.sign_partial(self.mint_account)

            signed_txs.append(recovered_tx)
            
        wallet = Wallet(self.payer)
        
        signed_txs = wallet.sign_all_transactions(signed_txs)

        return [b64encode(tx.serialize(verify_signatures=False)) for tx in signed_txs]
    
    
    def send_transactions(self, txs: list):
        
        url = "https://bifrost.blocksmithlabs.io/api/solana/send-transaction"
        
        headers = {
            'Host': 'bifrost.blocksmithlabs.io',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'content-type': 'text/plain;charset=UTF-8',
            'accept': '*/*',
            'origin': 'https://bifrost.blocksmithlabs.io',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'es-ES,es;q=0.9',
            "referer": self.mint_site
        }
    
        self.session.headers = headers
        
        data = json.dumps(txs)

        try:
                
            res = self.session.post(url, data=data, timeout=30)

            return res.json().get("success")
        
        except:
            
            return None
