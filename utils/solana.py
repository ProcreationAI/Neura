import base58
from solana.blockhash import Blockhash
from solana.rpc.commitment import Commitment
import base64
import requests
from solana.publickey import PublicKey
import struct
from solana.rpc.api import Client
from anchorpy import Program, Wallet, Provider
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from solana.rpc import types
from urllib.parse import urlparse
from anchorpy.idl import Idl

from lib.idl import AccountClient


def get_websocket_url(rpc: str):
    
    parsed = urlparse(rpc)
    
    return "wss://" + parsed.netloc

def get_wallet_nfts(wallet: str, rpc: str):

    client = Client(rpc)
    
    try:
        
        res = client.get_token_accounts_by_owner(owner=wallet, opts=types.TokenAccountOpts(encoding="jsonParsed", program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")))

        nfts = res["result"]["value"]

        holded_nfts = []

        for nft in nfts:

            nft_data = nft["account"]["data"]["parsed"]["info"]

            if int(nft_data["tokenAmount"]["amount"]) == 1:

                holded_nfts.append(nft_data["mint"])

        return holded_nfts

    except:
        
        return None
    
def get_last_account_txs(rpc: str, account: str, limit: int, commitment: str, until: str = None):

    try:
        
        client = Client(rpc)
        
        txs = client.get_signatures_for_address(account=account, limit=limit, commitment=Commitment(commitment), until=until)["result"]

        return txs

    except:
                        
        return None
    
def get_blockhash(rpc: str) -> Blockhash:

    try:
            
        client = Client(rpc)
        
        res = client.get_recent_blockhash(Commitment('finalized'))

        return Blockhash(res['result']['value']['blockhash'])

    except:
        
        return None
    

def get_wallet_balance(pubkey: str, rpc: str):

    try:

        client = Client(rpc)

        balance = client.get_balance(pubkey)

        return balance["result"]["value"]

    except:

        return 0
    
def get_pub_from_priv(privkey: str):

    try:
        wallet = Keypair.from_secret_key(base58.b58decode(privkey))

        return str(wallet.public_key)

    except:

        return None
    
def _get_metadata_account(mint_key):

    metadata_program_id = PublicKey('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s')

    return PublicKey.find_program_address(
        seeds=[
            b'metadata', 
            bytes(metadata_program_id), 
            bytes(PublicKey(mint_key))
        ],
        program_id=metadata_program_id
    )[0]


def _unpack_metadata_account(data):

    assert(data[0] == 4)
    i = 1
    source_account = base58.b58encode(bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
    i += 32
    mint_account = base58.b58encode(bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
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
            creator = base58.b58encode(bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
            creators.append(creator.decode("utf-8").strip("\x00"))
            i += 32
            verified.append(data[i])
            i += 1
            share.append(data[i])
            i += 1
    primary_sale_happened = bool(data[i])
    i += 1
    is_mutable = bool(data[i])
    
    i += 7

    collection_address = base58.b58encode(data[i:][:32])
    
    collection_address = collection_address.decode("utf-8").strip("\x00") if not collection_address.isdigit() else None
    
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
        "collection": collection_address
    }
    
    return metadata

def get_uri_metadata(uri: str):
    
    try:
        
        return requests.get(uri).json()
    
    except:
                
        return None


def get_nft_metadata(mint_key: str, rpc: str):

    try:
        
        client = Client(rpc)
        
        metadata_account = _get_metadata_account(mint_key)

        data = base64.b64decode(client.get_account_info(metadata_account)['result']['value']['data'][0])

        metadata = _unpack_metadata_account(data)

        return metadata

    except:
                        
        return None


async def get_program_account_idl(name: str, account: str, prog: str, rpc: str, prog_idl: dict = None):

    try:
            
        program = None
        client = None
        
        program_id = PublicKey(prog)
            
        client = AsyncClient(rpc)

        provider = Provider(client, Wallet(Keypair.generate()))
        
        if prog_idl:
            
            idl = Idl.from_json(prog_idl)
            
        else:
                
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

    except:
        
        if program:
            program.close()

        if client:
            client.close()
            
        return None
def get_lamports_from_listing_data(data: str, left_offset: int = None, right_offset: int = None) -> int:
    
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