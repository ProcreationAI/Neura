import asyncio
import json
from threading import Thread

from base58 import b58decode, b58encode
from urllib.parse import quote

from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from solana.message import Message
from solana.rpc.api import Client
from solana.rpc import types
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.transaction import AccountMeta, TransactionInstruction, Transaction
from spl.token.instructions import create_associated_token_account, transfer_checked, TransferCheckedParams
from solana.system_program import TransferParams, transfer
from solana.blockhash import Blockhash
from solana.rpc.commitment import Commitment
from anchorpy import Program, Wallet, Provider
from web3 import Web3
from solana.rpc.async_api import AsyncClient
import base64
from spl.token.instructions import InitializeMintParams, MintToParams, create_associated_token_account, get_associated_token_address, initialize_mint, mint_to, initialize_account, InitializeAccountParams
from dhooks import Webhook, Embed
import requests
import time
import aiohttp
from modules import MagicEden, OpenSea, CoralCube, SolWalletManager
from lib import AccountClient
from utils import *
import subprocess

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
    

async def get_account_metadata(name: str, account: str, prog: str):

    try:

        program = None
        
        program_id = PublicKey(prog)
            
        client = AsyncClient(sol_rpc)

        provider = Provider(client, Wallet(Keypair.generate()))
        
        idl = await Program.fetch_idl(
            program_id,
            provider
        )

        program = Program(
            idl,
            program_id,
            provider
        )

        candyMachine = await AccountClient.fetch_custom(program.account[name], PublicKey(account))

        await program.close()
        await client.close()

        return candyMachine

    except Exception as e:
        
        print(e)
        
        await client.close()

        if program:

            await program.close()

        return None


def validate_me_purchase_results(nft_data: dict, filters: dict, min_rank: int = None, max_rank: int = None):

    if filters:
        
        attributes = nft_data["attributes"]
        
        if attributes:
            
            possible_attributes = []

            for attribute in attributes:
                
                possible_attributes.append(
                    {
                        "trait_type": attribute["trait_type"].lower().strip(),
                        "value": attribute["value"].lower().strip()
                    }
                )            
            
            print(json.dumps(possible_attributes, indent=3))
            if not all(attr in possible_attributes for attr in filters):
                    
                return False
        else:
            
            return False

    if min_rank is not None and max_rank is not None:
    
        if nft_data["rarity"]:
            
            ranks = [rank["rank"] for rank in nft_data["rarity"].values()]
            
            for rank in ranks:
                    
                if not min_rank <= rank <= max_rank:
                    
                    return False
            
        else:
            
            return False
                

    return True
  

def get_nft_metadata(mint_key):

    client = Client(sol_rpc)

    try:
        metadata_account = get_metadata_account(mint_key)

        data = base64.b64decode(client.get_account_info(
            metadata_account)['result']['value']['data'][0])

        metadata = unpack_metadata_account(data)

        return metadata

    except:  
        
        return None


def get_me_collection_metadata(symbol: str):

    last_listed = MagicEden.get_listed_nfts(
        symbol=symbol,
    )

    if last_listed:
        
        last_listed = last_listed[0]
        
        mint = last_listed["mintAddress"]
        
        nft_metadata = get_nft_metadata(mint_key=mint)
        
        if nft_metadata:
            
            uri = nft_metadata["data"]["uri"]
            print()
            try:
                
                uri_metadata = requests.get(uri).json()
                
            except:
                
                uri_metadata = None
                
            if uri_metadata:
                                
                attributes = [attribute["trait_type"] for attribute in uri_metadata["attributes"]] if uri_metadata.get("attributes") else []
                
                creators = nft_metadata["creators"]
            
                update_auth = nft_metadata["update_authority"]
            
                return {
                    "creators": creators,
                    "updateAuthority": update_auth,
                    "attributes": attributes
                }
        
    return None
 
 
start_tls() 
sol_rpc = "https://thrumming-damp-shadow.solana-mainnet.quiknode.pro/362bbea5917e5ec837d4e76ffe9aafcc1d22a44c/"

client = Client(sol_rpc)


me = SolWalletManager(
    rpc=sol_rpc,
    privkey="Xg6Ufrx89Bgpa1GyFjQWALZK36xPTymzyb9sWe3NgCt3Jw3DsAtq8QDCXP3VRW95HH9MUXkAF2Dg8vCi6ncMSgo"
)
a = client.get_account_info("2gMo2Qtqa83GyhA9uQmoB9wbyjFhNYrd1L4izGCsbEo3")

data = "BAAAADAuMDYVAAAASHlwZSBQcmltYXRlcyBFbWJhc3N5BAAAAEhZUEVzBAAAAAAAAEkAAABodHRwczovL21vbmtlbGFicy5ueWMzLmRpZ2l0YWxvY2VhbnNwYWNlcy5jb20vaHlwZS1wcmltYXRlcy1lbWJhc3N5L2pzb24vsxVncTNP5lHi8OhzVQbmtxEG0DZjAbjyR0Fgz0XW0zmAPqy3viVxdjzlyJLgRRT+4sdeFjzBFu3YgeSUx/NF7scsAQBzBAAAAAAAAN6ZUX59w3onLMVVrh+xFCnpVzPD/eMYVbjNxQ6fepZArCYAABFwDeYqJxiSLjhJBOQ6U7uSS9UJt1nOvV6ul5DofWGjXx2usr/wn1pusyr85kEvYKYLVUcBi3FhByGbznXtO1JkAAEAAAAAAAAAAQt4zsDxKuQERqhTI9f9WwjmowS2g9XMzd6olKUcu/gMAgAAAJC/xWIAlDV3AAAAAAQAAABNYWluBAEAAAAAAAABOYzILfoAsmmYebjeKHZ4N0PGzzogHh13WP4lgytDp7yvG8tiAJQ1dwAAAAAWAAAASFlQRTogUHJpbWF0ZXMgRW1iYXNzeQoBAAAAAAAAABUAAABIeXBlIFByaW1hdGVzIEVtYmFzc3kAAAAAAAAAAAAARW1iYXNzeQAAAAAAAAAAAYCWmAAAAAAAARQAAAABAJQ1dwAAAAABBQAAAERVVENIABUAAABIeXBlIFByaW1hdGVzIEVtYmFzc3kAAAAAAAAAAAGAlpgAAAAAAAEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

import borsh

from borsh import types


schema = {
    "z": types.string,
    "a": types.string,
    "b": types.u32,
    "c": types.u32,
    "d": types.u64,
    "e": types.string,
    "f": types.u16,
    "g": types.fixed_array(types.u8, 32),
    "h": types.fixed_array(types.u8, 32),
    "i": types.u16,
    "j": types.u64,
    "k": types.fixed_array(types.u8, 32),
    "l": types.u32,
    "m": types.fixed_array(types.u8, 32),
    "n": types.fixed_array(types.u8, 32),


}
print(list(bytes(b58decode("2B52sUmgGeTLc1Cw3yijHtL5Zxhe8uWQJCSNFcFPh1xE"))))
des = borsh.deserialize(schema=schema, data=base64.b64decode(data))
print(des)
a = des["o"]

print(b58encode(bytes(a)))