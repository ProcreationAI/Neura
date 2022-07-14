import base58
import base64
import requests
from solana.publickey import PublicKey
import struct
from solana.rpc.api import Client

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


def get_nft_metadata(mint_key: str, rpc: str):

    try:
        
        client = Client(rpc)
        
        metadata_account = _get_metadata_account(mint_key)

        data = base64.b64decode(client.get_account_info(
            metadata_account)['result']['value']['data'][0])

        metadata = _unpack_metadata_account(data)

        return metadata

    except:  
        
        return None
    
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