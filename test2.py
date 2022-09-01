import json
from base58 import b58decode
from modules import MagicEden, ExchangeArt
from modules.famous_fox import FamousFox
from modules.wallet_manager import SolWalletManager
from utils.solana import get_nft_metadata
from solana.publickey import PublicKey

a = SolWalletManager(
    rpc="https://snipe.acidnode.io/",
    privkey="3chJPsP3iLRAg2FiRrd5D1N4DfKKhkVw2DWpWP7rf9L7ccFNE5kp39aX86D7BQRZfXuxyXdgyAAdBqW5mkQVNx87",
)

# bFh29pSqpqq6GiABU2mjf78NF2JiTDERVanVPvHFtzm
#a = get_nft_metadata("6fF22VaQLVLN5h3ASfCARrzKVQM7vgJLZekhrTCBJFsE", "https://snipe.acidnode.io/")


b = a.full_burn_nft("6fF22VaQLVLN5h3ASfCARrzKVQM7vgJLZekhrTCBJFsE")

print(b)