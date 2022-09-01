

from solana.rpc.api import Client
from solana.rpc.commitment import Commitment
from me_module import MagicEden

def get_account_last_txs(account: str, limit: int, commitment: str, until: str = None):

    try:
        
        client = Client(sol_rpc)
        
        tx = client.get_signatures_for_address(account=account, limit=limit, commitment=Commitment(commitment), until=until)["result"]

        return tx

    except:
                
        return None
    

sol_rpc = "https://api.mainnet-beta.solana.com"
privkey = ""

recent_txs = []
until_tx = None


magic_eden = MagicEden(
    rpc=sol_rpc,
    privkey=privkey
)

while True:
    
    last_txs = get_account_last_txs(
        account="M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K", 
        limit=10, 
        commitment="confirmed",
        until=until_tx
    )
    
    if last_txs:
            
        for tx in last_txs:
            
            if tx["signature"] not in recent_txs:
                
                #check if the signature it's a ME listing and get the needed accs
                
                #buy_nft func needs some params
                tx = magic_eden.buy_nft(
                    seller="", #NFT current owner
                    price=0, #in lamports
                    mint="", #mint address
                    creators=[] #NFT creators
                )
                
                print(tx)
                
                #successful purchase
                
        until_tx = last_txs[0]["signature"]
