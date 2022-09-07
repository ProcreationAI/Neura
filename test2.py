import json
from base58 import b58decode, b58encode
from modules import MagicEden, ExchangeArt
from modules.coral_cube import CoralCube
from modules.famous_fox import FamousFox
from modules.wallet_manager import SolWalletManager
from utils.solana import get_nft_metadata
from solana.publickey import PublicKey
import requests

a = CoralCube(
    rpc="https://snipe.acidnode.io/",
    privkey="3chJPsP3iLRAg2FiRrd5D1N4DfKKhkVw2DWpWP7rf9L7ccFNE5kp39aX86D7BQRZfXuxyXdgyAAdBqW5mkQVNx87",
)

b = a.check_tx_is_listing("2g9922N12EuEQRGPJ5xZ9APYAXpewiN32GMBPcXTxkZUAycxz2T1FZvZoRQ3p1s6HMGQJbz1YX6e4bEFBmPL8WNj")


print(b)
