from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.system_program import create_account, CreateAccountParams
from spl.token.instructions import InitializeMintParams, MintToParams, create_associated_token_account, get_associated_token_address, initialize_mint, initialize_mint, mint_to, ApproveParams, approve
from solana.transaction import Transaction, TransactionInstruction, AccountMeta
from solana.rpc.types import TxOpts
from solana.blockhash import Blockhash
from solana.rpc.commitment import Commitment
from base58 import b58decode, b58encode
from solana.rpc.core import UnconfirmedTxError


SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
SYSTEM_RECENT_BLOCKHASH_PROGRAM = 'SysvarRecentB1ockHashes11111111111111111111'
SYSTEM_INSTRUCTIONS_PROGRAM = 'Sysvar1nstructions1111111111111111111111111'
TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
ASSOCIATED_TOKEN_ID = 'ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL'
METADATA_PROGRAM_ID = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'
COMPUTE_BUDGET_PROGRAM = "ComputeBudget111111111111111111111111111111"

USDC_COIN = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

ML_PROGRAM = 'minwAEdewYNqagUwzrVBUGWuo277eeSMwEwj76agxYd'
ML_AUTH = "mnKzuL9RMtR6GeSHBfDpnQaefcMsiw7waoTSduKNiXM"
ML_WALLET = "7FHzVCP9eX6zmZjw3qwvmdDMhSvCkLxipQatAqhtbVBf"
ML_USDC_ATA = "Gdq32GtxXRr9t3BScA6VdtKZ7TFu62d6HBhrNFMZNto9"

OPTS = TxOpts(skip_preflight=True, skip_confirmation=False, preflight_commitment=Commitment("confirmed"))

class MonkeLabsLaunchpad():

    def __init__(self, privkey: str, rpc: str, accounts: dict):

        self.accounts = accounts
        
        self.client = Client(rpc)

        self.payer = Keypair.from_secret_key(b58decode(privkey))

    def _get_blockhash(self):

        res = self.client.get_recent_blockhash(Commitment('finalized'))

        return Blockhash(res['result']['value']['blockhash'])

    def create_transaction(self):

        self.transaction = Transaction()
        
        mint_account = Keypair.generate()
        
        payer_ata = get_associated_token_address(owner=self.payer.public_key, mint=mint_account.public_key)
        usdc_ata = get_associated_token_address(owner=self.payer.public_key, mint=PublicKey(USDC_COIN))
        
        data = "003057050000000000"

        encoded_data = b58encode(bytes.fromhex(data))
        data = b58decode(encoded_data)
        
        self.transaction.add(
            TransactionInstruction(
                keys=[],
                data=data,
                program_id=PublicKey(COMPUTE_BUDGET_PROGRAM)
            )
        )
        
        keys = [
            AccountMeta(pubkey=self.payer.public_key, is_signer=True, is_writable=True),
            AccountMeta(pubkey=mint_account.public_key, is_signer=True, is_writable=True),
            AccountMeta(pubkey=payer_ata, is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(ASSOCIATED_TOKEN_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM), is_signer=False, is_writable=False),
        ]
        
        data = "64"
    
        encoded_data = b58encode(bytes.fromhex(data))
        data = b58decode(encoded_data)
        
        self.transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(ML_PROGRAM)
            )
        )
        
        MINT_METADATA = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(mint_account.public_key))
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )

        pda_buffer = int(self.accounts["REACT_APP_PDA_BUFFER"])
        
        PROGRAM_AUTH = PublicKey.find_program_address(
            seeds=[
                bytes([255 & pda_buffer, (65280 & pda_buffer) >> 8]),
                "auth".encode("utf-8"),
                bytes(PublicKey(ML_PROGRAM))
            ],
            program_id=PublicKey(ML_PROGRAM)
        )

        PAYER_AUTH = PublicKey.find_program_address(
            seeds=[
                bytes([255 & pda_buffer, (65280 & pda_buffer) >> 8]),
                bytes(PublicKey(self.payer.public_key)),
                bytes(PublicKey(ML_PROGRAM))
            ],
            program_id=PublicKey(ML_PROGRAM)
        )

        MINT_EDITION = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(mint_account.public_key),
                'edition'.encode('utf-8')
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )

        LTIME = PublicKey.find_program_address(
            seeds=[
                "ltime".encode("utf-8"),
                bytes(PublicKey(self.payer.public_key)),
                bytes(PublicKey(ML_PROGRAM))
            ],
            program_id=PublicKey(ML_PROGRAM)
        )
        
        COLLECTION_EDITION = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(self.accounts["REACT_APP_COLLECTION_KEY"])),
                'edition'.encode('utf-8')
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )

        COLLECTION_METADATA = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(self.accounts["REACT_APP_COLLECTION_KEY"])),
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )
        

        keys = [
            AccountMeta(pubkey=self.payer.public_key, is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(self.accounts["REACT_APP_CONFIG_KEY"]), is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(self.accounts["REACT_APP_PRIMARY_WALLET"]), is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(ML_AUTH), is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(self.accounts["REACT_APP_INDEX_KEY"]), is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(self.accounts["REACT_APP_WHITELIST_KEY"] or Keypair.generate().public_key), is_signer=False, is_writable=False),
            AccountMeta(pubkey=payer_ata, is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=MINT_METADATA[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=mint_account.public_key, is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(METADATA_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_INSTRUCTIONS_PROGRAM), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PAYER_AUTH[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=LTIME[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=MINT_EDITION[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(ML_WALLET), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(USDC_COIN), is_signer=False, is_writable=False),
            AccountMeta(pubkey=usdc_ata, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(ML_USDC_ATA), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(self.accounts["REACT_APP_COLLECTION_KEY"]), is_signer=False, is_writable=False),
            AccountMeta(pubkey=COLLECTION_EDITION[0], is_signer=False, is_writable=False),
            AccountMeta(pubkey=COLLECTION_METADATA[0], is_signer=False, is_writable=False),
            AccountMeta(pubkey=PROGRAM_AUTH[0], is_signer=False, is_writable=True),
        ]
        
        data = "0a01"
        
        encoded_data = b58encode(bytes.fromhex(data))
        data = b58decode(encoded_data)
        
        self.transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(ML_PROGRAM)
            )
        )

        data = "fa"

        encoded_data = b58encode(bytes.fromhex(data))
        data = b58decode(encoded_data)
        
        self.transaction.add(
            TransactionInstruction(
                keys=[],
                data=data,
                program_id=PublicKey(ML_PROGRAM)
            )
        )

        self.signers = [
            self.payer,
            mint_account
        ]

    def send_transaction(self):

        try:
            
            self.transaction.sign(*self.signers)
            
            tx = self.transaction.serialize()

            tx_hash = self.client.send_raw_transaction(tx, OPTS)['result']
            
            return tx_hash

        except UnconfirmedTxError:

            return None

        except:
            
            return False



if __name__ == "__main__":

    MonkeLabsLaunchpad()
