from anchorpy import Wallet
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Commitment
from solana.blockhash import Blockhash
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction, Transaction
from solana.system_program import create_account, CreateAccountParams
from spl.token.instructions import InitializeMintParams, MintToParams, create_associated_token_account, get_associated_token_address, initialize_mint, mint_to
from base58 import b58decode, b58encode
from solana.rpc.core import UnconfirmedTxError


TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
METADATA_PROGRAM_ID = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'
SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
METADATA_PUBLIC_KEY = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
ASSOCIATED_TOKEN_ID = 'ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL'
COMPUTE_BUDGET_ID = "ComputeBudget111111111111111111111111111111"

LMN_PROGRAM = "ArAA6CZC123yMJLUe4uisBEgvfuw2WEvex9iFmFCYiXv"
LMN_TRESAURY = "33nQCgievSd3jJLSWFBefH3BJRN7h6sAoS82VFFdJGF5"

OPTS = TxOpts(skip_preflight=True, skip_confirmation=False, preflight_commitment=Commitment("confirmed"))
    
class LaunchMyNftLaunchpad():

    def __init__(self, privkey: str, rpc: str, cmid: str, candy_machine_meta):

        self.cmid = cmid
        
        self.cm_meta = candy_machine_meta
                
        self.client = Client(rpc)
        self.payer = Keypair.from_secret_key(b58decode(privkey))

    def _get_blockhash(self):

        res = self.client.get_recent_blockhash(Commitment('finalized'))

        return Blockhash(res['result']['value']['blockhash'])

    def create_transaction(self):

        self.transaction = Transaction()
        
        self.mint_account = Keypair.generate()

        buyer_ata = get_associated_token_address(owner=self.payer.public_key, mint=self.mint_account.public_key)

        self.transaction.add(
            TransactionInstruction(
                keys=[],
                data=bytes.fromhex("00605b030010270000"),
                program_id=PublicKey(COMPUTE_BUDGET_ID)
            )
        )
        
        METADATA_PROGRAM_ADDRESS = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PUBLIC_KEY)),
                bytes(self.mint_account.public_key)
            ],
            program_id=PublicKey(METADATA_PUBLIC_KEY)
        )

        EDITION_PROGRAM_ADDRESS = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PUBLIC_KEY)),
                bytes(self.mint_account.public_key),
                'edition'.encode('utf-8')
            ],
            program_id=PublicKey(METADATA_PUBLIC_KEY)
        )

        TOTAL_MINTS = PublicKey.find_program_address(
            seeds=[
                'TotalMints'.encode('utf-8'),
                bytes(PublicKey(self.payer.public_key)),
                bytes(PublicKey(self.cmid)),
            ],
            program_id=PublicKey(LMN_PROGRAM)
        )
        keys = [
            AccountMeta(pubkey=PublicKey(self.cmid),is_writable=True, is_signer=False),
            AccountMeta(pubkey=self.payer.public_key,is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(self.cm_meta.wallet),is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(LMN_TRESAURY),is_writable=True, is_signer=False),
            AccountMeta(pubkey=METADATA_PROGRAM_ADDRESS[0], is_writable=True, is_signer=False),
            AccountMeta(pubkey=self.mint_account.public_key,is_writable=True, is_signer=True),
            AccountMeta(pubkey=buyer_ata, is_writable=True, is_signer=False),
            AccountMeta(pubkey=EDITION_PROGRAM_ADDRESS[0], is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(TOTAL_MINTS[0]), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(ASSOCIATED_TOKEN_ID),is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(METADATA_PROGRAM_ID),is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID),is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM),is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_CLOCK_PROGRAM),is_signer=False, is_writable=False)
        ]

        price_data = list(int(self.cm_meta.data.price).to_bytes(8, "little"))
        main_data = list(bytes.fromhex("4f47cf20b2661513000000000000000000000000"))

        data = main_data + price_data

        encoded_data = b58encode(bytes(data))
        data = b58decode(encoded_data)

        self.transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(LMN_PROGRAM)
            )
        )

        self.signers = [
            self.payer,
            self.mint_account
        ]

        
    def send_transaction(self):

            
        try:
            
            self.transaction.sign(*self.signers)
            
            tx = self.transaction.serialize(verify_signatures=False)

            tx_hash = self.client.send_raw_transaction(tx, OPTS)['result']
            
            return tx_hash

        except UnconfirmedTxError:

            return None

        except:
                                                
            return False



if __name__ == "__main__":

    LaunchMyNftLaunchpad()
