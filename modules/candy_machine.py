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

    def __init__(self, privkey: str, cmid: str, rpc: str, candy_machine_meta, collection_meta):
        
        self.cmid = cmid
        
        self.cm_meta = candy_machine_meta
        self.coll_meta = collection_meta
                
        self.client = Client(rpc)

        self.payer = Keypair.from_secret_key(b58decode(privkey))

    def create_transaction(self):
        
        self.transaction = Transaction()

        mint_account = Keypair.generate()
        payer_ata = get_associated_token_address(owner=self.payer.public_key, mint=mint_account.public_key)

        cm_wallet = self.cm_meta.wallet
        cm_auth = self.cm_meta.authority
        
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
                    dest=payer_ata,
                    mint_authority=self.payer.public_key,
                    amount=1
                )
            )
        )

        keys = [
            AccountMeta(pubkey=PublicKey(self.cmid),is_signer=False, is_writable=True),
            AccountMeta(pubkey=CANDY_MACHINE_CREATOR[0], is_signer=False, is_writable=False),
            AccountMeta(pubkey=self.payer.public_key,is_signer=True, is_writable=False),
            AccountMeta(pubkey=cm_wallet, is_signer=False, is_writable=True),
            AccountMeta(pubkey=METADATA_PROGRAM_ADDRESS[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=mint_account.public_key,is_signer=False, is_writable=True),
            AccountMeta(pubkey=self.payer.public_key,is_signer=True, is_writable=False),
            AccountMeta(pubkey=self.payer.public_key,is_signer=True, is_writable=False),
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

        if self.cm_meta.data.whitelist_mint_settings:
            
            whitelist_mint = self.cm_meta.data.whitelist_mint_settings.mint

            whitelist_associated_acc = get_associated_token_address(owner=self.payer.public_key, mint=PublicKey(whitelist_mint))

            keys.append(AccountMeta(pubkey=PublicKey(whitelist_associated_acc), is_signer=False, is_writable=True))
            keys.append(AccountMeta(pubkey=PublicKey(whitelist_mint), is_signer=False, is_writable=True))
            keys.append(AccountMeta(pubkey=PublicKey(self.payer.public_key), is_signer=True, is_writable=False))

        elif self.cm_meta.token_mint:
            
            whitelist_mint = self.cm_meta.token_mint
            
            whitelist_associated_acc = get_associated_token_address(owner=self.payer.public_key, mint=PublicKey(whitelist_mint))

            keys.append(AccountMeta(pubkey=PublicKey(whitelist_associated_acc), is_signer=False, is_writable=True))
            keys.append(AccountMeta(pubkey=PublicKey(self.payer.public_key), is_signer=True, is_writable=False))

            
        self.transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(CANDY_MACHINE_PROGRAM_ID)
            )
        )

        collection_mint = self.coll_meta.mint if self.coll_meta else None
        
        if collection_mint:
                        
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
                    bytes(PublicKey(collection_mint)),
                ],
                program_id=PublicKey(METADATA_PROGRAM_ID)
            )

            COLLECTION_EDITION = PublicKey.find_program_address(
                seeds=[
                    "metadata".encode("utf-8"),
                    bytes(PublicKey(METADATA_PROGRAM_ID)),
                    bytes(PublicKey(collection_mint)),
                    "edition".encode("utf-8")
                ],
                program_id=PublicKey(METADATA_PROGRAM_ID)
            )


            COLLECTION_RECORD = PublicKey.find_program_address(
                seeds=[
                    "metadata".encode("utf-8"),
                    bytes(PublicKey(METADATA_PROGRAM_ID)),
                    bytes(PublicKey(collection_mint)),
                    "collection_authority".encode("utf-8"),
                    bytes(PublicKey(COLLECTION_PDA[0]))
                ],
                program_id=PublicKey(METADATA_PROGRAM_ID)
            )

            keys = [
                AccountMeta(pubkey=PublicKey(self.cmid), is_writable=False, is_signer=False),
                AccountMeta(pubkey=METADATA_PROGRAM_ADDRESS[0], is_writable=False, is_signer=False),
                AccountMeta(pubkey=self.payer.public_key, is_signer=True, is_writable=False),
                AccountMeta(pubkey=COLLECTION_PDA[0], is_writable=True, is_signer=False),
                AccountMeta(pubkey=PublicKey(METADATA_PROGRAM_ID), is_signer=False, is_writable=False),
                AccountMeta(pubkey=PublicKey(SYSTEM_INSTRUCTIONS_PROGRAM), is_signer=False, is_writable=False),
                AccountMeta(pubkey=PublicKey(collection_mint), is_signer=False, is_writable=False),
                AccountMeta(pubkey=COLLECION_METADATA[0], is_writable=True, is_signer=False),
                AccountMeta(pubkey=COLLECTION_EDITION[0], is_writable=False, is_signer=False),
                AccountMeta(pubkey=cm_auth, is_signer=False, is_writable=False),
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

        except:
                                    
            return False


if __name__ == "__main__":

    CandyMachinev2()
