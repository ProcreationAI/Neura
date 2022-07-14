from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from spl.token.instructions import get_associated_token_address
from solana.transaction import Transaction, TransactionInstruction, AccountMeta
from solana.rpc.types import TxOpts
from solana.blockhash import Blockhash
from solana.rpc.commitment import Commitment
from base58 import b58decode, b58encode
from rich.console import Console
import requests
import json

from utils.bypass import create_tls_payload
from utils.solana import get_lamports_from_listing_data

WRAPPED_SOL = "So11111111111111111111111111111111111111112"
METADATA_PROGRAM_ID = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
ASSOCIATED_TOKEN_ID = 'ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL'
SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'

AUCTION_PROGRAM = "hausS13jsjafwWwGqZTUQRmWyvyxn9EQpqMwV1PBBmk"
CC_OWNER = "8Pqp68JANeq1kBgwaQvCGA6zPbmRBxMmnPg8v7brhKxM"
CC_KEY = "29xtkHHFLUHXiLoxTzbC7U8kekTwN3mVQSkfXnB1sQ6e"
CC_FEE_ACCOUNT = "6WntYbCCnjKbt6nKXzGJgmPybZURN11aK6fUxLbrJkMc"
CC_TREASURY = "4eAqqq3B177DydnC5Du8xQEq42p2RTmf5CsU3emzNdiV"

console = Console(highlight=False, log_path=False)

