from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Commitment
from solana.blockhash import Blockhash
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction, Transaction
from base58 import b58decode, b58encode

from utils.solana import get_lamports_from_listing_data

TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'
SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
SYSTEM_SLOT_HASHES = "SysvarS1otHashes111111111111111111111111111"
COMPUTE_BUDGET = "ComputeBudget111111111111111111111111111111"
ASSOCIATED_TOKEN_ID = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"

FFF_PROGRAM = "8BYmYs3zsBhftNELJdiKsCN2WyCBbrTwXd6WG4AFPr6n"
FOXY_ID = "FoXyMu5xwXre7zEoSvzViRk3nGawHUp9kUh97y2NDhcq"
FFF_TRESAURY = "2x3yujqB7LCMdCxV7fiZxPZStNy7RTYqWLSvnqtqjHR6"

OPTS = TxOpts(skip_preflight=True, skip_confirmation=False, preflight_commitment=Commitment("confirmed"))

class FamousFox():
    
    
    def __init__(self, rpc: str, privkey: str):
        
        self.client = Client(rpc)
        
        self.payer = Keypair.from_secret_key(b58decode(privkey))

    def _get_blockhash(self):

        res = self.client.get_recent_blockhash(Commitment('finalized'))
    
        return Blockhash(res['result']['value']['blockhash'])

    
    def check_tx_is_listing(self, tx: str) -> dict | None:

        try:
                        
            tx = self.client.get_transaction(tx_sig=tx, commitment=Commitment("confirmed"))["result"]
                        
            logs = "".join(tx["meta"]["logMessages"])
            accounts = tx["transaction"]["message"]["accountKeys"]

            if not tx["meta"]["err"] and FFF_PROGRAM in accounts:
                
                instr_data = tx["transaction"]["message"]["instructions"][-1]["data"]
                instr_data = b58decode(instr_data).hex()
                
                if "Instruction: ListItem" in logs:
                                        
                    mint = tx["meta"]["postTokenBalances"][0]["mint"]
                    lamports = get_lamports_from_listing_data(data=instr_data, left_offset=32, right_offset=0)
                    seller = accounts[0]

                elif "Instruction: UpdateItem" in logs:
                    
                    mint = accounts[-1]
                    lamports = get_lamports_from_listing_data(data=instr_data, left_offset=16, right_offset=0)
                    seller = accounts[2]
                                
                return {
                    "price": lamports,
                    "seller": seller,
                    "mint": mint
                }
                
        except:
                        
            pass
        
        return None


    def buy_token(self, mint: str, price: int, seller: str) -> str | None:
        
        transaction = Transaction()
        
        ITEM = PublicKey.find_program_address(
            seeds=[
                bytes(PublicKey(mint)),
                "item".encode("UTF-8"),
                bytes(PublicKey(seller))
            ],
            program_id=PublicKey(FFF_PROGRAM)
        )
                
        MARKET = PublicKey.find_program_address(
            seeds=[
                bytes(PublicKey(ITEM[0])),
                bytes(PublicKey(TOKEN_PROGRAM_ID)),
                bytes(PublicKey(mint))
            ],
            program_id=PublicKey(ASSOCIATED_TOKEN_ID)
        )
        
        USER_MINT = PublicKey.find_program_address(
            seeds=[
                bytes(PublicKey(self.payer.public_key)),
                bytes(PublicKey(TOKEN_PROGRAM_ID)),
                bytes(PublicKey(mint)),
            ],
            program_id=PublicKey(ASSOCIATED_TOKEN_ID)
        )
        
        FOXY_SELLER = PublicKey.find_program_address(
            seeds=[
                bytes(PublicKey(seller)),
                bytes(PublicKey(TOKEN_PROGRAM_ID)),
                bytes(PublicKey(FOXY_ID)),
            ],
            program_id=PublicKey(ASSOCIATED_TOKEN_ID)
        )
        
        FOXY_BUYER = PublicKey.find_program_address(
            seeds=[
                bytes(PublicKey(self.payer.public_key)),
                bytes(PublicKey(TOKEN_PROGRAM_ID)),
                bytes(PublicKey(FOXY_ID)),
            ],
            program_id=PublicKey(ASSOCIATED_TOKEN_ID)
        )
        
        keys = [
            AccountMeta(pubkey=PublicKey(ITEM[0]), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(self.payer.public_key), is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(seller), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(mint), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(FFF_TRESAURY), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(FFF_TRESAURY), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(MARKET[0]), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(USER_MINT[0]), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(FOXY_ID), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(FOXY_SELLER[0]), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(FOXY_BUYER[0]), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(ASSOCIATED_TOKEN_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM), is_signer=False, is_writable=False),
        ]
        
        price_data = list(price.to_bytes(8, "little"))
        main_data = list(bytes.fromhex("5052c1c9d81b46b845000000000000000100000000000000"))
        fox_data = list(bytes.fromhex("7b00000000000000"))
        
        data = main_data + price_data + fox_data

        encoded_data = b58encode(bytes(data))
        data = b58decode(encoded_data)
        
        # 1 - BuyItem
        transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(FFF_PROGRAM)
            )
        )
        
        signers = [
            self.payer
        ]
        
        try:
            
            transaction.recent_blockhash = self._get_blockhash()
            transaction.sign(*signers)
            
            tx = transaction.serialize()

            tx_hash = self.client.send_raw_transaction(tx, OPTS)["result"]

            return tx_hash
        
        except:
            
            return None 
        

if __name__ == "__main__":
    
    FamousFox()