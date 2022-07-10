from anchorpy import Program
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
import time
from solana.rpc.core import UnconfirmedTxError


SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
SYSTEM_RECENT_BLOCKHASH_PROGRAM = 'SysvarRecentB1ockHashes11111111111111111111'
SYSTEM_INSTRUCTIONS_PROGRAM = 'Sysvar1nstructions1111111111111111111111111'
TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
ASSOCIATED_TOKEN_ID = 'ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL'
METADATA_PROGRAM_ID = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'

CANDY_MACHINE_PROGRAM_ID = 'cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ'

OPTS = TxOpts(skip_preflight=True, skip_confirmation=False, preflight_commitment=Commitment("confirmed"))

class CandyMachinev2():

    def __init__(self, privkey: str, cmid: str, rpc: str, candy_machine_meta: Program, collection_meta: Program):
        
        self.cmid = cmid
        
        self.cm_wallet = candy_machine_meta.wallet
        self.cm_auth = candy_machine_meta.authority
        
        self.whitelist_mint = candy_machine_meta.data.whitelist_mint_settings.mint if candy_machine_meta.data.whitelist_mint_settings else None
        self.collection_mint = collection_meta.mint if collection_meta else None
        
        self.go_live_date = int(candy_machine_meta.data.go_live_date)

        self.client = Client(rpc)

        self.payer = Keypair.from_secret_key(b58decode(privkey))

    def _get_blockhash(self):

        res = self.client.get_recent_blockhash(Commitment('finalized'))

        return Blockhash(res['result']['value']['blockhash'])

    def create_transaction(self):
        
        self.transaction = Transaction()

        mint_account = Keypair.generate()
        associated_token_account = get_associated_token_address(owner=self.payer.public_key, mint=mint_account.public_key)

        METADATA_PROGRAM_ADDRESS = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(mint_account.public_key)
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )

        EDITION_PROGRAM_ADDRESS = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(mint_account.public_key),
                'edition'.encode('utf-8')
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )

        CANDY_MACHINE_CREATOR = PublicKey.find_program_address(
            seeds=[
                'candy_machine'.encode('utf-8'),
                bytes(PublicKey(self.cmid))
            ],
            program_id=PublicKey(CANDY_MACHINE_PROGRAM_ID)
        )

        self.transaction.add(
            create_account(
                CreateAccountParams(
                    from_pubkey=self.payer.public_key,
                    new_account_pubkey=mint_account.public_key,
                    lamports=1461600,
                    space=82,
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

        keys = [
            AccountMeta(pubkey=PublicKey(self.cmid),is_signer=False, is_writable=True),
            AccountMeta(pubkey=CANDY_MACHINE_CREATOR[0], is_signer=False, is_writable=False),
            AccountMeta(pubkey=self.payer.public_key,is_signer=True, is_writable=True),
            AccountMeta(pubkey=self.cm_wallet, is_signer=False, is_writable=True),
            AccountMeta(pubkey=METADATA_PROGRAM_ADDRESS[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=mint_account.public_key,is_signer=True, is_writable=True),
            AccountMeta(pubkey=self.payer.public_key,is_signer=True, is_writable=True),
            AccountMeta(pubkey=self.payer.public_key,is_signer=True, is_writable=True),
            AccountMeta(pubkey=EDITION_PROGRAM_ADDRESS[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(METADATA_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_CLOCK_PROGRAM),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RECENT_BLOCKHASH_PROGRAM),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_INSTRUCTIONS_PROGRAM),is_signer=False, is_writable=False)
        ]

        creator_bump = [CANDY_MACHINE_CREATOR[1]]
        main_data = list(bytes.fromhex("d33906a70fdb23fb"))
        
        data = main_data + creator_bump

        encoded_data = b58encode(bytes(data))
        data = b58decode(encoded_data)

        self.signers = [
            self.payer,
            mint_account
        ]

        if self.whitelist_mint:

            whitelist_burn = Keypair.generate()
            whitelist_associated_acc = get_associated_token_address(owner=self.payer.public_key, mint=PublicKey(self.whitelist_mint))

            self.signers.append(whitelist_burn)

            keys.append(AccountMeta(pubkey=PublicKey(whitelist_burn.public_key), is_signer=True, is_writable=False))
            keys.append(AccountMeta(pubkey=PublicKey(whitelist_associated_acc), is_signer=False, is_writable=True))
            keys.append(AccountMeta(pubkey=PublicKey(self.whitelist_mint), is_signer=False, is_writable=True))

            if int(time.time()) < self.go_live_date:

                self.transaction.add(
                    approve(
                        ApproveParams(
                            program_id=PublicKey(TOKEN_PROGRAM_ID),
                            source=whitelist_associated_acc,
                            delegate=whitelist_burn.public_key,
                            owner=self.payer.public_key,
                            amount=1,
                            signers=[]
                        )
                    )
                )

        self.transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(CANDY_MACHINE_PROGRAM_ID)
            )
        )

        if not self.collection_mint:
            
            return
        
        COLLECTION_PDA = PublicKey.find_program_address(
            seeds=[
                "collection".encode("utf-8"),
                bytes(PublicKey(self.cmid)),
            ],
            program_id=PublicKey(CANDY_MACHINE_PROGRAM_ID)
        )

        COLLECION_METADATA = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(self.collection_mint)),
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )

        COLLECTION_EDITION = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(self.collection_mint)),
                "edition".encode("utf-8")
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )


        COLLECTION_RECORD = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(self.collection_mint)),
                "collection_authority".encode("utf-8"),
                bytes(PublicKey(COLLECTION_PDA[0]))
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )

        keys = [
            AccountMeta(pubkey=PublicKey(self.cmid), is_writable=True, is_signer=False),
            AccountMeta(pubkey=METADATA_PROGRAM_ADDRESS[0], is_writable=True, is_signer=False),
            AccountMeta(pubkey=self.payer.public_key, is_signer=True, is_writable=True),
            AccountMeta(pubkey=COLLECTION_PDA[0], is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(METADATA_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_INSTRUCTIONS_PROGRAM), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(self.collection_mint), is_signer=False, is_writable=False),
            AccountMeta(pubkey=COLLECION_METADATA[0], is_writable=False, is_signer=False),
            AccountMeta(pubkey=COLLECTION_EDITION[0], is_writable=False, is_signer=False),
            AccountMeta(pubkey=self.cm_auth, is_signer=False, is_writable=True),
            AccountMeta(pubkey=COLLECTION_RECORD[0], is_writable=False, is_signer=False)
        ]

        data = "6711c819765f7d3d"

        encoded_data = b58encode(bytes.fromhex(data))
        data = b58decode(encoded_data)
        
        self.transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(CANDY_MACHINE_PROGRAM_ID)
            )
        )
        
        

    def simulate_transaction(self):

        try:

            simul_tx = self.transaction
            
            simul_tx.sign(*self.signers)
            
            simul_hash = self.client.simulate_transaction(simul_tx)

            return not simul_hash["result"]["value"]["err"]

        except:

            return False

    def send_transaction(self):

        try:
            
            self.transaction.sign(*self.signers)
            
            tx = self.transaction.serialize()

            tx_hash = self.client.send_raw_transaction(tx, OPTS)['result']
            
            return tx_hash

        except UnconfirmedTxError:

            return None

        except Exception as e:
            
            print(e)

            return False


if __name__ == "__main__":

    CandyMachinev2()
