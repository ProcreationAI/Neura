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

        res = requests.get("https://discord.com/api/v7/users/@me", headers=headers)

        return res.json() if res.status_code == 200 else None
        
    except:
        
        return None

def bifrost_dc_login(mint_site: str, dc_auth_token: str) -> None | BifrostAuth:
    
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

    print(bf_auth.session.cookies.get_dict())
    return bf_auth

url = "https://bifrost.blocksmithlabs.io/mint/sentries"

dc_auth_token = "NDE5MDk3NjE3NDY1ODY4Mjg5.Gq3Cij.IIHGqtdE_fGaN4Bh-s4b7K1djoRi0p0tb9vuR4"


bf_auth = bifrost_dc_login(mint_site=url, dc_auth_token=dc_auth_token)

#Gxjbv483FHhAEy63m32QMS9r7zCmTLMiBLK85TknRgFP

bf = BifrostLaunchpad(
    bf_auth=bf_auth,
    privkey="59c95GpudN8Ks6UJDDHAmJ59yhTVFz74Fh2SbtfbtxfVEtEn2H1KxbQZEMydRwbqBmBdEdrB22ZW9YxZNXqiWZFX"
)


a = bf.get_cm_state("Gxjbv483FHhAEy63m32QMS9r7zCmTLMiBLK85TknRgFP")

print(a)
