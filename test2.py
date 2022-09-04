import json
from base58 import b58decode, b58encode
from modules import MagicEden, ExchangeArt
from modules.famous_fox import FamousFox
from modules.wallet_manager import SolWalletManager
from utils.solana import get_nft_metadata
from solana.publickey import PublicKey
import requests

""" a = MagicEden(
    rpc="https://snipe.acidnode.io/",
    privkey="3chJPsP3iLRAg2FiRrd5D1N4DfKKhkVw2DWpWP7rf9L7ccFNE5kp39aX86D7BQRZfXuxyXdgyAAdBqW5mkQVNx87",
)

# bFh29pSqpqq6GiABU2mjf78NF2JiTDERVanVPvHFtzm
c = get_nft_metadata("HdQnH1LbrBCyu3Wu6i367ejiCZqMoma1HYXsHicTLKM8", "https://snipe.acidnode.io/")

print(c) """

def get_uri_metadata(uri: str):
    
    try:
        
        return requests.get(uri).json()
    
    except:
                
        return None


def get_me_collection_metadata(symbol: str):

    last_listed = MagicEden.get_listed_nfts(
        symbol=symbol,
        limit=2
    )

    if last_listed:
        
        last_listed = last_listed[0]
        
        mint = last_listed["mintAddress"]
        
        nft_metadata = get_nft_metadata(mint_key=mint, rpc="https://snipe.acidnode.io/")
        
        if nft_metadata:
            
            uri = nft_metadata["data"]["uri"]

            print(uri)
            uri_metadata = get_uri_metadata(uri=uri)
            
            if uri_metadata:
                                
                attributes = [attribute["trait_type"] for attribute in uri_metadata["attributes"]] if uri_metadata.get("attributes") else []
                
                creators = nft_metadata["data"]["creators"]
            
                update_auth = nft_metadata["update_authority"]
            
                return {
                    "creators": creators,
                    "updateAuthority": update_auth,
                    "attributes": attributes
                }
        
    return None




get_me_collection_metadata("heavendao")