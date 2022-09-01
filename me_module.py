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


class MagicEden():
    
    
    def __init__(self, rpc: str, privkey: str):
        
        self.client = Client(rpc)

        self.payer = Keypair.from_secret_key(b58decode(privkey))

    def _get_blockhash(self):

        res = self.client.get_recent_blockhash(Commitment('finalized'))

        return Blockhash(res['result']['value']['blockhash'])

    def buy_nft(self, seller: str, price: int, mint: str, escrow: str, creators: list) -> str | None:
        
        OPTS = TxOpts(skip_preflight=True, skip_confirmation=False, preflight_commitment=Commitment("confirmed"))

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

            transaction.recent_blockhash = self._get_blockhash()
            transaction.sign(*signers)

            tx = transaction.serialize()

            tx_hash = self.client.send_raw_transaction(tx, OPTS)["result"]
            
            return tx_hash

        except:
                        
            return None


if __name__ == "__main__":
    
    MagicEden()