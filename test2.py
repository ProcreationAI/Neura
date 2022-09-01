from modules import MagicEden, ExchangeArt
from utils.solana import get_nft_metadata


a = MagicEden(
    rpc="https://snipe.acidnode.io/",
    privkey="3chJPsP3iLRAg2FiRrd5D1N4DfKKhkVw2DWpWP7rf9L7ccFNE5kp39aX86D7BQRZfXuxyXdgyAAdBqW5mkQVNx87",
)

mint = "BU7o9jWY3UJTRWaX1zdA8qoGrNYtpEhwhihGD27nSKEV"

meta = get_nft_metadata(mint, "https://snipe.acidnode.io/")


b = a.buy_nft(
    seller="MW8v1nQAmt3dFbSJ58Q1miFXiemHJFSYTj3E7Xm6fDN",
    price=int(0.04*(10**9)),
    mint=mint,
    escrow="5baiMgjfhWREPrX7N5aHoLMUqyAU6v7Jhxru11kSVqWX",
    creators=meta["data"]["creators"]
)

print(b)