class CoralCube():

    def __init__(self, rpc: str = None, privkey: str = None):

        self.client = Client(rpc)

        self.payer = Keypair.from_secret_key(b58decode(privkey))

    def _get_blockhash(self):

        res = self.client.get_recent_blockhash(Commitment('finalized'))

        return Blockhash(res['result']['value']['blockhash'])

    @staticmethod
    def _receipt_token(account: str, mint_address: str):

        return PublicKey.find_program_address(
            seeds=[
                bytes(PublicKey(account)),
                bytes(PublicKey(TOKEN_PROGRAM_ID)),
                bytes(PublicKey(mint_address))
            ],
            program_id=PublicKey(ASSOCIATED_TOKEN_ID)
        )

    @staticmethod
    def _trade_state(account: str, token_account: str, mint_address: str, price: int):

        return PublicKey.find_program_address(
            seeds=[
                "auction_house".encode("utf-8"),
                bytes(PublicKey(account)),
                bytes(PublicKey(CC_KEY)),
                bytes(PublicKey(token_account)),
                bytes(PublicKey(WRAPPED_SOL)),
                bytes(PublicKey(mint_address)),
                (price).to_bytes(8, "little"),
                (1).to_bytes(8, "little")

            ],
            program_id=PublicKey(AUCTION_PROGRAM)
        )

    @staticmethod
    def get_nft_data(mint: str) -> dict | None:

        try:

            headers = {
                'authority': 'api.coralcube.io',
                'accept': 'application/json, text/plain, */*',
                'origin': 'https://coralcube.io',
                'referer': 'https://coralcube.io/',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            }

            payload = create_tls_payload(
                url=f"https://api.coralcube.io/v1/getItem?mint={mint}",
                method="GET",
                headers=headers
            )

            res = requests.post("http://127.0.0.1:3000",
                                json=payload, timeout=3).json()

            return json.loads(res["body"])

        except:

            return None

    @staticmethod
    def get_listed_nfts(symbol: str, min_sol: float = 0, max_sol: float = 999999999, limit: int = 20, recenlty_listed: bool = False) -> list | None:

        try:

            headers = {
                'authority': 'api.coralcube.io',
                'accept': 'application/json, text/plain, */*',
                'origin': 'https://coralcube.io',
                'referer': 'https://coralcube.io/',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            }

            params = {
                "listing_status": ["listed"],
                "price_range": {
                    "currency": "sol",
                    "min_price": str(min_sol),
                    "max_price": str(max_sol)
                },
                
            }
            
            order = "price_asc"
            
            if recenlty_listed:
                
                order = "recently_listed"
            
            payload = create_tls_payload(
                url=f"https://api.coralcube.io/v1/getItems?offset=0&page_size={limit}&ranking={order}&symbol={symbol}",
                method="POST",
                headers=headers,
                params=params
            )

            res = requests.post("http://127.0.0.1:3000",
                                json=payload, timeout=3).json()
            
            return json.loads(res["body"])["items"]

        except:

            return None


    def check_tx_is_listing(self, tx: str) -> dict | None:

        try:

            tx = self.client.get_transaction(tx_sig=tx, commitment=Commitment("confirmed"))["result"]

            logs = "".join(tx["meta"]["logMessages"])
            accounts = tx["transaction"]["message"]["accountKeys"]

            if not tx["meta"]["err"] and "Instruction: Sell" in logs and tx["meta"]["postTokenBalances"] and AUCTION_PROGRAM in accounts:

                instr_data = tx["transaction"]["message"]["instructions"][-1]["data"]
                instr_data = b58decode(instr_data).hex()

                mint = tx["meta"]["postTokenBalances"][0]["mint"]
                lamports = get_lamports_from_listing_data(data=instr_data, left_offset=22, right_offset=16)
                seller = accounts[0]
                                
                return {
                    "mint": mint,
                    "price": lamports,
                    "seller": seller
                }

        except:

            pass

        return None

    def list_nft(self, seller: str, mint: str, price: int) -> str | None:
        
        OPTS = TxOpts(skip_preflight=True, skip_confirmation=True)

        transaction = Transaction()

        token_account = get_associated_token_address(owner=PublicKey(seller), mint=PublicKey(mint))

        METADATA = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(mint))
            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )

        SELLER_TRADE_STATE = self._trade_state(
            account=seller,
            token_account=str(token_account),
            mint_address=mint,
            price=price
        )

        FREE_TRADE_STATE = PublicKey.find_program_address(
            seeds=[
                "auction_house".encode("utf-8"),
                bytes(PublicKey(seller)),
                bytes(PublicKey(CC_KEY)),
                bytes(PublicKey(token_account)),
                bytes(PublicKey(WRAPPED_SOL)),
                bytes(PublicKey(mint)),
                (0).to_bytes(8, "little"),
                (1).to_bytes(8, "little")

            ],
            program_id=PublicKey(AUCTION_PROGRAM)
        )

        PROGRAM_AS_SIGNER = PublicKey.find_program_address(
            seeds=[
                "auction_house".encode("utf-8"),
                "signer".encode("utf-8"),

            ],
            program_id=PublicKey(AUCTION_PROGRAM)
        )

        keys = [
            AccountMeta(pubkey=PublicKey(self.payer.public_key),is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(token_account),is_signer=False, is_writable=True),
            AccountMeta(pubkey=METADATA[0],is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(CC_OWNER),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(CC_KEY),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(CC_FEE_ACCOUNT),is_signer=False, is_writable=True),
            AccountMeta(pubkey=SELLER_TRADE_STATE[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=FREE_TRADE_STATE[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PROGRAM_AS_SIGNER[0], is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM),is_signer=False, is_writable=False)
        ]

        trade_state_bump = [SELLER_TRADE_STATE[1]]
        free_trade_state_bump = [FREE_TRADE_STATE[1]]
        program_as_signer_bump = [PROGRAM_AS_SIGNER[1]]
        price_data = list(price.to_bytes(8, "little"))
        main_data = list(bytes.fromhex("33e685a4017f83ad"))
        padding_data = list(bytes.fromhex("0100000000000000"))
        
        data = main_data + trade_state_bump + free_trade_state_bump + program_as_signer_bump + price_data + padding_data

        encoded_data = b58encode(bytes(data))
        data = b58decode(encoded_data)

        transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(AUCTION_PROGRAM)
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

    def buy_nft(self, seller: str, mint: str, price: int, creators: list) -> str | None:

        OPTS = TxOpts(skip_preflight=True, skip_confirmation=False, preflight_commitment=Commitment("confirmed"))

        transaction = Transaction()

        token_account = get_associated_token_address(owner=PublicKey(seller), mint=PublicKey(mint))

        METADATA = PublicKey.find_program_address(
            seeds=[
                "metadata".encode("utf-8"),
                bytes(PublicKey(METADATA_PROGRAM_ID)),
                bytes(PublicKey(mint))

            ],
            program_id=PublicKey(METADATA_PROGRAM_ID)
        )

        ESCROW_PAYMENT = PublicKey.find_program_address(
            seeds=[
                "auction_house".encode("utf-8"),
                bytes(PublicKey(CC_KEY)),
                bytes(PublicKey(self.payer.public_key))

            ],
            program_id=PublicKey(AUCTION_PROGRAM)
        )

        BUYER_TRADE_STATE = self._trade_state(
            account=str(self.payer.public_key),
            token_account=str(token_account),
            mint_address=mint,
            price=price
        )

        keys = [
            AccountMeta(pubkey=PublicKey(self.payer.public_key),is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(self.payer.public_key),is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(WRAPPED_SOL),is_signer=False, is_writable=False),
            AccountMeta(pubkey=token_account,is_signer=False, is_writable=True),
            AccountMeta(pubkey=METADATA[0],is_signer=False, is_writable=False),
            AccountMeta(pubkey=ESCROW_PAYMENT[0],is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(CC_OWNER),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(CC_KEY),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(CC_FEE_ACCOUNT),is_signer=False, is_writable=True),
            AccountMeta(pubkey=BUYER_TRADE_STATE[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM),is_signer=False, is_writable=False)
        ]

        trade_state_bump = [BUYER_TRADE_STATE[1]]
        escrow_payment_bump = [ESCROW_PAYMENT[1]]
        price_data = list(price.to_bytes(8, "little"))
        main_data = list(bytes.fromhex("66063d1201daebea"))
        padding_data = list(bytes.fromhex("0100000000000000"))
        
        data = main_data + trade_state_bump + escrow_payment_bump + price_data + padding_data

        encoded_data = b58encode(bytes(data))
        data = b58decode(encoded_data)

        transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(AUCTION_PROGRAM)
            )
        )

        BUYER_RECEIPT = self._receipt_token(account=str(self.payer.public_key), mint_address=mint)

        SELLER_TRADE_STATE = self._trade_state(
            account=seller,
            token_account=str(token_account),
            mint_address=mint,
            price=price
        )

        FREE_TRADE_STATE = PublicKey.find_program_address(
            seeds=[
                "auction_house".encode("utf-8"),
                bytes(PublicKey(seller)),
                bytes(PublicKey(CC_KEY)),
                bytes(PublicKey(token_account)),
                bytes(PublicKey(WRAPPED_SOL)),
                bytes(PublicKey(mint)),
                (0).to_bytes(8, "little"),
                (1).to_bytes(8, "little")
            ],
            program_id=PublicKey(AUCTION_PROGRAM)
        )

        PROGRAM_AS_SIGNER = PublicKey.find_program_address(
            seeds=[
                "auction_house".encode("utf-8"),
                "signer".encode("utf-8")
            ],
            program_id=PublicKey(AUCTION_PROGRAM)
        )

        keys = [
            AccountMeta(pubkey=PublicKey(self.payer.public_key),is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(seller),is_writable=True, is_signer=False),
            AccountMeta(pubkey=token_account,is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(mint),is_writable=False, is_signer=False),
            AccountMeta(pubkey=METADATA[0],is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(WRAPPED_SOL),is_signer=False, is_writable=False),
            AccountMeta(pubkey=ESCROW_PAYMENT[0],is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(seller),is_signer=False, is_writable=True),
            AccountMeta(pubkey=BUYER_RECEIPT[0],is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(CC_OWNER),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(CC_KEY),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(CC_FEE_ACCOUNT),is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(CC_TREASURY),is_signer=False, is_writable=True),
            AccountMeta(pubkey=BUYER_TRADE_STATE[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=SELLER_TRADE_STATE[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=FREE_TRADE_STATE[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(ASSOCIATED_TOKEN_ID),is_signer=False, is_writable=False),
            AccountMeta(pubkey=PROGRAM_AS_SIGNER[0], is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM),is_signer=False, is_writable=False),
        ]

        for creator in creators:

            keys.append(AccountMeta(pubkey=PublicKey(creator),is_signer=False, is_writable=True))

        free_trade_state_bump = [FREE_TRADE_STATE[1]]
        program_as_signer_bump = [PROGRAM_AS_SIGNER[1]]
        main_data = list(bytes.fromhex("254ad99d4f312306"))
        
        data = main_data + escrow_payment_bump + free_trade_state_bump + program_as_signer_bump + price_data + padding_data

        encoded_data = b58encode(bytes(data))
        data = b58decode(encoded_data)

        transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(AUCTION_PROGRAM)
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
    
    CoralCube()