from base64 import b64decode
import json
import math
import requests
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
from urllib.parse import urlsplit   
from utils.bypass import create_tls_payload

SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
SYSTEM_RECENT_BLOCKHASH_PROGRAM = 'SysvarRecentB1ockHashes11111111111111111111'
SYSTEM_INSTRUCTIONS_PROGRAM = 'Sysvar1nstructions1111111111111111111111111'
TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
ASSOCIATED_TOKEN_ID = 'ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL'
METADATA_PROGRAM_ID = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'

EXCHANGE_PROGRAM = "EXBuYPNgBUXMTsjCbezENRUtFQzjUNZxvPGTd11Pznk5"
EXCHANGE_WALLET = "6482e33zrerYfhKAjPR2ncMSrH2tbTy5LDjdhB5PXzxd"

OPTS = TxOpts(skip_preflight=True, skip_confirmation=False, preflight_commitment=Commitment("confirmed"))

class ExchangeArt():
    
    
    def __init__(self, privkey: str, rpc: str, contract: dict) -> None:
        
        
        self.client = Client(rpc)
        
        self.payer = Keypair.from_secret_key(b58decode(privkey))
        
        contract_info = contract["contractGroups"][0]["availableContracts"]["editionSales"][0]
        
        self.contract_data = contract_info["data"]
        self.contract_keys = contract_info["keys"]
        
        mint_info = contract["contractGroups"][0]["mint"]
        
        self.supply = mint_info["masterEditionAccount"]["maxSupply"]
        self.creators = [acc["address"] for acc in mint_info["metadataAccount"]["creators"]] if mint_info["metadataAccount"].get("creators") else []

    def _get_blockhash(self):

        res = self.client.get_recent_blockhash(Commitment('finalized'))

        return Blockhash(res['result']['value']['blockhash'])
    
    
    @staticmethod
    def get_collection_supply(mint_key: str, rpc):
        
        mint_auth = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(mint_key)),
                "edition".encode("utf-8")
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )[0]

        client = Client(rpc)
        
        try:
                
            res = client.get_account_info(mint_auth, commitment=Commitment("processed"))

            data = res["result"]["value"]["data"][0]

            data = b64decode(data)

            if len(data) != 282:
                
                return None
            
            minted = int.from_bytes(data[1:9], "little")
            available = int.from_bytes(data[10:18], "little")
            
            return (minted, available)    

        except:
                        
            return None
        
    @staticmethod
    def get_hmac_code(wallet_address: str):
        
        url = f"https://api.exchange.art/v2/mints/editions/pass?address={wallet_address}"
        
        headers = {
            'authorization': 'api.exchange.art',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'content-type': 'application/json',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-recaptcha-token': 'AV64Ye1fCaAhPlZxdggX0KaZk9s7liUIO6oCgCO1oOTdIQpsVhIEHkNhz6xMpRJPx7zaisd5rYKaBFK9FwUTioUTalMLXv7vb7m-xNuCplMXJEYeQYwH47-mHkYRIy-lY6ikk7Kxx7FNQA6VleTwXOEdfQ:U=f27260e800000000',
            'sec-ch-ua-platform': '"macOS"',
            'origin': 'https://exchange.art',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://exchange.art/',
            'accept-language': 'es-ES,es;q=0.9',
        }
        
        payload = create_tls_payload(
            url=url,
            headers=headers,
            method="GET"
        )
        
        try:
            
            res = requests.post("http://127.0.0.1:3000", json=payload).json()
            
            print(res)
            res = json.loads(res["body"])
            
            return res if res.get("hmacCode") else None
        
        except:
                        
            return None
    
    @staticmethod
    def get_collection_info(url: str):
        
        split_url = urlsplit(url)

        contract = split_url.path.split("/")[-1]
        
        url = f"https://api.exchange.art/v2/mints/contracts?filters[mints]={contract}&filters[nftType]=masterEditions&filters[inclUnverified]=truenull"

        headers = {
            'authority': 'api.exchange.art',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'origin': 'https://exchange.art',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://exchange.art/',
            'accept-language': 'es-ES,es;q=0.9',
        }

        payload = create_tls_payload(
            url=url,
            headers=headers,
            method="GET"
        )
        
        try:
            
            res = requests.post("http://127.0.0.1:3000", json=payload).json()
            
            res = json.loads(res["body"])
            
            return res if res.get("totalGroups") == 1 else None
        
        except:
                        
            return None
        
    def create_transaction(self, tsmp: int, hmac: list, edition_no: int):
        
        self.transaction = Transaction()
        
        mint_account = Keypair.generate()
        payer_ata = get_associated_token_address(owner=self.payer.public_key, mint=mint_account.public_key)

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
        
        MASTER_EDITION = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(self.contract_keys["mintKey"])),
                "edition".encode("utf-8")
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )
        
        MASTER_METADATA = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(self.contract_keys["mintKey"]))
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )
        
        NEW_METADATA = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(mint_account.public_key)
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )
        
        NEW_EDITION = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(mint_account.public_key),
                "edition".encode("utf-8")
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )
        
        META_EDITION_MARK_PDA = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(self.contract_keys["mintKey"])),
                "edition".encode("utf-8"),
                str(math.floor((edition_no + 1)/248)).encode("utf-8")
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )
        
        PDA_DEPOSIT_AUTH = PublicKey.find_program_address(
            seeds=[
                "exchgeditions".encode("utf-8"),
                bytes(PublicKey(self.contract_keys["mintKey"])),
                bytes(PublicKey(EXCHANGE_PROGRAM))
            ],
            program_id=PublicKey(EXCHANGE_PROGRAM)
        )
        
        keys = [
            AccountMeta(pubkey=self.payer.public_key, is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(self.contract_keys["mintKey"]), is_signer=False, is_writable=False),
            AccountMeta(pubkey=MASTER_EDITION[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=MASTER_METADATA[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(self.contract_keys["initializer"]), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(self.contract_keys["saleAccount"]), is_signer=False, is_writable=True),
            AccountMeta(pubkey=NEW_METADATA[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=NEW_EDITION[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=mint_account.public_key, is_signer=False, is_writable=True),
            AccountMeta(pubkey=META_EDITION_MARK_PDA[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(self.contract_keys["depositAccount"]), is_signer=False, is_writable=True),
            AccountMeta(pubkey=payer_ata, is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(EXCHANGE_WALLET), is_signer=False, is_writable=True),
            AccountMeta(pubkey=PDA_DEPOSIT_AUTH[0], is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(METADATA_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_INSTRUCTIONS_PROGRAM), is_signer=False, is_writable=False),
        ]
        
        for creator in self.creators:
            
            keys.append(AccountMeta(pubkey=PublicKey(creator), is_signer=False, is_writable=True))
            
        main_data = list(bytes.fromhex("e3052f6278c1a906"))
        edition_num = list(int(edition_no + 1).to_bytes(8, "little"))
        time_stamp = list(int(tsmp).to_bytes(8, "little"))
        price = list(int(self.contract_data["price"]).to_bytes(8, "little"))
                
        data = main_data + edition_num + time_stamp + price + hmac

        encoded_data = b58encode(bytes(data))
        data = b58decode(encoded_data)

        self.transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(EXCHANGE_PROGRAM)
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
        