from solana.rpc.api import Client
from solana.rpc import types
from solana.rpc.commitment import Commitment
from solana.blockhash import Blockhash
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction, Transaction
from solana.system_program import create_account, CreateAccountParams
from spl.token.instructions import InitializeMintParams, MintToParams, create_associated_token_account, get_associated_token_address, initialize_mint, mint_to, initialize_account, InitializeAccountParams
from base58 import b58decode, b58encode
from solana.system_program import transfer, TransferParams, allocate, AllocateParams, assign, AssignParams
from solana.rpc.core import UnconfirmedTxError

TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
MEMO_PROGRAM_ID = 'MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr'
ME_NOTARY = '23W5dZSNiNtKXCGvcjkRAJZ6admMXQ26s3ttBaH6Lb2k'
TOKEN_METADATA_ID = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'
SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
ME_PROGRAM = "CMZYPASGWeTz7RNGHaRJfCq2XQ5pYK6nDvVQxzkH51zb"
SYSTEM_SLOT_HASHES = "SysvarS1otHashes111111111111111111111111111"
COMPUTE_BUDGET = "ComputeBudget111111111111111111111111111111"
ASSOCIATED_TOKEN_ID = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"

OPTS = types.TxOpts(skip_preflight=True, skip_confirmation=False)
MINT_LEN = 82

