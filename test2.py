import json
import requests
from solana.keypair import Keypair
import requests
from urllib.parse import quote, urlencode
import re

from modules import BifrostLaunchpad, BifrostAuth

def check_dc_token(token: str):
    
    try:
                
        headers = {
            'authorization': token
        }

        return requests.get("https://discord.com/api/v7/users/@me", headers=headers).json()
        
    except:
        
        return None

def bifrost_dc_login(mint_site: str, dc_auth_token: str) -> None | requests.Session:
    
    user_dc_data = check_dc_token(token=dc_auth_token)
    
    if not user_dc_data:
        
        print("invalid Discord user auth token")
        
        return None
    
    user_name = user_dc_data["username"] + "#" + user_dc_data["discriminator"]
    
    bf_auth = BifrostAuth(
        mint_site=mint_site
    )
    
    print(f"Accessing {mint_site} for Discord login...")
    
    if bf_auth.get_mint_site():
        
        print("Access successful")
        
    else:
        
        print(f"Unable to access {mint_site}")
        
        return None
    
    print("Generating Discord auth session...")
    
    if bf_auth.generate_auth_session():
        
        print("Auth session generated successfuly")
        
    else:
        
        print("Unable to generate auth session")
        
        return None

    print(json.dumps(bf_auth.session.headers, indent=3))
    print("Generating Discord signin...")
    
    signin_url = bf_auth.generate_dc_signin()
    
    if signin_url:
        
        print("Signin generated successfuly")
        
    else:
        
        print("Unable to generate signin")
        
        return None

    print(f"Logging in as {user_name}")
    
    auth_url = bf_auth.authorize_discord(signin_url=signin_url, dc_auth_token=dc_auth_token)
    
    if auth_url:
        
        print("Logged in successfuly")
        
    else:
        
        print("Unable to login")
        
        return None
    
    print(f"Waiting for auth callback...")
    
    if bf_auth.discord_auth_callback(auth_url=auth_url):
        
        print("Auth callback received successfuly")
        
    else:
        
        print("Auth callback failed")
        
        return None

    return bf_auth.session

url = "https://bifrost.blocksmithlabs.io/mint/froots"

dc_auth_token = "NDE5MDk3NjE3NDY1ODY4Mjg5.GlxA8N.j2y-0gFtvpbYXPsY5Yq7iFMy4pOA98PxgozYII"


bifrost_dc_login(mint_site=url, dc_auth_token=dc_auth_token)

exit()

txs = ["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"]

a = BifrostLaunchpad(
    privkey="59c95GpudN8Ks6UJDDHAmJ59yhTVFz74Fh2SbtfbtxfVEtEn2H1KxbQZEMydRwbqBmBdEdrB22ZW9YxZNXqiWZFX",
    bf_auth_session=bl.session
)


res = a.send_transactions(txs=txs)

print(res)
