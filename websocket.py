
import json
import websocket
from modules import MagicEden

def on_message(ws, message):

    block_txs = json.loads(message)["params"]["result"]["value"]["block"]["transactions"]

    for tx in block_txs:

        listing_data = MagicEden.check_tx_is_listing_2(tx)
        
        if listing_data:
            
            print(listing_data)


def on_error(ws, message):

    print(message)

def on_open(ws: websocket.WebSocket):

    ws.send(json.dumps(
        payload
    ))


rpc = "wss://thrumming-damp-shadow.solana-mainnet.quiknode.pro/362bbea5917e5ec837d4e76ffe9aafcc1d22a44c/"

payload = {
  "jsonrpc": "2.0",
  "id": "1",
  "method": "blockSubscribe",
  "params": [
    {
      "mentionsAccountOrProgram": "M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K"
    },
    {
      "commitment": "confirmed",
      "encoding": "jsonParsed",
      "transactionDetails": "full"
    }
  ]
}

ws = websocket.WebSocketApp(url=rpc, on_open=on_open, on_message=on_message, on_error=on_error)

ws.run_forever()
