from solana.rpc.api import Client
from solana.rpc import types
from solana.rpc.commitment import Commitment
from solana.blockhash import Blockhash
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction, Transaction
from solana.system_program import create_account, CreateAccountParams
from spl.token.instructions import InitializeMintParams, MintToParams, create_associated_token_account, get_associated_token_address, initialize_mint, mint_to
from base58 import b58decode, b58encode
from solana.rpc.core import UnconfirmedTxError
from anchorpy import Program


TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
METADATA_PROGRAM_ID = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'
SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
METADATA_PUBLIC_KEY = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'

LMN_PROGRAM = "ArAA6CZC123yMJLUe4uisBEgvfuw2WEvex9iFmFCYiXv"
LMN_TRESAURY = "33nQCgievSd3jJLSWFBefH3BJRN7h6sAoS82VFFdJGF5"

OPTS = types.TxOpts(skip_preflight=True, skip_confirmation=False)
MINT_LEN = 82

class LaunchMyNftLaunchpad():

    def __init__(self, privkey: str, rpc: str, cmid: str, candy_machine_meta: Program):

        self.cmid = cmid
        self.wallet = candy_machine_meta.wallet

        self.client = Client(rpc)
        self.payer = Keypair.from_secret_key(b58decode(privkey))
        self.transaction = Transaction(fee_payer=self.payer.public_key)

    def _get_blockhash(self):

        res = self.client.get_recent_blockhash(Commitment('finalized'))

        return Blockhash(res['result']['value']['blockhash'])

    def create_transaction(self):

        mint_account = Keypair.generate()

        self.transaction.add(
            create_account(
                CreateAccountParams(
                    from_pubkey=self.payer.public_key,
                    new_account_pubkey=mint_account.public_key,
                    lamports=self.client.get_minimum_balance_for_rent_exemption(MINT_LEN)['result'],
                    space=MINT_LEN,
                    program_id=PublicKey(TOKEN_PROGRAM_ID)
                )
            )
        )

        self.transaction.add(
            initialize_mint(
                InitializeMintParams(
                    program_id=PublicKey(TOKEN_PROGRAM_ID),
                    mint=mint_account.public_key,
                    decimals=0,
                    mint_authority=self.payer.public_key,
                    freeze_authority=self.payer.public_key
                )
            )
        )

        associated_token_account = get_associated_token_address(owner=self.payer.public_key, mint=mint_account.public_key)

        self.transaction.add(
            create_associated_token_account(
                payer=self.payer.public_key,
                owner=self.payer.public_key,
                mint=mint_account.public_key
            )
        )

        self.transaction.add(
            mint_to(
                MintToParams(
                    program_id=PublicKey(TOKEN_PROGRAM_ID),
                    mint=mint_account.public_key,
                    dest=associated_token_account,
                    mint_authority=self.payer.public_key,
                    amount=1
                )
            )
        )

        CANDY_MACHINE_CREATOR = PublicKey.find_program_address(
            seeds=[
                "candy_machine".encode("utf-8"),
                bytes(PublicKey(self.cmid))

            ],
            program_id=PublicKey(LMN_PROGRAM)
        )

        METADATA_PROGRAM_ADDRESS = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PUBLIC_KEY)),
                bytes(mint_account.public_key)
            ],
            program_id=PublicKey(METADATA_PUBLIC_KEY)
        )

        EDITION_PROGRAM_ADDRESS = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PUBLIC_KEY)),
                bytes(mint_account.public_key),
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
            AccountMeta(pubkey=CANDY_MACHINE_CREATOR[0], is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(self.wallet),is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(LMN_TRESAURY),is_writable=True, is_signer=False),
            AccountMeta(pubkey=METADATA_PROGRAM_ADDRESS[0], is_writable=True, is_signer=False),
            AccountMeta(pubkey=mint_account.public_key,is_writable=True, is_signer=True),
            AccountMeta(pubkey=EDITION_PROGRAM_ADDRESS[0], is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(TOTAL_MINTS[0]), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(METADATA_PROGRAM_ID),is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID),is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM),is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_CLOCK_PROGRAM),is_signer=False, is_writable=False)

        ]

        creator_bump = hex(CANDY_MACHINE_CREATOR[1]).replace("0x", "")
        total_mints_bump = hex(TOTAL_MINTS[1]).replace("0x", "")

        data = "78791792ad6ec7cd" + creator_bump + total_mints_bump + "0100000000"

        encoded_data = b58encode(bytes.fromhex(data))

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
            mint_account
        ]

    def sign_transaction(self):
        
        try:
            
            self.transaction.recent_blockhash = self._get_blockhash()
            self.transaction.sign(*self.signers)
            
            return True
        
        except:
            
            return None
        
    def send_transaction(self):

        try:

            txn = self.transaction.serialize()

            tx_hash = self.client.send_raw_transaction(txn, OPTS)['result']

            return tx_hash

        except UnconfirmedTxError:

            return None

        except:

            return False


if __name__ == "__main__":

    LaunchMyNftLaunchpad()
