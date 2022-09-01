from anchorpy import Wallet
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.transaction import Transaction, TransactionInstruction, AccountMeta
from spl.token.instructions import create_associated_token_account, transfer_checked, TransferCheckedParams, burn, BurnParams, get_associated_token_address, close_account, CloseAccountParams
from solana.rpc.types import TxOpts
from base58 import b58decode
from solana.system_program import TransferParams, transfer


from utils.solana import get_blockhash, get_nft_metadata

SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
SYSTEM_RECENT_BLOCKHASH_PROGRAM = 'SysvarRecentB1ockHashes11111111111111111111'
SYSTEM_INSTRUCTIONS_PROGRAM = 'Sysvar1nstructions1111111111111111111111111'
TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
ASSOCIATED_TOKEN_ID = 'ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL'
METADATA_PROGRAM_ID = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'

NFT_TRANSFER_PROGRAM = "DeJBGdMFa1uynnnKiwrVioatTuHmNLpyFKnmB5kaFdzQ"
BURN_PROGRAM = "burn68h9dS2tvZwtCFMt79SyaEgvqtcZZWJphizQxgt"


class SolWalletManager():
    
    def __init__(self, rpc: str, privkey: str):
        
        self.rpc = rpc
        self.client = Client(rpc)
        
        self.payer = Keypair.from_secret_key(b58decode(privkey))

    def transfer_sol(self, amount: int, to_address: str):

        OPTS = TxOpts(skip_preflight=True, skip_confirmation=True)

        transaction = Transaction()
        
        
        transaction.add(
            transfer(
                TransferParams(
                    from_pubkey=PublicKey(self.payer.public_key),
                    to_pubkey=PublicKey(to_address),
                    lamports=amount
                )
            )
        )
        
        signers = [
            self.payer
        ]
        
        try:
            
            transaction.recent_blockhash = get_blockhash(self.rpc)
            transaction.sign(*signers)
            
            tx = transaction.serialize()

            tx_hash = self.client.send_raw_transaction(tx, OPTS)['result']
            
            return tx_hash

        except:
                                                
            return False
        
    def transfer_nft(self, mint_address: str, to_address: str):

        OPTS = TxOpts(skip_preflight=True, skip_confirmation=True)

        transaction = Transaction(fee_payer=self.payer.public_key)
                
        transaction.add(
            TransactionInstruction(
                keys=[
                    AccountMeta(pubkey=PublicKey(to_address),is_signer=False, is_writable=False)
                ],
                program_id=PublicKey(NFT_TRANSFER_PROGRAM),
                data=b58decode("11111111111111111111111111111111")
            )
        )

        token_ata = get_associated_token_address(owner=PublicKey(to_address), mint=PublicKey(mint_address))

        try:
            
            check_account = self.client.get_account_info(token_ata)

        except:
            
            return None
        
        if not check_account['result']['value']:
            transaction.add(
                create_associated_token_account(
                    payer=self.payer.public_key,
                    owner=PublicKey(to_address),
                    mint=PublicKey(mint_address)
                )
            )


        try:
            
            tokenholder = PublicKey(self.client.get_token_largest_accounts(mint_address)['result']['value'][0]['address'])

        except:
            
            return None
        
        transaction.add(
            transfer_checked(
                TransferCheckedParams(
                    amount=1,
                    dest=token_ata,
                    source=tokenholder,
                    owner=self.payer.public_key,
                    decimals=0,
                    program_id=PublicKey(TOKEN_PROGRAM_ID),
                    mint=PublicKey(mint_address),
                    signers=[]
                )
            ))
        
        signers = [
            self.payer
        ]
        
        try:
            
            transaction.recent_blockhash = get_blockhash(self.rpc)
            transaction.sign(*signers)
            
            tx = transaction.serialize()

            tx_hash = self.client.send_raw_transaction(tx, OPTS)['result']
            
            return tx_hash

        except:
                                                
            return False
    

        
    def burn_nft(self, mint: str):
        
        OPTS = TxOpts(skip_preflight=True, skip_confirmation=True)
        
        transaction = Transaction()
        
        token_ata = get_associated_token_address(owner=self.payer.public_key, mint=PublicKey(mint))
        
        transaction.add(
            burn(
                BurnParams(
                    program_id=PublicKey(TOKEN_PROGRAM_ID),
                    account=token_ata,
                    mint=PublicKey(mint),
                    owner=self.payer.public_key,
                    amount=1,
                    signers=[]
                )
            )
        )
        
        transaction.add(
            close_account(
                CloseAccountParams(
                    program_id=PublicKey(TOKEN_PROGRAM_ID),
                    account=token_ata,
                    dest=self.payer.public_key,
                    owner=self.payer.public_key,
                    signers=[]
                )
            )
        )
        
        signers = [
            self.payer
        ]
        
        try:
            
            transaction.recent_blockhash = get_blockhash(self.rpc)
            transaction.sign(*signers)
            
            tx = transaction.serialize()

            tx_hash = self.client.send_raw_transaction(tx, OPTS)['result']
            
            return tx_hash

        except:
                                                
            return False
    
    def full_burn_nft(self, mint: str):
        
        OPTS = TxOpts(skip_preflight=True, skip_confirmation=True)

        transaction = Transaction()
        
        payer_ata = get_associated_token_address(owner=self.payer.public_key, mint=PublicKey(mint))
        
        transaction.add(
            TransactionInstruction(
                keys=[],
                program_id=PublicKey("F6fmDVCQfvnEq2KR8hhfZSEczfM9JK9fWbCsYJNbTGn7"),
                data=bytes.fromhex("afaf6d1f0d989bed")
            )
        )
        
        EDITION_PROGRAM_ADDRESS = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(mint)),
                'edition'.encode('utf-8')
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )
        
        METADATA_PROGRAM_ADDRESS = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(mint))
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )
        
        
        nft_metadata = get_nft_metadata(mint, self.rpc)
        
        keys = [
            AccountMeta(pubkey=METADATA_PROGRAM_ADDRESS[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(self.payer.public_key), is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(mint), is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(payer_ata), is_signer=False, is_writable=True),
            AccountMeta(pubkey=EDITION_PROGRAM_ADDRESS[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID), is_signer=False, is_writable=False)
        ]
        
        if nft_metadata["collection"]:
            
            COLLECTION_METADATA = PublicKey.find_program_address(
                seeds=[
                    'metadata'.encode('utf-8'),
                    bytes(PublicKey(METADATA_PROGRAM_ID)),
                    bytes(PublicKey(nft_metadata["collection"]))
                ],
                program_id=PublicKey(METADATA_PROGRAM_ID)
            )
            
            keys.append(AccountMeta(pubkey=COLLECTION_METADATA[0], is_writable=True, is_signer=False))
            
        transaction.add(
            TransactionInstruction(
                keys=keys,
                program_id=PublicKey(METADATA_PROGRAM_ID),
                data=bytes.fromhex("1d")
            )
        )

        signers = [
            self.payer
        ]
        
        try:
            
            transaction.recent_blockhash = get_blockhash(self.rpc)
            transaction.sign(*signers)
            
            tx = transaction.serialize()

            tx_hash = self.client.send_raw_transaction(tx, OPTS)['result']
            
            return tx_hash

        except:
                                                
            return False
        

        
if __name__ == "__main__":
    
    SolWalletManager()
        
        