import json
from base58 import b58decode
from modules import MagicEden, ExchangeArt
from modules.famous_fox import FamousFox
from modules.wallet_manager import SolWalletManager
from utils.solana import get_nft_metadata
from solana.publickey import PublicKey


a = MagicEden(
    rpc="https://snipe.acidnode.io/",
    privkey="3chJPsP3iLRAg2FiRrd5D1N4DfKKhkVw2DWpWP7rf9L7ccFNE5kp39aX86D7BQRZfXuxyXdgyAAdBqW5mkQVNx87",
)

# bFh29pSqpqq6GiABU2mjf78NF2JiTDERVanVPvHFtzm
c = get_nft_metadata("HdQnH1LbrBCyu3Wu6i367ejiCZqMoma1HYXsHicTLKM8", "https://snipe.acidnode.io/")

print(c)



