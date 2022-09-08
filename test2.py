import json
import time
from base58 import b58decode, b58encode
from modules import MagicEden, ExchangeArt
from modules.coral_cube import CoralCube
from modules.famous_fox import FamousFox
from modules.wallet_manager import SolWalletManager
from utils.solana import get_nft_metadata, lamports_to_sol
from solana.publickey import PublicKey
import requests

a = CoralCube(
    rpc="https://snipe.acidnode.io/",
    privkey="3chJPsP3iLRAg2FiRrd5D1N4DfKKhkVw2DWpWP7rf9L7ccFNE5kp39aX86D7BQRZfXuxyXdgyAAdBqW5mkQVNx87",
)

while True:
    
    try:
        
            
        b = a.get_listed_nfts("gm_duckz", limit=2)

        print(lamports_to_sol(b[0]["price"]))

        
    except Exception as e:
        
        print(e)
        
        print("err")
        
    time.sleep(1)