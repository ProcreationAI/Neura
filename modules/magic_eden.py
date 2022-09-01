import json
import requests
from solana.message import Message
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction, TransactionInstruction, AccountMeta
from spl.token.instructions import get_associated_token_address
from base58 import b58decode, b58encode
from solana.rpc.commitment import Commitment
from solana.blockhash import Blockhash
from rich.console import Console
from solana.rpc.core import UnconfirmedTxError
from urllib.parse import quote

from utils.bypass import create_tls_payload
from utils.solana import get_blockhash, get_lamports_from_listing_data, sol_to_lamports, lamports_to_sol

TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
TOKEN_METADATA_ID = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'
SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
SYSTEM_SLOT_HASHES = "SysvarS1otHashes111111111111111111111111111"
COMPUTE_BUDGET = "ComputeBudget111111111111111111111111111111"
ASSOCIATED_TOKEN_ID = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"

ME_PROGRAM = "M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K"
SELLER_REFERAL = "autMW8SgBkVYeBgqYiTuJZnkvDZMVU2MHJh9Jh7CSQ2"
AUCTION_HOUSE = "E8cU1WiRWjanGxmn96ewBgk9vPTcL6AEZ1t6F6fkgUWe"
AUCTION_FEE = "rFqFJ9g7TGBD8Ed7TPDnvGKZ5pWLPDyxLcvcH2eRCtt"
PROGRAM_SIGNER = "1BWutmTvYPwDtmw9abTkS4Ssr8no61spGAvW1X6NDix"
HAUS_PROGRAM = "hausS13jsjafwWwGqZTUQRmWyvyxn9EQpqMwV1PBBmk"

console = Console(highlight=False, log_path=False)


