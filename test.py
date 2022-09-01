import asyncio
from datetime import datetime
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
from solana.rpc.async_api import AsyncClient
import base64
from spl.token.instructions import InitializeMintParams, MintToParams, create_associated_token_account, get_associated_token_address, initialize_mint, mint_to, initialize_account, InitializeAccountParams
from dhooks import Webhook, Embed
import requests
import time
import aiohttp

from lib.idl import AccountClient
import subprocess

from modules import MagicEden, CoralCube
from utils.constants import *
from utils.solana import get_nft_metadata

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
 

def get_account_last_txs(account: str, limit: int, commitment: str, until: str = None):

    try:
        
        client = Client(sol_rpc)
        
        tx = client.get_signatures_for_address(account=account, limit=limit, commitment=Commitment(commitment), until=until)["result"]

        return tx

    except:
                
        return None
    

def get_me_highest_attribute_floor(collection_attributes: list, nft_attributes: list) -> int | None:
            
    highest_floor = 0

    for nattr in nft_attributes:
        
        for cattr in collection_attributes:
            
            if nattr == cattr["attribute"]:
                
                if cattr["floor"] > highest_floor:
                    
                    highest_floor = cattr["floor"]

    if highest_floor:
            
        return highest_floor

    return None

def send_sniper_webhook(mint: str, tx: str, price: float, sniping_time: float, webhook: str):
    
    nft_data = MagicEden.get_nft_data(mint=mint)
    
    if nft_data:
        
        name = nft_data["title"]
        img = nft_data["img"]
        url = f"https://magiceden.io/item-details/{mint}"
        tx_url = f"https://explorer.solana.com/tx/{tx}"
        
        embed = Embed(
            timestamp="now"
        )
        
        embed.color = Discord.EMBED_COLOR
        embed.description = "`SUCCESSFUL SNIPE`"
        
        embed.set_title(name, url)
        embed.set_thumbnail(img)
        embed.set_footer(Discord.EMBED_FOOTER_TXT, Discord.EMBED_FOOTER_IMG)
        
        embed.add_field("**Price**", f"{price} SOL", inline=False)
        embed.add_field("**Speed**", f"{sniping_time} s", inline=False)
        embed.add_field("**Transaction**", f"[Explorer]({tx_url})", inline=False)
        
        try:
            
            return Webhook(webhook).send(embed=embed)
        
        except:
            
            pass
            
    return None


sol_rpc = "https://api.mainnet-beta.solana.com"
sol_rpc = "https://snipe.acidnode.io/"
#sol_rpc = "https://late-spring-market.solana-mainnet.discover.quiknode.pro/78837b96c6e80f0da8101c6b3342544ad52ad2f9/"

client = Client(sol_rpc)

a = client.get_account_info("Aqw1uJT4o24WKrjKvETvA7ftSjrgMXQFnEywfHKn8f5N")

data = a["result"]["value"]["data"][0]

data = base64.b64decode(data)

minted = int.from_bytes(data[1:9], "little")
available = int.from_bytes(data[10:18], "little")

print(minted, available)
exit()

i = 15
until_tx = None
recent_txs = []

while i:
    
    last_txs = get_account_last_txs(
        account="M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K", 
        limit=10, 
        commitment="confirmed",
        until=until_tx
    )
    
    if last_txs:
            
        for a in last_txs:
            
            if a["signature"] not in recent_txs:
                
                recent_txs.append(a["signature"])
                our_time = int(time.time())
                me_time = a["blockTime"]
                tx = a["signature"]
                
                our_time = datetime.fromtimestamp(our_time).strftime("%H:%M:%S")
                print(f"our time: {our_time} | ME time: {me_time} | tx: {tx}")
                
        until_tx = last_txs[0]["signature"]
        i -= 1

        print("="*50)