class MagicEdenLaunchpad():
    
    def __init__(self, privkey: str, cmid: str, rpc: str, candy_machine_meta, wallet_limit: int, price: int):

        self.config_addres = candy_machine_meta.config
        self.wallet_auth = candy_machine_meta.wallet_authority
        self.order_info = candy_machine_meta.order_info
        self.cmid = cmid
        self.wallet_limit = wallet_limit
        self.price = price
        
        self.client = Client(rpc)
        self.payer = Keypair.from_secret_key(b58decode(privkey))
        self.transaction = Transaction(fee_payer=self.payer.public_key)
        
    def _get_blockhash(self):
        
        res = self.client.get_recent_blockhash(Commitment('finalized'))
    
        return Blockhash(res['result']['value']['blockhash'])
            
    def create_transaction(self):        
        
        mint_account = Keypair.generate()
        middleman_account = Keypair.generate()
        
        self.transaction.add(
            TransactionInstruction(
                keys=[],
                program_id=PublicKey(COMPUTE_BUDGET),
                data=b58decode("16jwcDm")
            )
        )
        
        # 2 - Transfer
        self.transaction.add(
            transfer(
                TransferParams(
                    from_pubkey=self.payer.public_key,
                    to_pubkey=middleman_account.public_key,
                    lamports=self.price
                )
            )
            
        )
        
        # 3 - Allocate Account
        self.transaction.add(
            allocate(
                AllocateParams(
                    account_pubkey=middleman_account.public_key,
                    space=165
                )
            )
        )
        
        # 4 - Assign Account
        self.transaction.add(
            assign(
                AssignParams(
                    account_pubkey=middleman_account.public_key,
                    program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
                )
            )
        )
        
        # 5 - Initialize Account
        self.transaction.add(
            initialize_account(
                InitializeAccountParams(
                    program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
                    account=middleman_account.public_key,
                    mint=PublicKey(WRAPPED_SOL),
                    owner=self.payer.public_key
                )
            )
        )
        
        # 6 - Memo
        """ self.transaction.add(
            TransactionInstruction(
                keys = [],
                program_id=PublicKey(MEMO_PROGRAM_ID),
                data=b58decode("ZpjF2LSqDPUqWEuY5Zhv377mZ6yGdB3pp4z5XZoks2mJu4VkSdqhP")
            )
        ) """
        
        """ self.transaction.add(
            create_account(
                CreateAccountParams(
                    from_pubkey= self.payer.public_key,
                    new_account_pubkey= mint_account.public_key,
                    lamports= balance_needed['result'],
                    space= MINT_LEN,
                    program_id=PublicKey(TOKEN_PROGRAM_ID)
                )
            )
        )


        self.transaction.add(
            initialize_mint(
                InitializeMintParams(
                    program_id= PublicKey(TOKEN_PROGRAM_ID),
                    mint= mint_account.public_key,
                    decimals= 0,
                    mint_authority= self.payer.public_key,
                    freeze_authority= self.payer.public_key
                )
            )
        )

        self.transaction.add(
            create_associated_token_account(
                payer= self.payer.public_key,
                owner= self.payer.public_key,
                mint= mint_account.public_key
            )
        ) """

        associated_token_account = get_associated_token_address(self.payer.public_key,mint_account.public_key)
        pay_to_ata = get_associated_token_address(self.wallet_auth, PublicKey(WRAPPED_SOL))

        """ self.transaction.add(
            mint_to(
                MintToParams(
                    program_id= PublicKey(TOKEN_PROGRAM_ID),
                    mint= mint_account.public_key,
                    dest= associated_token_account,
                    mint_authority= self.payer.public_key,
                    amount= 1
                )
            )
        ) """
        
        METADATA_PROGRAM_ADDRESS = PublicKey.find_program_address(
            
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(TOKEN_METADATA_ID)),
                bytes(mint_account.public_key)
            ],

            program_id= PublicKey('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s')
        )


        EDITION_PROGRAM_ADDRESS = PublicKey.find_program_address(
            
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(TOKEN_METADATA_ID)),
                bytes(mint_account.public_key),
                'edition'.encode('utf-8')
            ],
            
            program_id= PublicKey('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s')
        )


        WALLET_LIMIT_ADDRESS = PublicKey.find_program_address(
            seeds=[
                'wallet_limit'.encode('utf-8'),
                bytes(PublicKey(self.cmid)),
                bytes(self.payer.public_key)
            ],

            program_id= PublicKey(ME_PROGRAM)
        )


        LAUNCH_STAGES_ADDRESS = PublicKey.find_program_address(
            
            seeds=[
                'candy_machine'.encode('utf-8'),
                'launch_stages'.encode('utf-8'),
                bytes(PublicKey(self.cmid)),
            ],
            
            program_id=PublicKey(ME_PROGRAM)
        )

        # 21 accs
        keys = [
            AccountMeta(PublicKey(self.config_addres), is_signer= False, is_writable= False),
            AccountMeta(PublicKey(self.cmid), is_signer= False, is_writable= True),
            AccountMeta(pubkey=self.payer.public_key, is_signer= True, is_writable=True),
            AccountMeta(pubkey=self.payer.public_key, is_signer= True, is_writable=True),
            AccountMeta(pubkey=LAUNCH_STAGES_ADDRESS[0], is_signer= False, is_writable= True),
            AccountMeta(pubkey=middleman_account.public_key, is_signer= True, is_writable= True),
            AccountMeta(pubkey=pay_to_ata, is_signer= False, is_writable= True),
            AccountMeta(pubkey=PublicKey(ME_NOTARY), is_signer= True, is_writable= False),
            AccountMeta(pubkey=METADATA_PROGRAM_ADDRESS[0], is_signer= False, is_writable= True),
            AccountMeta(pubkey=mint_account.public_key, is_signer= True, is_writable= True),
            AccountMeta(pubkey=associated_token_account, is_signer= False, is_writable= True),
            AccountMeta(pubkey=EDITION_PROGRAM_ADDRESS[0], is_signer= False, is_writable= True),
            AccountMeta(pubkey=WALLET_LIMIT_ADDRESS[0], is_signer = False, is_writable = True),
            AccountMeta(pubkey=PublicKey(self.order_info), is_signer= False, is_writable= True),
            AccountMeta(pubkey=PublicKey(SYSTEM_SLOT_HASHES), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(TOKEN_METADATA_ID), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(ASSOCIATED_TOKEN_ID), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM), is_signer= False, is_writable= False),
            AccountMeta(pubkey=PublicKey(ME_NOTARY), is_signer= True, is_writable= False),

        ]
        
        hex_data_bump = hex(WALLET_LIMIT_ADDRESS[1]).replace("0x", "")
        
        if self.wallet_limit:
            
            hex_data_limit = hex(self.wallet_limit).replace("0x", "")
            
            data = "d33906a70fdb23fb" + hex_data_bump + "00010" + hex_data_limit
        
        else:
            
            data = "d33906a70fdb23fb" + hex_data_bump + "0000"      


        encoded_data = b58encode(bytes.fromhex(data))

        data = b58decode(encoded_data)
                
        self.transaction.add(
            TransactionInstruction(
                keys=keys,
                program_id=PublicKey(ME_PROGRAM),
                data=data
            )
        )

        self.signers = [
            self.payer,
            mint_account,
            PublicKey(ME_NOTARY),
            middleman_account
        ]
            
    def sign_transaction(self):
            
        try:
            
            self.transaction.recent_blockhash = self._get_blockhash()

            self.transaction.sign_partial(PublicKey(ME_NOTARY))
            self.transaction.sign(*self.signers)

            message = self.transaction.serialize_message()
            message_encoded = b58encode(message)
            
            return message_encoded.decode('utf-8')

        except:
            
            return None

    def simulate_transaction(self):

        try:
            
            tx_hash = self.client.simulate_transaction(self.transaction)

            return not tx_hash["result"]["value"]["err"]
        
        except:

            return False

    def send_transaction(self, signature: str):
        
        try:
            
            signature_hash = b58decode(signature)

            self.transaction.add_signature(PublicKey(ME_NOTARY), signature=signature_hash)

            txn = self.transaction.serialize()
                
            tx_hash = self.client.send_raw_transaction(txn, OPTS)
            
            return tx_hash["result"]
        
        except UnconfirmedTxError:

            return None
        
        except:
            
            return False 
        
if __name__ == "__main__":

    MagicEdenLaunchpad()