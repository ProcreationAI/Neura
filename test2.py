import json
import requests
from solana.keypair import Keypair
import requests
from urllib.parse import quote, urlencode
import re

from modules import BifrostLaunchpad, BifrostMint


a = BifrostMint(
    
)

import requests
url = "https://bifrost.blocksmithlabs.io/mint/froots"

bl = BifrostLaunchpad(
    mint_site=url,
    discord_auth="NDE5MDk3NjE3NDY1ODY4Mjg5.GlxA8N.j2y-0gFtvpbYXPsY5Yq7iFMy4pOA98PxgozYII"
)

bl.session.verify = "./charles-ssl-proxying-certificate.pem"


res = bl.get_mint_site()

print(res)

res = bl.generate_auth_session()

print(res)

res = bl.generate_dc_signin()

print(res)

res = bl.authorize_discord(signin_url=res)

print(res)

res = bl.discord_auth_callback(res)

print(res)

txs = bl.get_transactions(cmid="4mnZ9MmH5Nr4GconnbW9hThodL2cAumXhMBBycAT3jt7",
                          payer="mcJVJGZX3HXETvS2w9zW5jFLeawcLeYzgU1zmF1gCXs",
                          token_bonding="Abi8x2TudSz4H6zT7kow7gvC9dt6oAQwVyCuLoYtpjJW",
                          max_price=2.427042743869653)

print(json.dumps(txs, indent=3))