class MagicEden():
    
    
    def __init__(self, rpc: str, privkey: str):
        
        self.rpc = rpc
        self.client = Client(rpc)

        self.payer = Keypair.from_secret_key(b58decode(privkey))

    @staticmethod
    def get_nft_data(mint: str) -> dict | None:

        try:

            headers = {
                'authority': 'api-mainnet.magiceden.io',
                'accept': 'application/json, text/plain, */*',
                'origin': 'https://magiceden.io',
                'referer': 'https://magiceden.io/',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            }

            payload = create_tls_payload(
                url=f"https://api-mainnet.magiceden.io/rpc/getNFTByMintAddress/{mint}?useRarity=true",
                method="GET",
                headers=headers
            )

            res = requests.post("http://127.0.0.1:3000",
                                json=payload, timeout=3).json()

            res = json.loads(res["body"])

            return res["results"]

        except:

            return None


    @staticmethod
    def get_collection_attributes(symbol: str) -> dict | None:

        try:

            headers = {
                'authority': 'api-mainnet.magiceden.io',
                'accept': 'application/json, text/plain, */*',
                'origin': 'https://magiceden.io',
                'referer': 'https://magiceden.io/',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            }

            payload = create_tls_payload(
                url=f"https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/{symbol}?edge_cache=true",
                method="GET",
                headers=headers
            )

            res = requests.post("http://127.0.0.1:3000",json=payload, timeout=3).json()

            res = json.loads(res["body"])

            return res["results"]["availableAttributes"]

        except:

            return None

    

    @staticmethod
    def get_listed_nfts(symbol: str, min_sol: float = 0, max_sol: float = 999999999, limit: int = 20, recenlty_listed: bool = False, attributes: list = None) -> list | None:

        results = []
        
        skip = 1 if limit < 20 else limit//20
            
        try:
            
            for i in range(skip):
                
                headers = {
                    'authority': 'api-mainnet.magiceden.io',
                    'accept': 'application/json, text/plain, */*',
                    'origin': 'https://magiceden.io',
                    'referer': 'https://magiceden.io/',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
                }

                query = {"$match":{"$or":[{"collectionSymbol":symbol},{"onChainCollectionAddress":symbol}],"takerAmount":{"$gte":sol_to_lamports(min_sol),"$lte":sol_to_lamports(max_sol)}},"$sort":{"takerAmount":1},"$skip":i*20,"$limit":limit,"status":[]}
                
                query["$sort"] = {"createdAt": -1} if recenlty_listed else {"takerAmount": 1}

                if attributes:
                    
                    query['$match']["$and"] = [{"$or":[{"attributes":{"$elemMatch":{"trait_type":attribute["trait_type"],"value":attribute["value"]}}}]} for attribute in attributes]
                    
                    
                query = quote(json.dumps(query))

                payload = create_tls_payload(
                    url=f"https://api-mainnet.magiceden.io/rpc/getListedNFTsByQueryLite?q={query}",
                    method="GET",
                    headers=headers
                )

                res = requests.post("http://127.0.0.1:3000",json=payload, timeout=5).json()

                results += json.loads(res["body"])["results"]
            
            return results
        
        except:
            
            return None

    @staticmethod
    def get_wallet_listed(wallet: str) -> list | None:
            
        try:

            headers = {
                'authority': 'api-mainnet.magiceden.io',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'es-ES,es;q=0.9',
                'origin': 'https://magiceden.io',
                'referer': 'https://magiceden.io/',
                'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            }

            payload = create_tls_payload(
                url=f"https://api-mainnet.magiceden.io/search_escrows?initializerKey={wallet}",
                method="GET",
                headers=headers
            )

            res = requests.post("http://127.0.0.1:3000", json=payload, timeout=20).json()

            return json.loads(res["body"])["results"]

        except:
            

            return None

    @staticmethod
    def get_wallet_nfts(wallet: str) -> list | None:

        try:  

            headers = {
                'authority': 'api-mainnet.magiceden.io',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'es-ES,es;q=0.9',
                'origin': 'https://magiceden.io',
                'referer': 'https://magiceden.io/',
                'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            }


            payload = create_tls_payload(
                url=f"https://api-mainnet.magiceden.io/rpc/getNFTsByOwner/{wallet}",
                method="GET",
                headers=headers
            )

            res = requests.post("http://127.0.0.1:3000", json=payload, timeout=20)

            return json.loads(res.json()["body"])["results"]

        except:
            
            return None  


    def check_tx_is_listing(self, tx: str) -> dict | None:

        try:
                        
            tx = self.client.get_transaction(tx_sig=tx, commitment=Commitment("confirmed"))["result"]
            
            logs = "".join(tx["meta"]["logMessages"])
            accounts = tx["transaction"]["message"]["accountKeys"]
            
            if not tx["meta"]["err"] and "Instruction: Sell" in logs and tx["meta"]["postTokenBalances"] and ME_PROGRAM in accounts:
                                
                instr_data = tx["transaction"]["message"]["instructions"][0]["data"]
                instr_data = b58decode(instr_data).hex()
                
                mint = tx["meta"]["postTokenBalances"][0]["mint"]
                seller = accounts[0]
                escrow = accounts[2]
                
                lamports = get_lamports_from_listing_data(data=instr_data, left_offset=20, right_offset=32)
                                
                return {
                    "mint": mint,
                    "price": lamports,
                    "seller": seller,
                    "escrow": escrow
                }
                
        except:
                                                
            pass
        
        return None


    def list_nft(self, mint: str, price: int) -> str | None:
        
        OPTS = TxOpts(skip_preflight=True, skip_confirmation=True)

        price = lamports_to_sol(price)
        
        token_ata = get_associated_token_address(
            owner=self.payer.public_key,
            mint=PublicKey(mint)
        )
        
        url = f"https://api-mainnet.magiceden.io/v2/instructions/sell?seller={self.payer.public_key}&auctionHouseAddress={AUCTION_HOUSE}&tokenMint={mint}&tokenAccount={token_ata}&price={price}&expiry=-1"

        headers = {
            'authority': 'api-mainnet.magiceden.io',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'es-ES,es;q=0.9',
            'origin': 'https://magiceden.io',
            'referer': 'https://magiceden.io/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
        }
        
        payload = create_tls_payload(
            url=url,
            method="GET",
            headers=headers
        )

        i = 5

        while i:

            try:

                res = requests.post('http://127.0.0.1:3000', json=payload, timeout=3).json()

                res = json.loads(res["body"])
                
                data = res["txSigned"]["data"]

                tx = Transaction.deserialize(bytes(data))

                #tx.sign_partial(*[self.payer])
                tx.add_signer(self.payer)

                serialized = tx.serialize()

                tx_hash = self.client.send_raw_transaction(serialized, opts=OPTS)["result"]

                return tx_hash

            except:
                
                i -= 1

        return None

    def delist_nft(self, mint: str, price: int) -> str | None:

        OPTS = TxOpts(skip_preflight=True, skip_confirmation=True)

        price = lamports_to_sol(price)
        
        token_ata = get_associated_token_address(
            owner=self.payer.public_key,
            mint=PublicKey(mint)
        )

        url = f"https://api-mainnet.magiceden.io/v2/instructions/sell_cancel?seller={self.payer.public_key}&auctionHouseAddress={AUCTION_HOUSE}&tokenMint={mint}&tokenAccount={token_ata}&price={price}&sellerReferral={SELLER_REFERAL}&expiry=-1"

        headers = {
            'authority': 'api-mainnet.magiceden.io',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'es-ES,es;q=0.9',
            'origin': 'https://magiceden.io',
            'referer': 'https://magiceden.io/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
        }

        payload = create_tls_payload(
            url=url,
            method="GET",
            headers=headers
        )
        
        i = 5

        while i:

            try:

                res = requests.post('http://127.0.0.1:3000', json=payload, timeout=2).json()

                res = json.loads(res["body"])

                data = res["txSigned"]["data"]

                tx = Transaction.deserialize(bytes(data))

                #tx.sign_partial(*[self.payer])
                tx.add_signer(self.payer)

                serialized = tx.serialize()

                tx_hash = self.client.send_raw_transaction(serialized, opts=OPTS)["result"]

                return tx_hash

            except:
                                        
                i -= 1

        return None
    
    
    def buy_nft_api(self, seller: str, price: int, mint: str) -> str | None:
        
        OPTS = TxOpts(skip_preflight=True, skip_confirmation=False, preflight_commitment=Commitment("confirmed"))

        price = lamports_to_sol(price)

        token_ata = get_associated_token_address(
            owner=PublicKey(seller),
            mint=PublicKey(mint)
        )
                 
        url = f"https://api-mainnet.magiceden.io/v2/instructions/buy_now?buyer={self.payer.public_key}&seller={seller}&auctionHouseAddress={AUCTION_HOUSE}&tokenMint={mint}&tokenATA={token_ata}&price={price}&sellerReferral={SELLER_REFERAL}&sellerExpiry=-1"

        headers = {
            'authority': 'api-mainnet.magiceden.io',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'es-ES,es;q=0.9',
            'origin': 'https://magiceden.io',
            'referer': 'https://magiceden.io/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
        }

        payload = create_tls_payload(
            url=url,
            method="GET",
            headers=headers
        )
        
        i = 5

        while i:

            try:

                res = requests.post('http://127.0.0.1:3000', json=payload, timeout=2).json()

                res = json.loads(res["body"])

                data = res["txSigned"]["data"]

                tx = Transaction.deserialize(bytes(data))

                #tx.sign_partial(*[self.payer])
                tx.add_signer(self.payer)
                
                serialized = tx.serialize()

                tx_hash = self.client.send_raw_transaction(serialized, opts=OPTS)["result"]
                
                return tx_hash

            except UnconfirmedTxError:
                
                return None
            
            except:
                                                        
                i -= 1
                
        return None    
    
    def buy_nft(self, seller: str, price: int, mint: str, escrow: str, creators: list) -> str | None:
        
        OPTS = TxOpts(skip_preflight=True, skip_confirmation=False, preflight_commitment=Commitment("processed"))

        transaction = Transaction()
        
        BUYER_ESCROW = PublicKey.find_program_address(
            seeds=[
                'm2'.encode('utf-8'),
                bytes(PublicKey(AUCTION_HOUSE)),
                bytes(PublicKey(self.payer.public_key)),
            ],
            program_id=PublicKey(ME_PROGRAM)
        )

        keys = [
            AccountMeta(pubkey=self.payer.public_key, is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(BUYER_ESCROW[0]), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(SELLER_REFERAL), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(AUCTION_HOUSE), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer=False, is_writable=False)
        ]
        
        buyer_escrow_bump = [BUYER_ESCROW[1]]
        price_data = list(price.to_bytes(8, "little"))
        main_data = list(bytes.fromhex("f223c68952e1f2b6"))
        
        data = main_data + buyer_escrow_bump + price_data

        encoded_data = b58encode(bytes(data))
        data = b58decode(encoded_data)
        
        # 1 - Deposit
        transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(ME_PROGRAM)
            )
        )

        METADATA = PublicKey.find_program_address(
            seeds=[
                'metadata'.encode('utf-8'),
                bytes(PublicKey(TOKEN_METADATA_ID)),
                bytes(PublicKey(mint))
            ],
            program_id=PublicKey(TOKEN_METADATA_ID)
        )

        BUY_ORDER_ACCOUNT = PublicKey.find_program_address(
            seeds=[
                'm2'.encode('utf-8'),
                bytes(self.payer.public_key),
                bytes(PublicKey(AUCTION_HOUSE)),
                bytes(PublicKey(mint))
            ],
            program_id=PublicKey(ME_PROGRAM)
        )

        keys = [
            AccountMeta(pubkey=self.payer.public_key, is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(mint), is_writable=False, is_signer=False),
            AccountMeta(pubkey=METADATA[0], is_writable=False, is_signer=False),
            AccountMeta(pubkey=BUYER_ESCROW[0], is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(SELLER_REFERAL), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(AUCTION_HOUSE), is_signer=False, is_writable=False),
            AccountMeta(pubkey=BUY_ORDER_ACCOUNT[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(SELLER_REFERAL), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID), is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM), is_writable=False, is_signer=False),
        ]

        buy_order_bump = [BUY_ORDER_ACCOUNT[1]]
        main_data = list(bytes.fromhex("66063d1201daebea"))
        padding_data = list(bytes.fromhex("01000000000000000000000000000000"))
        
        data = main_data + buy_order_bump + buyer_escrow_bump + price_data + padding_data

        encoded_data = b58encode(bytes(data))
        data = b58decode(encoded_data)
        
        # 2 - Buy
        transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(ME_PROGRAM)
            )
        )
    
    
        seller_ata = get_associated_token_address(
            owner=PublicKey(seller),
            mint=PublicKey(mint)
        )

        buyer_ata = get_associated_token_address(
            owner=PublicKey(self.payer.public_key),
            mint=PublicKey(mint)
        )
        

        keys = [
            AccountMeta(pubkey=self.payer.public_key, is_signer=True, is_writable=True),
            AccountMeta(pubkey=PublicKey(seller), is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=seller_ata, is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(mint), is_writable=False, is_signer=False),
            AccountMeta(pubkey=METADATA[0], is_writable=False, is_signer=False),
            AccountMeta(pubkey=BUYER_ESCROW[0], is_writable=True, is_signer=False),
            AccountMeta(pubkey=buyer_ata, is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(SELLER_REFERAL), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(AUCTION_HOUSE), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(AUCTION_FEE), is_signer=False, is_writable=True),
            AccountMeta(pubkey=BUY_ORDER_ACCOUNT[0], is_signer=False, is_writable=True),
            AccountMeta(pubkey=PublicKey(SELLER_REFERAL), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(escrow), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(SELLER_REFERAL), is_writable=True, is_signer=False),
            AccountMeta(pubkey=PublicKey(TOKEN_PROGRAM_ID), is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_PROGRAM_ID), is_signer=False, is_writable=False),
            AccountMeta(pubkey=PublicKey(ASSOCIATED_TOKEN_ID), is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(PROGRAM_SIGNER), is_writable=False, is_signer=False),
            AccountMeta(pubkey=PublicKey(SYSTEM_RENT_PROGRAM), is_writable=False, is_signer=False),
        ]
        
        for creator in creators:

            keys.append(AccountMeta(pubkey=PublicKey(creator),is_signer=False, is_writable=True))
            
        program_signer_bump = [250]
        main_data = list(bytes.fromhex("254ad99d4f312306"))
        expiry_data = list(bytes.fromhex("ffffffffffffffff"))
        
        data = main_data + buyer_escrow_bump + program_signer_bump + price_data + padding_data + expiry_data

        encoded_data = b58encode(bytes(data))
        data = b58decode(encoded_data)

        # 3 - Execute sale
        transaction.add(
            TransactionInstruction(
                keys=keys,
                data=data,
                program_id=PublicKey(ME_PROGRAM)
            )
        )
        
        signers = [
            self.payer,
        ]
        
        try:

            transaction.recent_blockhash = get_blockhash(self.rpc)
            transaction.sign(*signers)

            tx = transaction.serialize()

            tx_hash = self.client.send_raw_transaction(tx, OPTS)["result"]
            
            return tx_hash

        except:
                        
            return None


if __name__ == "__main__":
    
    MagicEden()