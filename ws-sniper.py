
from datetime import datetime
import json
import time
import websocket
from base58 import b58decode
from dhooks import Embed, Webhook
import requests
from dhooks import Embed, Webhook
from solana.rpc.api import Client
import base64
import base58
import struct
from solana.rpc.api import Client
from solana.publickey import PublicKey
from modules import MagicEden

def get_lamports_from_listing_data(data: str, left_offset: int, right_offset: int) -> int:

    right_offset = - right_offset if right_offset else right_offset

    data = data[left_offset:right_offset]

    return int.from_bytes(bytes.fromhex(data), "little")


def on_message(_, message):


    tx = json.loads(message)["params"]["result"]["value"]

    logs = "".join(tx["logs"])
    
    if not tx["err"] and "Instruction: Sell" in logs:
        
        listing_data = me.check_tx_is_listing(tx["signature"])
        
        if listing_data:
            
            print(json.dumps(listing_data, indent=3))

    
def on_open(ws: websocket.WebSocket):

    ws.send(json.dumps(

        {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "logsSubscribe",
        "params": [
            {
            "mentions": [ "M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K" ]
            },
            {
            "commitment": "processed"
            }
        ],
        }
    ))

def on_error(_, error):
    
    print(error)

rpc = "wss://snipe.acidnode.io/"


me = MagicEden(
    rpc="https://sol.getblock.io/mainnet/?api_key=7752292c-0ffe-4356-a05b-6b7f3089f028",
    privkey="3chJPsP3iLRAg2FiRrd5D1N4DfKKhkVw2DWpWP7rf9L7ccFNE5kp39aX86D7BQRZfXuxyXdgyAAdBqW5mkQVNx87"
)
ws = websocket.WebSocketApp(url=rpc, on_open=on_open, on_message=on_message, on_error=on_error)

ws.run_forever()


