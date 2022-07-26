from pathlib import Path
import sys

class SolanaEndpoints():
    
    MAINNET_RPC = "https://api.mainnet-beta.solana.com"
 
    
class Bot():
    
    VERSION = "0.19.4.0"
    USER_OS = sys.platform

class Discord():
    
    SUCCESS_WH = "https://discord.com/api/webhooks/997906580395786280/ZHbcYl0pjjf7yOpq0ExwOdsksrGj5LZQZ4mQckQ8hgqD1J3SdcViEz833TxOL2dxufgt"
    EMBED_COLOR = 0x6436CB
    EMBED_FOOTER_IMG = "https://cdn.discordapp.com/attachments/921022038074871879/981234960121856110/logo2.png"
    EMBED_FOOTER_TXT = "Neura | NFT bot & Alpha group"
    
class Keys():
    
    TLS_KEY = "oLZxFnte8n5UL6ERJqBjH7tJk37jVh503RP5IIt0"
    CF_API_KEY = "9c72148a-4e93-46b9-b5d0-d125e6c12f92"
    OS_API_KEY = "8216f4bf-659c-4b22-be8b-690285f86762"
    

class Paths():
    
    BIFROST_PATH  = str(Path("bin/bifrost.dll").resolve())
    TLS_PATH = str(Path("bin/TLS").resolve()) if sys.platform == "darwin" else str(Path("bin/TLS.exe").resolve())

class SolanaPrograms():
    
    CMV2_PROGRAM = "cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ"
    ME_PROGRAM = "CMZYPASGWeTz7RNGHaRJfCq2XQ5pYK6nDvVQxzkH51zb"
    LMN_PROGRAM = "ArAA6CZC123yMJLUe4uisBEgvfuw2WEvex9iFmFCYiXv"
    ML_PROGRAM = "minwAEdewYNqagUwzrVBUGWuo277eeSMwEwj76agxYd"
    BF_PROGRAM = "BFCMkgg9eFSv54HKJZFD5RMG8kNR5eMAEWnAtfRTPCjU"
    