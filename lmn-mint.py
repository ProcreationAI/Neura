

import asyncio
from modules import LaunchMyNftLaunchpad
from utils.constants import SolanaPrograms
from utils.solana import get_program_account_idl


meta = asyncio.run(get_program_account_idl("CandyMachine", "HGiDkxk7WPns4ZwVATGGvMNQttz3pjix1JMLzZ8hwiJz", SolanaPrograms.LMN_PROGRAM, "http://142.132.134.62:8899/"))

lmn = LaunchMyNftLaunchpad(
    privkey="3chJPsP3iLRAg2FiRrd5D1N4DfKKhkVw2DWpWP7rf9L7ccFNE5kp39aX86D7BQRZfXuxyXdgyAAdBqW5mkQVNx87",
    rpc="http://142.132.134.62:8899/",
    cmid="HGiDkxk7WPns4ZwVATGGvMNQttz3pjix1JMLzZ8hwiJz",
    candy_machine_meta=meta
)

lmn.create_transaction()

bh = lmn._get_blockhash()

lmn.transaction.recent_blockhash = bh

tx = lmn.send_transaction()


print(tx)
