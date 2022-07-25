
import asyncio
from threading import Thread
from utils.constants import SolanaEndpoints, SolanaPrograms

from utils.solana import get_program_account_idl    



print(asyncio.run(get_program_account_idl("CandyMachineData", "4mnZ9MmH5Nr4GconnbW9hThodL2cAumXhMBBycAT3jt7", "HEiMicL2q6G6SQqpHek4xyMXs1jzPCDC71ZwxZLXx43i", "http://142.132.134.62:8899/")))