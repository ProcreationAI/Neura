import re
import json
import os
from rich.console import Console
from threading import Thread
from rich.prompt import Prompt
from urllib.parse import urlsplit
from datetime import datetime
from rich.table import Table
import base58
import csv
import time
import subprocess
import asyncio
from dateutil import tz
import sys
import requests
from bs4 import BeautifulSoup
from base58 import b58decode, b58encode
from base64 import b64decode, b64encode
import borsh
from borsh import types as btypes

from solana.rpc.api import Client
from solana.rpc import types
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.blockhash import Blockhash
from solana.rpc.commitment import Commitment
from anchorpy import Program, Wallet, Provider
from web3 import Web3
from solana.rpc.async_api import AsyncClient

from modules import (
    CandyMachinev2,
    MagicEdenLaunchpad,
    MagicEden,
    EthContract,
    FamousFox,
    OpenSea,
    LaunchMyNftLaunchpad,
    CoralCube,
    NeuraDB,
    MonkeLabsLaunchpad,
    SolWalletManager
)

from lib import (
    AccountClient
)

from utils import *

def get_eth_wallets():

    w3conn = Web3(Web3.HTTPProvider(eth_rpc))

    wallets = []

    try:

        with open('eth-wallets.csv', 'r') as f:

            reader = csv.reader(f)

            next(reader)

            task_id = 1

            for wallet in reader:

                if not any(data == "" for data in wallet):

                    name, privkey, _, contract, function, amount, price, gas, cancel = wallet

                    name = name if len(name) <= 12 else name[:12]

                    address = get_pub_from_priv(privkey, blockchain="eth")

                    if address and w3conn.isAddress(contract):

                        try:

                            wallets.append(

                                {
                                    "name": name.upper(),
                                    "address": address,
                                    "privkey": privkey,
                                    "task-id": task_id,
                                    "contract": contract,
                                    "function": function,
                                    "amount": int(amount),
                                    "price": float(price),
                                    "gas": int(gas),
                                    "cancel": int(cancel),
                                    "tasks": 1
                                }
                            )

                        except ValueError:

                            return None
                    else:

                        return None

                task_id += 1

    except:

        return None

    return wallets


def get_sol_wallets():

    wallets = []

    try:

        with open('sol-wallets.csv', 'r') as f:

            reader = csv.reader(f)

            next(reader)

            for wallet in reader:

                if not any(data == "" for data in wallet):

                    name, privkey, tasks = wallet

                    name = name if len(name) <= 9 else name[:9]

                    address = get_pub_from_priv(privkey, blockchain="sol")

                    if address:

                        try:

                            tasks = int(tasks)

                            """ if mode in [1, 2, 9, 11]:
                                    
                                if tasks > max_tasks:

                                    tasks = max_tasks

                                elif tasks < min_tasks:
                                    
                                    tasks = min_tasks """
                                
                            wallets.append(

                                {
                                    "name": name.upper(),
                                    "address": address,
                                    "privkey": privkey,
                                    "tasks": int(tasks)
                                }

                            )

                        except ValueError:

                            pass
    except:

        pass

    return wallets


def get_eth_sniper_wallets():

    try:

        wallets = []

        with open('eth-wallets.csv', 'r') as f:

            reader = csv.reader(f)

            next(reader)

            for wallet in reader:

                name, privkey, tasks, _, _, _, _, gas, _ = wallet

                name = name if len(name) <= 12 else name[:12]

                address = get_pub_from_priv(privkey, blockchain="eth")

                if address:

                    try:

                        wallets.append({
                            "name": name.upper(),
                            "address": address,
                            "privkey": privkey,
                            "gas": int(gas),
                            "tasks": int(tasks)
                        })

                    except ValueError:

                        pass

        return wallets

    except:

        return None


def clear(newline: bool = True):

    if user_platform == "darwin":

        os.system("clear")

    elif user_platform == "win32":

        os.system('cls')

    if newline:

        print()

def mint(wallet: dict):

    name = wallet["name"]
    tasks = wallet["tasks"]
    privkey = wallet["privkey"]

    trs = []

    
    if mode in [1, 2, 9, 11]:

        show_drop_time = datetime.fromtimestamp(DROP_TIME).strftime("%H:%M:%S")
        
        console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Initialazing mint[/]\n".format(name, f"0/{tasks}", show_drop_time)), end="")

    elif mode == 4:

        gas = wallet["gas"]

        console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 0/1 ] [GAS ~ {:<6}][/] [yellow]Initialazing mint[/]\n".format(name, gas)), end="")

    if mode != 4:
            
        if (auto_timer and mode != 11) or user_time:

            console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Awaiting for drop time[/]\n".format(name, f"0/{tasks}", show_drop_time)), end="")

            wait_for_drop(exit_before=3)
        
        elif await_mints:
            
            console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Awaiting for mints[/]\n".format(name, f"0/{tasks}", show_drop_time)), end="")
            
            wait_for_mints()
            
        while True:

            recent_blockhash = get_blockhash()

            if recent_blockhash:
                
                console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Initialazing transactions[/]\n".format(name, f"0/{tasks}", show_drop_time)), end="")
                
                break
            
            else:

                console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [red]Unable to initialize txs (node)[/]\n".format(name, f"0/{tasks}", show_drop_time)), end="")
                
        if (auto_timer and mode != 11) or user_time:
            
            wait_for_drop()
            
    for i in range(tasks):
        
        if mode != 4:
            
            status = "[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/]".format(name, f"{i + 1}/{tasks}", show_drop_time)
        
        if mode == 1:

            createtxT = Thread(
                target=send_cmv2_tx,
                args=[privkey, sol_rpc, recent_blockhash, status],
                daemon=True
            )

        if mode == 2:

            createtxT = Thread(
                target=send_me_tx,
                args=[privkey, sol_rpc, recent_blockhash, status],
                daemon=True
            )

        if mode == 9:
            
            createtxT = Thread(
                target=send_lmn_tx,
                args=[privkey, sol_rpc, recent_blockhash, status],
                daemon=True
            )

        if mode == 11:
            
            createtxT = Thread(
                target=send_ml_tx,
                args=[privkey, sol_rpc, recent_blockhash, status],
                daemon=True
            )
            
        if mode == 4:

            createtxT = Thread(target=mint_contract, args=[wallet], daemon=True)

        createtxT.start()
        trs.append(createtxT)
    
    for tr in trs:
        
        tr.join()


def send_cmv2_tx(privkey: str, rpc: str, blockhash: Blockhash, status: str):

    commits = 0

    candy = CandyMachinev2(
        privkey=privkey,
        cmid=CM,
        rpc=rpc,
        candy_machine_meta=cm_metadata,
        collection_meta=collection_set_metadata
    )

    try:

        candy.create_transaction()

        candy.transaction.recent_blockhash = blockhash

    except:
        
        console.print(logger(f"{status} [red]Error while creating tx (node)[/]\n"), end="")

        return
    
    while commits < (transaction_retry + 1):
        
        simulated = True

        if advanced_mode:

            console.print(logger(f"{status} [yellow]Simulating transaction [{commits + 1}][/]\n"), end="")
  
            simulated = candy.simulate_transaction()
            
            if simulated:

                console.print(logger(f"{status} [yellow]Simulation successful [{commits + 1}][/]\n"), end="")

            else:
                
                console.print(logger(f"{status} [red]Simulation failed [{commits + 1}][/]\n"), end="")

        if simulated:
                
            console.print(logger(f"{status} [yellow]Sending transaction [{commits + 1}][/]\n"), end="")

            tx = candy.send_transaction()
        
            if tx:

                console.print(logger(f"{status} [green]Mint successful at tx [{commits + 1}] with hash: {tx}[/]\n"), end="")

                return

            elif tx is None:

                console.print(logger(f"{status} [red]Unable to confirm tx [{commits + 1}][/]\n"), end="")

            elif tx is False:
                
                console.print(logger(f"{status} [red]Error while sending tx [{commits + 1}][/]\n"), end="")
            
        commits += 1


def send_ml_tx(privkey: str, rpc: str, blockhash: Blockhash, status: str):

    commits = 0

    launchpad = MonkeLabsLaunchpad(
        privkey=privkey,
        rpc=rpc,
        accounts=CM
    )

    try:

        launchpad.create_transaction()

        launchpad.transaction.recent_blockhash = blockhash

    except:
        
        console.print(logger(f"{status} [red]Error while creating tx (node)[/]\n"), end="")

        return
    
    while commits < (transaction_retry + 1):
    
        console.print(logger(f"{status} [yellow]Sending transaction [{commits + 1}][/]\n"), end="")

        tx = launchpad.send_transaction()
    
        if tx:

            console.print(logger(f"{status} [green]Mint successful at tx [{commits + 1}] with hash: {tx}[/]\n"), end="")

            return

        elif tx is None:

            console.print(logger(f"{status} [red]Unable to confirm tx [{commits + 1}][/]\n"), end="")

        elif tx is False:
            
            console.print(logger(f"{status} [red]Error while sending tx [{commits + 1}][/]\n"), end="")
            
        commits += 1


def mint_contract(wallet: dict):

    eth_mint = EthContract(
        contract_adress=wallet["contract"],
        function=wallet["function"],
        amount=wallet["amount"],
        price=wallet["price"],
        gas=wallet["gas"],
        cancel=wallet["cancel"],
        task=wallet["task-id"],
        name=wallet["name"],
        privkey=wallet["privkey"],
        wallet_address=wallet["address"],
        rpc=eth_rpc

    )

    eth_mint.run_task()


def send_lmn_tx(privkey: str, rpc: str, blockhash: Blockhash, status: str):
    
    commits = 0

    launchpad = LaunchMyNftLaunchpad(
        privkey=privkey,
        rpc=rpc,
        cmid=CM,
        candy_machine_meta=cm_metadata
    )
    
    try:

        launchpad.create_transaction()
        
        launchpad.transaction.recent_blockhash = blockhash
        
    except:

        console.print(logger(f"{status} [red]Error while creating tx (node)[/]\n"), end="")
        
        return
    

    while commits < (transaction_retry + 1):
        
        console.print(logger(f"{status} [yellow]Sending transaction [{commits + 1}][/]\n"), end="")

        tx = launchpad.send_transaction()
    
        if tx:

            console.print(logger(f"{status} [green]Mint successful at tx [{commits + 1}] with hash: {tx}[/]\n"), end="")

            return

        elif tx is None:

            console.print(logger(f"{status} [red]Unable to confirm tx [{commits + 1}][/]\n"), end="")

        elif tx is False:
            
            console.print(logger(f"{status} [red]Error while sending tx [{commits + 1}][/]\n"), end="")
            
        commits += 1
        
        
def send_me_tx(privkey: str, rpc: str, blockhash: Blockhash, status: str):

    commits = 0

    launchpad = MagicEdenLaunchpad(
        privkey=privkey,
        cmid=CM,
        rpc=rpc,
        candy_machine_meta=cm_metadata
    )
    
    try:

        launchpad.find_transaction_accounts()
    
    except:
        
        console.print(logger(f"{status} [red]Error while creating tx (node)[/]\n"), end="")
        
        return
    

    while commits < (transaction_retry + 1):
        
        console.print(logger(f"{status} [yellow]Sending transaction [{commits + 1}][/]\n"), end="")
        
        try:
            
            res = launchpad.get_transaction_hash(blockhash)

        except:
            
            res = None
            
        if res is not None:

            if res["statusCode"] == 200:
                
                res = json.loads(res["body"])
                
                data = res["tx"]

                tx = launchpad.send_transaction(tx_data=data)

                if tx:

                    console.print(logger(f"{status} [green]Mint successful at tx [{commits + 1}] with hash: {tx}[/]\n"), end="")
                    
                    return

                elif tx is None:

                    console.print(logger(f"{status} [red]Unable to confirm tx [{commits + 1}][/]\n"), end="")
                    
                elif tx is False:

                    console.print(logger(f"{status} [red]Error while sending tx [{commits + 1}][/]\n"), end="")
            
            else:

                console.print(logger(f"{status} [red]Unable to sign tx [{commits + 1}][/]\n"), end="")
    
        else:

            console.print(logger(f"{status} [red]Error while signing tx [{commits + 1}][/]\n"), end="")

        commits += 1


def check_cmid(cmid: str):
    
    global CM
    
    try:
        
        client = Client(sol_rpc)
        
        res = client.get_account_info(pubkey=cmid)

        owner = res["result"]["value"]["owner"]
        data = res["result"]["value"]["data"][0]

        data = str(b64decode(data))

        not_honeypot = re.search("(?P<url>https?://[^\s]+)", data)

        if owner == SolanaPrograms.CMV2_PROGRAM and not_honeypot:
            
            CM = cmid
                                                            
            return SolanaPrograms.CMV2_PROGRAM
            
        elif owner == SolanaPrograms.LMN_PROGRAM:
            
            CM = cmid
                                        
            return SolanaPrograms.LMN_PROGRAM
        
        elif owner == SolanaPrograms.ML_PROGRAM:
            
            CM = cmid
                                        
            return SolanaPrograms.ML_PROGRAM
    except Exception as e:
        
        print(e)
        exit()
        return None

def get_lmn_candy_machine(url: str):
    
    
    try:
        res = requests.get(url, timeout=5).text

        soup = BeautifulSoup(res, "lxml")

        cm_info_script = soup.find("script", {"id": "__NEXT_DATA__"})
        
        if cm_info_script:
            
            return json.loads(cm_info_script.text)["props"]["pageProps"]["collection"]["newCandyMachineAccountId"]
                
    
    except:
        
        pass
    
    return None

def is_URL(url):

    try:
        
        requests.get(url, timeout=3)

        return True
    
    except:
        
        return None
    
def get_scripts(url: str):

    global IDS
    
    try:
        res = requests.get(url, timeout=5).text

        soup = BeautifulSoup(res, "lxml")
        scripts = soup.find_all("script", {"src": True})

        cm_info_script = soup.find("script", {"id": "__NEXT_DATA__"})
        
        if cm_info_script:
            
            try:
                
                data = str(cm_info_script.text)

                section = re.findall("candyMachineId(.*?)\,", data)[0]
                
                cmid = re.sub('[^a-zA-Z0-9]+', '', section)
                
                IDS.append(cmid)
                
            except:
                
                pass
            
        if scripts:

            return [script["src"] for script in scripts]
        
    except:
        
        pass

def get_cmids(url: str, script: str):

    global IDS

    split_url = urlsplit(url)
    url = f"{split_url.scheme}://{split_url.netloc}{script}"

    if is_URL(url):

        try:
            
            res = str(requests.get(url, timeout=2).content.decode())
            
        except:
            
            return None

        possible_ids = re.findall(
            'PublicKey\(\"(.*?)\"\)', res) + re.findall('[a-zA-z ]+[= ]+\"(.*?)\"', res)

        for id in possible_ids:

            if re.match("^[A-Za-z0-9]*$", id):

                try:

                    if id not in IDS and len(base58.b58decode(id)) == 32:

                        IDS.append(id)
                except:

                    pass

 
def get_cmv2_candy_machine(url: str):

    scripts = get_scripts(url)

    if scripts:

        trs = []

        if not IDS:
                
            for script in scripts:

                getidsT = Thread(target=get_cmids,
                                    args=[
                                        url, script],
                                    daemon=True)
                getidsT.start()
                trs.append(getidsT)

            for tr in trs:
                tr.join()

        if IDS:

            trs = []

            for id in IDS:

                checkidsT = Thread(target=check_cmid,
                                    args=[id],
                                    daemon=True)
                checkidsT.start()
                trs.append(checkidsT)

            for tr in trs:
                tr.join()

    return CM
            

def get_ml_candy_machine(url: str):

    try:
        
        res = requests.get(url, timeout=5).text

        soup = BeautifulSoup(res, "lxml")
        scripts = soup.find_all("script", {"src": True})

        if scripts:

            script = [script["src"] for script in scripts if "main" in script["src"]][0]

            split_url = urlsplit(url)
            script = f"{split_url.scheme}://{split_url.netloc}{script}"
            
            if is_URL(script):

                res = str(requests.get(script, timeout=2).content.decode())
                
                monkelabs_data = re.findall('FAST_REFRESH:!0,(.*?)}\)', res)
                
                if monkelabs_data:
                    
                    accs = {}
                    
                    for acc in monkelabs_data[0].split(","):
                        
                        if len(acc.split(":")) == 2:
                            
                            key, value = acc.split(":")
                            
                            accs[key] = re.sub('[\W_]+', '', value)
                    
                    if accs:
                        
                        config_key = accs["REACT_APP_CONFIG_KEY"]
                        
                        client = Client(sol_rpc)
                        
                        res = client.get_account_info(config_key)
                        
                        data = res["result"]["value"]["data"][0]
                        
                        schema = {
                            "z": btypes.string,
                            "a": btypes.string,
                            "b": btypes.u32,
                            "c": btypes.u32,
                            "d": btypes.u64,
                            "e": btypes.string,
                            "f": btypes.u16,
                            "g": btypes.fixed_array(btypes.u8, 32),
                            "h": btypes.fixed_array(btypes.u8, 32),
                            "i": btypes.u16,
                            "j": btypes.u64,
                            "k": btypes.fixed_array(btypes.u8, 32),
                            "l": btypes.u32,
                            "collectionKey": btypes.fixed_array(btypes.u8, 32),
                            "n": btypes.fixed_array(btypes.u8, 32),
                            "o": btypes.u16,
                            "p": btypes.u64,
                            "q": btypes.fixed_array(btypes.u8, 32)
                        }
                        
                        deserialized = borsh.deserialize(schema=schema, data=b64decode(data))
                        
                        accs["REACT_APP_COLLECTION_KEY"] = deserialized["collectionKey"]
                        
                        return accs
                    
    except:
        
        pass
    
    return None


def get_ml_items_redeemed(index_key: str):
    
    try:
        
        client = Client("https://api.mainnet-beta.solana.com")

        res = client.get_account_info(index_key)

        data = res["result"]["value"]["data"][0]

        data = list(bytes(b64decode(data)))

        return (data[1] << 8) + data[0]
    
    except:
        
        return None


def show_banner():

    console.print(rf"""[purple]
     _   __
    / | / /__  __  ___________ _
   /  |/ / _ \/ / / / ___/ __ `/
  / /|  /  __/ /_/ / /  / /_/ /
 /_/ |_/\___/\__,_/_/   \__,_/  [/][white]v.{Bot.VERSION}[/]""")

    print("\n")


def get_launchpad_collection(url: str):

    try:
        
        symbol = get_collection_symbol(url=url)
        
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
        
        url = f"https://api-mainnet.magiceden.io/launchpads/{symbol}"
        

        payload = create_tls_payload(
            url=url,
            method="GET",
            headers=headers
        )

        collection = requests.post('http://127.0.0.1:3000', json=payload, timeout=10).json()
        
        collection = json.loads(collection["body"])

        stage = collection["state"]["stages"][-1]

        _time = int(datetime.fromisoformat(stage["startTime"][:-1]).timestamp())
        _time = get_local_time(_time)
        
        if "fixedLimit" in stage["walletLimit"]:
        
            wallet_limit = stage["walletLimit"]["fixedLimit"]["limit"]
            
        else:
            
            wallet_limit = None

        price = stage["price"]
        
        return {
            "name": collection["name"],
            "price": price,
            "supply": collection["size"],
            "cmid": collection["mint"]["candyMachineId"],
            "walletLimit": wallet_limit,
            "date": _time,
        }
                
    except:
        
        return None


def get_wallet_balance(pubkey: str, blockchain: str):

    if blockchain == "sol":

        try:

            client = Client(sol_rpc)

            balance = client.get_balance(pubkey)

            return balance["result"]["value"]

        except:

            return 0

    elif blockchain == "eth":

        try:

            w3conn = Web3(Web3.HTTPProvider(eth_rpc))

            return w3conn.eth.get_balance(pubkey)

        except:

            return 0


def get_wallet_nfts(wallet: str):

    try:

        client = Client(SolanaEndpoints.MAINNET_RPC)
        
        res = client.get_token_accounts_by_owner(owner=wallet, opts=types.TokenAccountOpts(encoding="jsonParsed", program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")))

        if not res.get("error") and res.get("result"): 

            if res["result"].get("value"):

                nfts = res["result"]["value"]

                if "account" in str(nfts) and "mint" in str(nfts):

                    holded_nfts = []

                    for nft in nfts:

                        nft_data = nft["account"]["data"]["parsed"]["info"]

                        if int(nft_data["tokenAmount"]["amount"]) > 0:

                            holded_nfts.append(nft_data["mint"])

                    return holded_nfts

    except:
        
        return None



def get_nft_metadata(mint_key):

    client = Client(sol_rpc)

    try:
        metadata_account = get_metadata_account(mint_key)

        data = b64decode(client.get_account_info(
            metadata_account)['result']['value']['data'][0])

        metadata = unpack_metadata_account(data)

        return metadata

    except:  
        
        return None


def get_collection_pda_account(cmid: str):
    
    return str(PublicKey.find_program_address(
        seeds=[
            "collection".encode("utf-8"),
            bytes(PublicKey(cmid)),
        ],
        program_id=PublicKey(SolanaPrograms.CMV2_PROGRAM)
    )[0])

async def get_account_metadata(name: str, account: str, prog: str):

    try:

        program = None
        client = None
        
        program_id = PublicKey(prog)
            
        client = AsyncClient(sol_rpc)

        provider = Provider(client, Wallet(Keypair.generate()))
        
        idl = await Program.fetch_idl(
            program_id,
            provider
        )
        
        program = Program(
            idl,
            program_id,
            provider
        )

        candyMachine = await AccountClient.fetch_custom(program.account[name], PublicKey(account))

        await program.close()
        await client.close()

        return candyMachine

    except:
        
        if program:
            await program.close()
        if client:
            await client.close()
            
        return None
    
def get_pub_from_priv(privkey: str, blockchain: str):

    if blockchain == "sol":

        try:
            wallet = Keypair.from_secret_key(base58.b58decode(privkey))

            pubkey = str(wallet.public_key)

        except:

            return None

    if blockchain == "eth":

        w3conn = Web3(Web3.HTTPProvider(eth_rpc))

        try:

            pubkey = w3conn.eth.account.privateKeyToAccount(privkey).address

        except:

            return None

    return pubkey


def wallet_is_holder(pubkey: str, hashlist: list):

    user_nfts = get_wallet_nfts(wallet=pubkey)
    
    if user_nfts:
        
        for nft in user_nfts:

            if nft in hashlist:

                return nft

    return False

def get_blockhash():

    try:
            
        client = Client(sol_rpc)
        
        res = client.get_recent_blockhash(Commitment('finalized'))

        blockhash = Blockhash(res['result']['value']['blockhash'])

        return blockhash

    except:
        
        return None
    

def get_local_time(_time: int):

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    utc = datetime.fromtimestamp(_time).replace(tzinfo=from_zone)
    return int(utc.astimezone(to_zone).timestamp())


def create_table_launchpad(collection: dict):

    table = Table()

    table.add_column("NAME", justify="center", style="yellow")
    table.add_column("TIME (LOCAL)", justify="center", style="yellow")
    table.add_column("CANDY MACHINE ID",
                     justify="center", style="green")
    table.add_column("SUPPLY", justify="center", style="cyan")
    table.add_column("PRICE", justify="center", style="cyan")
    
    table.add_row(
        collection["name"], datetime.fromtimestamp(DROP_TIME).strftime("%H:%M:%S"), collection["cmid"], str(collection["supply"]), str(lamports_to_sol(collection["price"])) + " SOL")

    return table



def validate_me_purchase_results(nft_data: dict, filters: dict, min_rank: int = None, max_rank: int = None):
    
    if filters:
        
        attributes = nft_data["attributes"]
        
        if attributes:
            
            possible_attributes = []

            for attribute in attributes:
                
                possible_attributes.append(
                    {
                        "trait_type": attribute["trait_type"].lower().strip(),
                        "value": attribute["value"].lower().strip()
                    }
                )            
            
            if not all(attr in possible_attributes for attr in filters):
                    
                return False
        else:
            
            return False

    if min_rank is not None and max_rank is not None:
    
        if nft_data["rarity"]:
            
            ranks = [rank["rank"] for rank in nft_data["rarity"].values()]
            
            for rank in ranks:
                
                if not min_rank <= rank <= max_rank:
                    
                    return False
            
        else:
            
            return False
                
    return True

def validate_cc_purchase_results(nft_data: dict, filters: dict, min_rank: int, max_rank: int):

    if filters:
        
        attributes = nft_data["attributes"]
        
        if attributes:
            
            possible_attributes = []

            for attribute in attributes:
                
                possible_attributes.append(
                    {
                        "trait_type": attribute["trait_type"].lower(),
                        "value": attribute["value"].lower()
                    }
                )            
            
            if not all(attr in possible_attributes for attr in filters):
                    
                return False
        else:
            
            return False

    if min_rank is not None and max_rank is not None:
    
        if nft_data["rarity_rank"]:
                    
            if not min_rank <= nft_data["rarity_rank"] <= max_rank:
                
                return False
            
        else:
            
            return False
                
    return True

def check_marketplace_url(url):

    split_url = urlsplit(url)

    if "magiceden.io" in split_url.netloc:

        if "/marketplace/" in split_url.path and is_URL(url):

            return "magiceden"
        
    elif "opensea.io" in split_url.netloc:

        if "/collection/" in split_url.path and is_URL(url):

            return "opensea"

    return None


def check_spl_token(token_mint: str):
    
    
    try:
        
        client = Client(sol_rpc)
        
        return client.get_token_supply(token_mint).get("result")
    
    except:
        
        return False


def get_collection_symbol(url):

    split_url = urlsplit(url)

    return split_url.path.split("/")[-1]

    
def get_me_collection_metadata(symbol: str):

    last_listed = MagicEden.get_listed_nfts(
        symbol=symbol,
    )

    if last_listed:
        
        last_listed = last_listed[0]
        
        mint = last_listed["mintAddress"]
        
        nft_metadata = get_nft_metadata(mint_key=mint)
        
        if nft_metadata:
            
            uri = nft_metadata["data"]["uri"]
            
            try:
                
                uri_metadata = requests.get(uri).json()
                
            except:
                
                uri_metadata = None
                
            if uri_metadata:
                                
                attributes = [attribute["trait_type"] for attribute in uri_metadata["attributes"]] if uri_metadata.get("attributes") else []
                
                creators = nft_metadata["data"]["creators"]
            
                update_auth = nft_metadata["update_authority"]
            
                return {
                    "creators": creators,
                    "updateAuthority": update_auth,
                    "attributes": attributes
                }
        
    return None

def get_cc_collection_metadata(symbol: str):

    last_listed = CoralCube.get_listed_nfts(
        symbol=symbol,
    )

    if last_listed:
        
        last_listed = last_listed[0]
        
        mint = last_listed["mint"]
        
        nft_metadata = get_nft_metadata(mint_key=mint)
        
        if nft_metadata:
            
            uri = nft_metadata["data"]["uri"]
            
            try:
                
                uri_metadata = requests.get(uri).json()
                
            except:
                
                uri_metadata = None
                
            if uri_metadata:
                                
                attributes = [attribute["trait_type"] for attribute in uri_metadata["attributes"]] if uri_metadata.get("attributes") else []
                
                creators = nft_metadata["data"]["creators"]
            
                update_auth = nft_metadata["update_authority"]
            
                return {
                    "creators": creators,
                    "updateAuthority": update_auth,
                    "attributes": attributes
                }
        
    return None

def get_os_collection_metadata(symbol: str):
    
    try:
        
        headers = {
            'Host': 'api.opensea.io',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'x-build-id': '73afa61d8158d8f35097d0761fda94f7843a950b',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'x-signed-query': 'd73eda68d997705a2785aa8222d5a3c5663c392d0df699f665e44fb31e14642b',
            'x-api-key': '2f6f419a083c46de9d83ce3dbe7db601',
            'sec-ch-ua-platform': '"macOS"',
            'origin': 'https://opensea.io',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://opensea.io/',
            'accept-language': 'es-ES,es;q=0.9',
        }

        params = {
            'id': 'TraitsDropdownQuery',
            'query': 'query TraitsDropdownQuery(\n  $collection: CollectionSlug!\n) {\n  collection(collection: $collection) {\n    assetCount\n    numericTraits {\n      key\n      value {\n        max\n        min\n      }\n    }\n    stringTraits {\n      key\n      counts {\n        count\n        value\n      }\n    }\n    defaultChain {\n      identifier\n    }\n    id\n  }\n}\n',
            'variables': {
                'collection': symbol,
            },
        }

        payload = create_tls_payload(
            url="https://api.opensea.io/graphql/",
            method="POST",
            headers=headers,
            params=params
        )

        res = requests.post('http://127.0.0.1:3000/', json=payload, timeout=3).json()

        res = json.loads(res["body"])

        if res["data"]["collection"]["stringTraits"]:
            
            attributes = [attr["key"] for attr in res["data"]["collection"]["stringTraits"]]

        else:
            
            attributes = []
            
        return {
            
            "attributes": attributes
        }

    except:
        
        return None
    
    
def get_account_last_txs(account: str, limit: int, commitment: str, until: str = None):

    try:
        
        client = Client(sol_rpc)
        
        tx = client.get_signatures_for_address(account=account, limit=limit, commitment=Commitment(commitment), until=until)["result"]

        return tx

    except:
                
        return None


def create_csv_file(file_name: str, columns: list):
        
    clean_columns = [column for column in columns if column.isascii()]
    
    try:
            
        with open(f'{file_name}.csv', 'w', newline="") as f:
            
            writer = csv.writer(f)
            
            writer.writerow(clean_columns)
            writer.writerow([None]*len(clean_columns))
        
        return True
    
    except:
        
        return None


def get_sweeper_data(file_name: str):
    
    try:
        
        with open(f'{file_name}.csv', 'r') as f:

            reader = list(csv.reader(f))

            keys = reader[0]
            values = reader[1]
                    
        sweeper_data = dict(zip(keys, values))
        
        if sweeper_data["Amount"] and int(sweeper_data["Amount"]) > 0:
            
            sweeper_data["Amount"] = int(sweeper_data["Amount"])
                    
        elif sweeper_data["MaxFunds"] and float(sweeper_data["MaxFunds"]) > 0:
            
            sweeper_data["MaxFunds"] = float(sweeper_data["MaxFunds"])
                    
        elif sweeper_data["UnderPrice"] and float(sweeper_data["UnderPrice"]) > 0:
            
            sweeper_data["UnderPrice"] = float(sweeper_data["UnderPrice"])
            
                                                        
        else:
            
            return None
                        
        sweeper_data["MinRank"] = int(sweeper_data["MinRank"]) if sweeper_data["MinRank"] and int(sweeper_data["MinRank"]) >= 0 else None
        sweeper_data["MaxRank"] = int(sweeper_data["MaxRank"]) if sweeper_data["MaxRank"] and int(sweeper_data["MaxRank"]) >= 0 else None
            
        return sweeper_data
        
    except:
                
        return None

def monitor_os_sniper_file(file_name: str):
    
    global sniper_data
    
    while not kill_sniper:
        
        try:
            
            with open(f'{file_name}.csv', 'r') as f:

                reader = list(csv.reader(f))

                keys = reader[0]
                values = reader[1]
                        
            sniper_data_raw = dict(zip(keys, values))
            
            sniper_data_raw["MinPrice"] = float(sniper_data_raw["MinPrice"])
            sniper_data_raw["MaxPrice"] = float(sniper_data_raw["MaxPrice"])
                                
            sniper_data_raw["Gas"] = float(sniper_data_raw["Gas"])
                
            sniper_data = sniper_data_raw
            
        except:
                        
            sniper_data = None
            
        time.sleep(0.5)



def monitor_fff_sniper_file(file_name: str):
    
    global sniper_data
    
    while not kill_sniper:
        
        try:
            
            with open(f'{file_name}.csv', 'r') as f:

                reader = list(csv.reader(f))

                keys = reader[0]
                values = reader[1]
                        
            sniper_data_raw = dict(zip(keys, values))
            
            sniper_data_raw["MinPrice"] = float(sniper_data_raw["MinPrice"])
            sniper_data_raw["MaxPrice"] = float(sniper_data_raw["MaxPrice"])
                                                
            sniper_data = sniper_data_raw
            
        except:
                        
            sniper_data = None
            
        time.sleep(0.5)

def monitor_me_sniper_file(file_name: str):
    
    [None, None]
    
    global sniper_data, kill_sniper, current_floors
    
    [None, None]

    while not kill_sniper:
        
        collections = []
        
        try:
            
            with open(f'{file_name}.csv', 'r') as f:

                reader = csv.reader(f)

                reader = list(reader)
                
            keys = reader[0]
            rows = reader[1:]
            
            if not rows and sniper_start:
                
                kill_sniper = True
                
        except:
                
            rows = []

        for values in rows:
            
            sniper_data_raw = dict(zip(keys, values))
            
            try:
                
                if sniper_data_raw["Collection"]:
                    
                    if sniper_data_raw["MinPrice"] and sniper_data_raw["MaxPrice"]:

                        sniper_data_raw["MinPrice"] = float(sniper_data_raw["MinPrice"])
                        sniper_data_raw["MaxPrice"] = float(sniper_data_raw["MaxPrice"])

                        sniper_data_raw["UnderFloor(%)"] = None
                        
                    elif sniper_data_raw["UnderFloor(%)"]:

                        sniper_data_raw["UnderFloor(%)"] = float(sniper_data_raw["UnderFloor(%)"])

                        sniper_data_raw["MinPrice"] = None
                        sniper_data_raw["MaxPrice"] = None
                        
                    else:

                        raise ValueError
                                                
                    sniper_data_raw["MaxRank"] = int(sniper_data_raw["MaxRank"]) if sniper_data_raw["MaxRank"] else None
                                                
                    sniper_data_raw["MinRank"] = int(sniper_data_raw["MinRank"]) if sniper_data_raw["MinRank"] else None
                        
                    sniper_data_raw["AutoListByPrice(%)"] = float(sniper_data_raw["AutoListByPrice(%)"]) if sniper_data_raw["AutoListByPrice(%)"] else None
                        
                    sniper_data_raw["AutoListByFloor(%)"] = float(sniper_data_raw["AutoListByFloor(%)"]) if sniper_data_raw["AutoListByFloor(%)"] else None
                        
                    filtered_attributes = []
                    
                    if sniper_data_raw["Attributes"]:
                        
                        attributes = sniper_data_raw["Attributes"].split(";")
                        
                        for attribute in attributes:
                            
                            trait, value = attribute.split("=")

                            filtered_attributes.append(
                                {
                                    "trait_type": trait.lower().strip(),
                                    "value": value.lower().strip()
                                }
                            )
                        
                    sniper_data_raw["Attributes"] = filtered_attributes if filtered_attributes else None
                               
                    sniper_data_raw["Floor"] = current_floors[sniper_data_raw["Collection"]] if sniper_data_raw["Collection"] in current_floors.keys() else None
                    
                    collections.append(sniper_data_raw)
                
            except:
                                                
                pass
            
        sniper_data = collections
            
        time.sleep(0.5)



def monitor_cc_sniper_file(file_name: str):
    
    [None, None]
    
    global sniper_data, kill_sniper, current_floors
    
    [None, None]

    while not kill_sniper:
        
        collections = []
        
        try:
            
            with open(f'{file_name}.csv', 'r') as f:

                reader = csv.reader(f)

                reader = list(reader)
                
            keys = reader[0]
            rows = reader[1:]
            
            if not rows and sniper_start:
                
                kill_sniper = True
                
        
        except:
                
            rows = []

        for values in rows:
            
            sniper_data_raw = dict(zip(keys, values))
            
            try:
                
                if sniper_data_raw["Collection"]:
                    
                    if sniper_data_raw["MinPrice"] and sniper_data_raw["MaxPrice"]:

                        sniper_data_raw["MinPrice"] = float(sniper_data_raw["MinPrice"])
                        sniper_data_raw["MaxPrice"] = float(sniper_data_raw["MaxPrice"])

                        sniper_data_raw["UnderFloor(%)"] = None
                        
                    elif sniper_data_raw["UnderFloor(%)"]:

                        sniper_data_raw["UnderFloor(%)"] = float(sniper_data_raw["UnderFloor(%)"])

                        sniper_data_raw["MinPrice"] = None
                        sniper_data_raw["MaxPrice"] = None
                        
                    else:

                        raise ValueError
                                                
                    sniper_data_raw["MaxRank"] = int(sniper_data_raw["MaxRank"]) if sniper_data_raw["MaxRank"] else None
                                                
                    sniper_data_raw["MinRank"] = int(sniper_data_raw["MinRank"]) if sniper_data_raw["MinRank"] else None                        
                    
                    sniper_data_raw["AutoListByPrice(%)"] = float(sniper_data_raw["AutoListByPrice(%)"]) if sniper_data_raw["AutoListByPrice(%)"] else None
                        
                    sniper_data_raw["AutoListByFloor(%)"] = float(sniper_data_raw["AutoListByFloor(%)"]) if sniper_data_raw["AutoListByFloor(%)"] else None
                        
                    filtered_attributes = []
                    
                    if sniper_data_raw["Attributes"]:
                        
                        attributes = sniper_data_raw["Attributes"].split(";")
                        
                        for attribute in attributes:
                            
                            trait, value = attribute.split("=")

                            filtered_attributes.append(
                                {
                                    "trait_type": trait.lower().strip(),
                                    "value": value.lower().strip()
                                }
                            )
                        
                    sniper_data_raw["Attributes"] = filtered_attributes if filtered_attributes else None
                               
                    sniper_data_raw["Floor"] = current_floors[sniper_data_raw["Collection"]] if sniper_data_raw["Collection"] in current_floors.keys() else None
                    
                    collections.append(sniper_data_raw)
                
            except:
                                
                pass
            
        sniper_data = collections
            
        time.sleep(0.5)
        
def show_me_collection_current_floor(symbol: str):
    
    global current_floors
    
    try:

        last_listed = MagicEden.get_listed_nfts(
            symbol=symbol,
            limit=3
        )
        
        if last_listed:
        
            floor = last_listed[0]["price"]
            
            console.print(logger(f"{status} [yellow]Current floor[/] [white]{symbol}[/] [purple]>[/] [cyan]{floor} SOL[/]"))
            
            current_floors[symbol] = floor
                
    except:
        
        pass

def show_cc_collection_current_floor(symbol: str):
    
    global current_floors
    
    try:

        last_listed = CoralCube.get_listed_nfts(
            symbol=symbol,
            limit=3
        )
        
        if last_listed:
        
            floor = lamports_to_sol(last_listed[0]["price"])
            
            console.print(logger(f"{status} [yellow]Current floor[/] [white]{symbol}[/] [purple]>[/] [cyan]{floor} SOL[/]"))
            
            current_floors[symbol] = floor
                
    except:
        
        pass

def monitor_me_collection_floor():
            
    while not kill_sniper:
        
        if sniper_start:
            
            trs = []
            
            for collection in sniper_data:
                
                symbol = collection["Collection"]
                
                showFloorT = Thread(
                    target=show_me_collection_current_floor,
                    args=[symbol],
                    daemon=True
                )
                
                showFloorT.start()
                trs.append(showFloorT)

            for tr in trs:
                
                tr.join()
                
            time.sleep(10)



def monitor_cc_collection_floor():
            
    while not kill_sniper:
        
        if sniper_start:
            
            trs = []
            
            for collection in sniper_data:
                
                symbol = collection["Collection"]
                
                showFloorT = Thread(
                    target=show_cc_collection_current_floor,
                    args=[symbol],
                    daemon=True
                )
                
                showFloorT.start()
                trs.append(showFloorT)

            for tr in trs:
                
                tr.join()
                
            time.sleep(10)


def monitor_os_collection_floor(symbol: str):
            
    while not kill_sniper:
        
        if status:
                
            try:

                headers = {
                    'Host': 'api.opensea.io',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
                    'x-build-id': '2457c87a0e707327c43a6ac8251d326f5b8ddf3d',
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
                    'accept': '*/*',
                    'content-type': 'application/json',
                    'x-signed-query': 'a58c3c6aea76e9b6e7fa7207c21ab86c0638da0c809d802ffa4f888f8e91d290',
                    'x-api-key': '2f6f419a083c46de9d83ce3dbe7db601',
                    'sec-ch-ua-platform': '"macOS"',
                    'origin': 'https://opensea.io',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://opensea.io/',
                    'accept-language': 'es-ES,es;q=0.9',
                }

                params = {
                    'id': 'CollectionPageQuery',
                    'query': 'query CollectionPageQuery(\n  $collection: CollectionSlug!\n  $collections: [CollectionSlug!]\n  $collectionQuery: String\n  $includeHiddenCollections: Boolean\n  $numericTraits: [TraitRangeType!]\n  $query: String\n  $sortAscending: Boolean\n  $sortBy: SearchSortBy\n  $stringTraits: [TraitInputType!]\n  $toggles: [SearchToggle!]\n  $showContextMenu: Boolean\n  $isCategory: Boolean!\n  $includeCollectionFilter: Boolean!\n) {\n  collection(collection: $collection) {\n    isEditable\n    bannerImageUrl\n    name\n    description\n    imageUrl\n    relayId\n    connectedTwitterUsername\n    assetContracts(first: 2) {\n      edges {\n        node {\n          chain\n          id\n        }\n      }\n    }\n    representativeAsset {\n      assetContract {\n        chain\n        openseaVersion\n        id\n      }\n      id\n    }\n    slug\n    ...verification_data\n    ...collection_url\n    ...CollectionHeader_data\n    owner {\n      ...AccountLink_data\n      id\n    }\n    ...PhoenixCollectionSocialBar_data\n    ...PhoenixCollectionActionBar_data\n    ...PhoenixCollectionInfo_data\n    id\n  }\n  ...TrendingCollectionsList_data_29bCDU @include(if: $isCategory)\n  assets: query @skip(if: $isCategory) {\n    ...AssetSearch_data_40oIf9\n  }\n}\n\nfragment AccountLink_data on AccountType {\n  address\n  config\n  isCompromised\n  user {\n    publicUsername\n    id\n  }\n  displayName\n  ...ProfileImage_data\n  ...wallet_accountKey\n  ...accounts_url\n}\n\nfragment AssetCardAnnotations_assetBundle on AssetBundleType {\n  assetCount\n}\n\nfragment AssetCardAnnotations_asset_1OrK6u on AssetType {\n  assetContract {\n    chain\n    id\n  }\n  decimals\n  relayId\n  favoritesCount\n  isDelisted\n  isFavorite\n  isFrozen\n  hasUnlockableContent\n  ...AssetCardBuyNow_data\n  orderData {\n    bestAsk {\n      orderType\n      relayId\n      maker {\n        address\n        id\n      }\n    }\n  }\n  ...AssetContextMenu_data_3z4lq0 @include(if: $showContextMenu)\n}\n\nfragment AssetCardBuyNow_data on AssetType {\n  tokenId\n  relayId\n  assetContract {\n    address\n    chain\n    id\n  }\n  collection {\n    slug\n    id\n  }\n  orderData {\n    bestAsk {\n      relayId\n      decimals\n      paymentAssetQuantity {\n        asset {\n          usdSpotPrice\n          decimals\n          id\n        }\n        quantity\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardContent_asset on AssetType {\n  relayId\n  name\n  ...AssetMedia_asset\n  assetContract {\n    address\n    chain\n    openseaVersion\n    id\n  }\n  tokenId\n  collection {\n    slug\n    id\n  }\n  isDelisted\n}\n\nfragment AssetCardContent_assetBundle on AssetBundleType {\n  assetQuantities(first: 18) {\n    edges {\n      node {\n        asset {\n          relayId\n          ...AssetMedia_asset\n          id\n        }\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardFooter_assetBundle on AssetBundleType {\n  ...AssetCardAnnotations_assetBundle\n  name\n  assetCount\n  assetQuantities(first: 18) {\n    edges {\n      node {\n        asset {\n          collection {\n            name\n            relayId\n            slug\n            isVerified\n            ...collection_url\n            id\n          }\n          id\n        }\n        id\n      }\n    }\n  }\n  assetEventData {\n    lastSale {\n      unitPriceQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n  orderData {\n    bestBid {\n      orderType\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n    bestAsk {\n      maker {\n        address\n        id\n      }\n      closedAt\n      orderType\n      dutchAuctionFinalPrice\n      openedAt\n      priceFnEndedAt\n      quantity\n      decimals\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardFooter_asset_1OrK6u on AssetType {\n  ...AssetCardAnnotations_asset_1OrK6u\n  name\n  tokenId\n  collection {\n    slug\n    name\n    isVerified\n    ...collection_url\n    id\n  }\n  isDelisted\n  assetContract {\n    address\n    chain\n    openseaVersion\n    id\n  }\n  assetEventData {\n    lastSale {\n      unitPriceQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n  orderData {\n    bestBid {\n      orderType\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n    bestAsk {\n      maker {\n        address\n        id\n      }\n      closedAt\n      orderType\n      dutchAuctionFinalPrice\n      openedAt\n      priceFnEndedAt\n      quantity\n      decimals\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n}\n\nfragment AssetContextMenu_data_3z4lq0 on AssetType {\n  ...asset_edit_url\n  ...asset_url\n  ...itemEvents_data\n  relayId\n  isDelisted\n  isEditable {\n    value\n    reason\n  }\n  isListable\n  ownership(identity: {}) {\n    isPrivate\n    quantity\n  }\n  creator {\n    address\n    id\n  }\n  collection {\n    isAuthorizedEditor\n    id\n  }\n  imageUrl\n  ownedQuantity(identity: {})\n}\n\nfragment AssetMedia_asset on AssetType {\n  animationUrl\n  backgroundColor\n  collection {\n    displayData {\n      cardDisplayStyle\n    }\n    id\n  }\n  isDelisted\n  imageUrl\n  displayImageUrl\n}\n\nfragment AssetQuantity_data on AssetQuantityType {\n  asset {\n    ...Price_data\n    id\n  }\n  quantity\n}\n\nfragment AssetSearchFilter_data_PFx8Z on Query {\n  ...CollectionFilter_data_tXjHb @include(if: $includeCollectionFilter)\n  collection(collection: $collection) {\n    numericTraits {\n      key\n      value {\n        max\n        min\n      }\n      ...NumericTraitFilter_data\n    }\n    stringTraits {\n      key\n      ...StringTraitFilter_data\n    }\n    defaultChain {\n      identifier\n    }\n    id\n  }\n  ...PaymentFilter_data_2YoIWt\n}\n\nfragment AssetSearchList_data_gVyhu on SearchResultType {\n  asset {\n    assetContract {\n      address\n      chain\n      id\n    }\n    collection {\n      isVerified\n      relayId\n      id\n    }\n    relayId\n    tokenId\n    ...AssetSelectionItem_data\n    ...asset_url\n    id\n  }\n  assetBundle {\n    relayId\n    id\n  }\n  ...Asset_data_gVyhu\n}\n\nfragment AssetSearch_data_40oIf9 on Query {\n  ...AssetSearchFilter_data_PFx8Z\n  ...SearchPills_data_2Kg4Sq\n  search(collections: $collections, first: 32, numericTraits: $numericTraits, querystring: $query, resultType: ASSETS, sortAscending: $sortAscending, sortBy: $sortBy, stringTraits: $stringTraits, toggles: $toggles) {\n    edges {\n      node {\n        ...AssetSearchList_data_gVyhu\n        __typename\n      }\n      cursor\n    }\n    totalCount\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment AssetSelectionItem_data on AssetType {\n  backgroundColor\n  collection {\n    displayData {\n      cardDisplayStyle\n    }\n    imageUrl\n    id\n  }\n  imageUrl\n  name\n  relayId\n}\n\nfragment Asset_data_gVyhu on SearchResultType {\n  asset {\n    relayId\n    isDelisted\n    ...AssetCardContent_asset\n    ...AssetCardFooter_asset_1OrK6u\n    ...AssetMedia_asset\n    ...asset_url\n    ...itemEvents_data\n    orderData {\n      bestAsk {\n        paymentAssetQuantity {\n          quantityInEth\n          id\n        }\n      }\n    }\n    id\n  }\n  assetBundle {\n    relayId\n    ...bundle_url\n    ...AssetCardContent_assetBundle\n    ...AssetCardFooter_assetBundle\n    orderData {\n      bestAsk {\n        paymentAssetQuantity {\n          quantityInEth\n          id\n        }\n      }\n    }\n    id\n  }\n}\n\nfragment CollectionCardContextMenu_data on CollectionType {\n  ...collection_url\n}\n\nfragment CollectionCard_data on CollectionType {\n  ...CollectionCardContextMenu_data\n  ...CollectionCard_getShowCollectionCardData\n  ...collection_url\n  description\n  name\n  shortDescription\n  slug\n  logo\n  banner\n  isVerified\n  owner {\n    ...AccountLink_data\n    id\n  }\n  stats {\n    totalSupply\n    id\n  }\n  defaultChain {\n    identifier\n  }\n}\n\nfragment CollectionCard_getShowCollectionCardData on CollectionType {\n  logo\n  banner\n}\n\nfragment CollectionFilter_data_tXjHb on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n        assetCount\n        imageUrl\n        name\n        slug\n        isVerified\n        id\n      }\n    }\n  }\n  collections(first: 100, includeHidden: $includeHiddenCollections, query: $collectionQuery, sortBy: SEVEN_DAY_VOLUME) {\n    edges {\n      node {\n        assetCount\n        imageUrl\n        name\n        slug\n        isVerified\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment CollectionHeader_data on CollectionType {\n  name\n  description\n  imageUrl\n  bannerImageUrl\n  relayId\n  slug\n  owner {\n    ...AccountLink_data\n    id\n  }\n  ...CollectionStatsBar_data\n  ...SocialBar_data\n  ...verification_data\n  ...CollectionWatchlistButton_data\n}\n\nfragment CollectionModalContent_data on CollectionType {\n  description\n  imageUrl\n  name\n  slug\n}\n\nfragment CollectionStatsBar_data on CollectionType {\n  stats {\n    numOwners\n    totalSupply\n    id\n  }\n  nativePaymentAsset {\n    ...PaymentAssetLogo_data\n    id\n  }\n  ...collection_url\n  ...collection_stats\n}\n\nfragment CollectionWatchlistButton_data on CollectionType {\n  relayId\n  isWatching\n}\n\nfragment NumericTraitFilter_data on NumericTraitTypePair {\n  key\n  value {\n    max\n    min\n  }\n}\n\nfragment PaymentAssetLogo_data on PaymentAssetType {\n  symbol\n  asset {\n    imageUrl\n    id\n  }\n}\n\nfragment PaymentFilter_data_2YoIWt on Query {\n  paymentAssets(first: 10) {\n    edges {\n      node {\n        symbol\n        relayId\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n  PaymentFilter_collection: collection(collection: $collection) {\n    paymentAssets {\n      symbol\n      relayId\n      id\n    }\n    id\n  }\n}\n\nfragment PhoenixCollectionActionBar_data on CollectionType {\n  relayId\n  isWatching\n  ...collection_url\n  ...CollectionWatchlistButton_data\n}\n\nfragment PhoenixCollectionInfo_data on CollectionType {\n  description\n  name\n  nativePaymentAsset {\n    ...PaymentAssetLogo_data\n    id\n  }\n  ...collection_url\n  ...collection_stats\n}\n\nfragment PhoenixCollectionSocialBar_data on CollectionType {\n  assetContracts(first: 2) {\n    edges {\n      node {\n        address\n        blockExplorerLink\n        chain\n        chainData {\n          blockExplorerName\n        }\n        id\n      }\n    }\n  }\n  discordUrl\n  externalUrl\n  instagramUsername\n  mediumUsername\n  telegramUrl\n  twitterUsername\n  connectedTwitterUsername\n  ...collection_url\n}\n\nfragment Price_data on AssetType {\n  decimals\n  imageUrl\n  symbol\n  usdSpotPrice\n  assetContract {\n    blockExplorerLink\n    chain\n    id\n  }\n}\n\nfragment ProfileImage_data on AccountType {\n  imageUrl\n  user {\n    publicUsername\n    id\n  }\n  displayName\n}\n\nfragment SearchPills_data_2Kg4Sq on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n        imageUrl\n        name\n        slug\n        ...CollectionModalContent_data\n        id\n      }\n    }\n  }\n}\n\nfragment SocialBar_data on CollectionType {\n  relayId\n  discordUrl\n  externalUrl\n  instagramUsername\n  mediumUsername\n  slug\n  telegramUrl\n  twitterUsername\n  connectedTwitterUsername\n  assetContracts(first: 2) {\n    edges {\n      node {\n        blockExplorerLink\n        chainData {\n          blockExplorerName\n        }\n        id\n      }\n    }\n  }\n  ...collection_url\n  ...CollectionWatchlistButton_data\n}\n\nfragment StringTraitFilter_data on StringTraitType {\n  counts {\n    count\n    value\n  }\n  key\n}\n\nfragment TrendingCollectionsList_data_29bCDU on Query {\n  trendingCollections(categories: $collections, first: 12) {\n    edges {\n      node {\n        ...CollectionCard_data\n        ...CollectionCard_getShowCollectionCardData\n        relayId\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment accounts_url on AccountType {\n  address\n  user {\n    publicUsername\n    id\n  }\n}\n\nfragment asset_edit_url on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n  collection {\n    slug\n    id\n  }\n}\n\nfragment asset_url on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n}\n\nfragment bundle_url on AssetBundleType {\n  slug\n}\n\nfragment collection_stats on CollectionType {\n  statsV2 {\n    numOwners\n    totalSupply\n    totalVolume {\n      unit\n    }\n    floorPrice {\n      unit\n    }\n  }\n}\n\nfragment collection_url on CollectionType {\n  slug\n}\n\nfragment itemEvents_data on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n}\n\nfragment verification_data on CollectionType {\n  isMintable\n  isSafelisted\n  isVerified\n}\n\nfragment wallet_accountKey on AccountType {\n  address\n}\n',
                    'variables': {
                        'collection': symbol,
                        'collections': [
                            symbol,
                        ],
                        'collectionQuery': None,
                        'includeHiddenCollections': None,
                        'numericTraits': None,
                        'query': None,
                        'sortAscending': True,
                        'sortBy': 'PRICE',
                        'stringTraits': None,
                        'toggles': None,
                        'showContextMenu': True,
                        'isCategory': False,
                        'includeCollectionFilter': False,
                    },
                }

                payload = create_tls_payload(
                    url="https://api.opensea.io/graphql/",
                    method="POST",
                    headers=headers,
                    params=params
                )
                
                res = requests.post('http://127.0.0.1:3000', json=payload, timeout=3).json()

                res = json.loads(res["body"])
                
                floor = float(res["data"]["collection"]["statsV2"]["floorPrice"]["unit"])
                
                console.print(logger(f"{status} [yellow]Current floor price[/] [purple]>[/] {floor} ETH"))
            
            except:
                                
                pass
                
            time.sleep(10)


def get_drop_time():

    if PROGRAM in [SolanaPrograms.CMV2_PROGRAM, SolanaPrograms.LMN_PROGRAM]:

        meta = asyncio.run(get_account_metadata("CandyMachine", CM, PROGRAM))

        return int(meta.data.go_live_date)

    elif PROGRAM == SolanaPrograms.ME_PROGRAM:

        collection = get_launchpad_collection(collection_url)

        if collection:

            return collection["date"]

    elif PROGRAM == SolanaPrograms.ML_PROGRAM:
        
        return int(CM["REACT_APP_CANDY_START_DATE"])
    
    return None


def validate_sol_rpc(rpc: str):

    try:

        headers = {
            'Content-Type': 'application/json',
        }

        json_data = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'getEpochInfo',
        }

        res = requests.post(rpc, headers=headers, json=json_data, timeout=2)

        return int(res.elapsed.total_seconds()*1000)

    except:
        
        return None


def validate_eth_rpc(rpc: str):

    try:
        
        w3conn = Web3(Web3.HTTPProvider(rpc))

        return w3conn.isConnected()

    except:
        
        return False
    
def wait_for_drop(exit_before: int = 0):

    global DROP_TIME
    
    while True:

        ts_now = int(time.time())

        if DROP_TIME - exit_before <= ts_now:

            break

        if not user_time and int(str(ts_now)[-1]) == 0:

            new_time = get_drop_time()

            if new_time and new_time != DROP_TIME:

                DROP_TIME = new_time

                show_new_time = datetime.fromtimestamp(DROP_TIME).strftime("%H:%M:%S")
                
                console.print(
                    logger(f"[BOT] [yellow]Found time reschedule to {show_new_time}[/]\n"), end="")



def wait_for_mints():
        
    while True:
        
        current_minted = None
        
        if mode in [1,2,9]:
                
            metadata = asyncio.run(get_account_metadata("CandyMachine", CM, PROGRAM))   
            
            if metadata:
                
                if PROGRAM in [SolanaPrograms.CMV2_PROGRAM, SolanaPrograms.LMN_PROGRAM]:
                    
                    current_minted = metadata.items_redeemed
                    
                elif PROGRAM == SolanaPrograms.ME_PROGRAM:
                    
                    current_minted = metadata.items_redeemed_normal
                
        elif mode == 11:
            
            current_minted = get_ml_items_redeemed(index_key=CM["REACT_APP_INDEX_KEY"])
        
        if current_minted and current_minted >= await_mints:
                    
            break
        
        time.sleep(1)
    
def create_table_wallets(wallets: list):

    with console.status(f"[yellow]Downloading wallets data[/]", spinner="bouncingBar", speed=1.5):

        table = Table(show_lines=True)
        table.add_column("WALLET", style="green", justify="center")
        table.add_column("ADDRESS", style="yellow", justify="center")
        table.add_column("TASKS", style="cyan", justify="center")
        table.add_column("BALANCE", style="cyan", justify="center")

        if "gas" in wallets[0].keys():

            table.add_column("GAS", style="cyan", justify="center")

        for wallet in wallets:

            if "gas" in wallet.keys():

                balance = get_wallet_balance(
                    wallet["address"], blockchain="eth")

                table.add_row(wallet["name"], wallet["address"], str(
                    wallet["tasks"]), str(balance/(10**18)), str(wallet["gas"]))

            else:

                balance = get_wallet_balance(
                    wallet["address"], blockchain="sol")

                table.add_row(wallet["name"], wallet["address"], str(
                    wallet["tasks"]), str(round(lamports_to_sol(balance), 2)))

        return table


def create_table_contract(wallets: dict):

    table = Table(show_lines=True)
    table.add_column("NAME", style="yellow", justify="center")
    table.add_column("ADDRESS", style="green", justify="center")
    table.add_column("AMOUNT", style="cyan", justify="center")
    table.add_column("MINT PRICE", style="cyan", justify="center")
    table.add_column("GAS", style="cyan", justify="center")

    for wallet in wallets:

        table.add_row(wallet["name"], wallet["address"], str(
            wallet["amount"]), str(wallet["price"]), str(wallet["gas"]))

    return table



def set_app_title(text: str):

    if user_platform == "win32":

        os.system("title " + f"{text}")

    elif user_platform == "darwin":

        sys.stdout.write(f"\x1b]2;{text}\x07")



def show_cm_status(cm: str, program: str):

    available = redeemed = None
    
    if mode in [1,2,9]:
            
        metadata = asyncio.run(get_account_metadata(
            "CandyMachine",
            account=cm,
            prog=program
        ))

        if metadata:

            if program == SolanaPrograms.CMV2_PROGRAM:

                available = metadata.data.items_available
                redeemed = metadata.items_redeemed

            elif program == SolanaPrograms.ME_PROGRAM:

                available = metadata.items_available
                redeemed = metadata.items_redeemed_normal

            elif program == SolanaPrograms.LMN_PROGRAM:
                
                available = metadata.data.items_available
                redeemed = metadata.items_redeemed
                
    elif mode == 11:        
        
        if program == SolanaPrograms.ML_PROGRAM:
            
            available = int(cm["REACT_APP_INDEX_CAP"])
            redeemed = get_ml_items_redeemed(index_key=cm["REACT_APP_INDEX_KEY"])
        
    if available and redeemed:
            
        minted = int((redeemed/available) * 100)

        console.print(
            f"[AVAILABLE ~ [green]{available}[/]] [REDEEMED ~ [yellow]{redeemed}[/]] [MINTED ~ [cyan]{minted}%[/]]\n")


def get_range_to_operate(operation: str, wallet_to_operate: int = None):

    if operation == "wallets":

        total_lenght = len(wallets_nfts)
        question = "[purple] >>[/] Select wallet/s to operate in: "
        error = "[red]    Invalid wallet/s provided[/]"

    if operation == "nfts":

        total_lenght = len(wallets_nfts[wallet_to_operate]["nfts"])
        question = f"[purple] >>[/] Select NFT/s to operate for wallet {wallet_to_operate}: "
        error = "[red]    Invalid NFT/s provided[/]"

    while True:

        nfts = console.input(question)

        try:

            send = True
            operate = []

            if nfts == "e":

                return "e"

            if bool(re.compile(r'[^0-9-,]').search(nfts)):

                send = False

            if "," in nfts or "-" in nfts:

                if "," in nfts:

                    for section in nfts.split(","):

                        if "-" in section:

                            if section.count("-") == 1:

                                min, max = section.split("-")

                                for i in range(int(min), int(max) + 1):

                                    if i in range(0, total_lenght):

                                        operate.append(i)

                                    else:

                                        send = False
                            else:

                                send = False
                        else:

                            section = int(section)

                            if section in range(0, total_lenght):

                                operate.append(section)

                            else:

                                send = False

                elif "-" in nfts and nfts.count("-") == 1:

                    min, max = nfts.split("-")

                    for i in range(int(min), int(max) + 1):

                        if i in range(0, total_lenght):

                            operate.append(i)

                        else:

                            send = False
                else:

                    send = False

            else:

                nfts = int(nfts)

                if nfts in range(0, total_lenght):

                    operate.append(nfts)

                else:

                    send = False

            if send:

                return operate

        except:

            pass

        console.print(error)


def get_balance_to_transfer(wallet: int):

    while True:

        try:

            balance = console.input(
                f"[purple] >>[/] Select an amount to transfer from wallet {i}: ")

            if balance == "e":

                return "e"

            balance = int(sol_to_lamports(float(balance)))

            wallet_balance = wallets_nfts[wallet]["balance"]

            if balance < wallet_balance:

                return balance

            else:

                return wallet_balance - 50000

        except:
            
            pass

        console.print("[red]    Invalid amount provided[/]")


def get_wallet_to_transfer():

    while True:

        try:

            wallet = console.input(
                "[purple] >>[/] Select wallet to transfer: ")

            if wallet == "e":

                return "e"

            wallet = int(wallet)

            if wallet in range(0, len(wallets_nfts)):

                return wallet

        except:

            pass

        console.print("[red]    Invalid wallet provided[/]")


def get_listing_price():

    while True:

        price = console.input(
            "[purple] >>[/] Insert a price for listing: ")

        try:

            if price == "e":

                return "e"

            return float(price)

        except ValueError:

            pass

        console.print("[red]    Invalid price provided[/]")


def show_selected_nfts():

    for i, wallet in enumerate(wallets_nfts):

        wallet_address = wallet["address"]
        wallet_nfts = wallet["nfts"]
        wallet_balance = wallet["balance"]

        console.print(
            "[purple] >>[/] {:<10} [green]{}[/]\n".format(f"Wallet {i}:", wallet_address))

        console.print(
            "[purple]  >[/] {:<10} [cyan]{}[/]\n".format(f"Balance:", round(lamports_to_sol(wallet_balance), 2)))

        if wallet_nfts:

            for j, nft in enumerate(wallet_nfts):

                nft_name = nft["name"]

                if i in wallets_to_operate and j in raw_wallets_nfts[i]:

                    if operation_type in ["l", "ts", "tn", "b"]:
                        
                        console.print(
                            "[purple]  >[/] {:<10} [yellow]{}[/]".format(f"NFT {j}:", f"[purple]> [/]{nft_name}"))
                    
                    elif operation_type in ["d", "u"]:

                        console.print(
                            "[purple]  >[/] {:<10} [yellow]{}[/] [cyan]{}[/]".format(f"NFT {j}:", f"[purple]> [/]{nft_name}", nft["price"]))
                        
                else:
                    
                    if operation_type in ["l", "ts", "tn", "b"]:
                        
                        console.print(
                            "[purple]  >[/] {:<10} [yellow]{}[/]".format(f"NFT {j}:", nft_name))
                    
                    elif operation_type in ["d", "u"]:

                        console.print(
                            "[purple]  >[/] {:<10} [yellow]{}[/] [cyan]{}[/]".format(f"NFT {j}:", nft_name, nft["price"]))
                        
        else:

            if operation_type in ["l", "ts", "tn", "b"]:

                console.print(
                    "[purple]  >[/] [yellow]No NFT's found on this wallet")

            elif operation_type in ["d", "u"]:

                console.print(
                    "[purple]  >[/] [yellow]No NFT's listed by this wallet")

        print()

def check_node_health():
        
    try:
        
        client = Client(sol_rpc)
        
        chain_client = Client(SolanaEndpoints.MAINNET_RPC)
        
        for _ in range(5):
            
            real_slot = chain_client.get_slot()["result"]
            
            node_slot = client.get_slot()["result"]
            
            delay = real_slot - node_slot if real_slot - node_slot >= 0 else 0
            
            console.print(f" [yellow]Your node is behind by[/] [white]{delay}[/] [yellow]slots[yellow]")
            
            time.sleep(0.5)
    except:
        
        console.print(f" [red]Unreachable node[/]")

def get_module():

    options = list(range(1, 13))

    while True:

        try:

            mode = int(console.input(
                "[purple] >>[/] Select a module to use: "))

            if mode in options:

                return mode

        except ValueError:

            pass

        except KeyboardInterrupt:

            exit(0)

        console.print("[red]    Invalid option provided[/]")


def get_hwid():
    
    try:
        
        return str(subprocess.check_output("wmic csproduct get uuid"), "utf-8").strip("UUID").strip()

    except:
        
        return None

def start_tls():

    subprocess.Popen(
        [Paths.TLS_PATH],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(0.5)
    
    headers = {
        "Authorization": Keys.TLS_KEY
    }

    requests.post('http://127.0.0.1:3000/authenticate', headers=headers, timeout=4)

user_platform = sys.platform
set_app_title(f"Neura - {Bot.VERSION}")
console = Console(highlight=False, log_path=False)

try:
    
    helheim.auth(Keys.CF_API_KEY)
    
    helheim_auth = True
    
except:
    
    helheim_auth = False
    

try:
    database = NeuraDB(
        host="eu02-sql.pebblehost.com",
        user="customer_253216_neura",
        password="$7YDLyaCk-4zJpvkoLkU",
        database="customer_253216_neura"
    )

except:

    database = None


while True:

    clear()

    if user_platform == "darwin":
        
        break
    
    nft_holder = get_config(parameter="holder")
    user_hwid = get_hwid()
    
    if user_hwid:
            
        if nft_holder:

            if database:
                
                if "beta" in nft_holder:
                    
                    beta_access = database.check_beta_access(nft_holder, user_hwid)
                    
                    if beta_access:
                        
                        break
                    
                    else:

                        console.input(
                            "[yellow] ERROR![/] [red]Invalid or already in use beta key [/]", password=True)

                else:
                        
                    neura_hashlist = database.get_column_data("holders", "nft")

                    if neura_hashlist:
                        
                        holder_pubkey = get_pub_from_priv(privkey=nft_holder, blockchain="sol")

                        if holder_pubkey:
                            
                            holder_nft = wallet_is_holder(
                                pubkey=holder_pubkey, hashlist=neura_hashlist)

                            if holder_nft:

                                access = database.check_holder_access(
                                    holder_nft, holder_pubkey, user_hwid)

                                if access:

                                    break

                                else:
                                    console.input(
                                        "[yellow] ERROR![/] [red]Provided holder wallet is already in use [/]", password=True)

                            else:
                                console.input(
                                    "[yellow] ERROR![/] [red]Provided holder wallet has no Neura NFT [/]", password=True)
                        else:

                            console.input(
                                "[yellow] ERROR![/] [red]Invalid holder wallet provided[/]", password=True)
                            
                    else:

                        console.input(
                            "[yellow] ERROR![/] [red]Neura database is unreachable, please contact support [/]", password=True)
            else:
                console.input(
                    "[yellow] ERROR![/] [red]Unable to connect with the Nuera database, please restart and if the problem persists, contact Neura support [/]", password=True)
        else:
            console.input(
                "[yellow] ERROR![/] [red]Invalid holder private key or beta access code [/]", password=True)

    else:
        console.input(
            "[yellow] ERROR![/] [red]Unable to get device info, please contact support[/]", password=True)

database.close_connection()

while True:

    clear()

    if not all(file in os.listdir(os.path.join(os.getcwd(), "bin")) for file in ["TLS.exe", "bifrost.dll"]):

        console.input(
            "[yellow] ERROR![/] [red]Some of the Neura config files are missing, please contact support [/]", password=True)

    else:
            
        try:
            
            start_tls()

            break

        except:

            console.input(
                "[yellow] ERROR![/] [red]Some of the Neura config files are missing, please contact support [/]", password=True)
    
    
while True:

    CM = None
    PROGRAM = None
    DROP_TIME = None
    IDS = []
    
    clear(newline=False)

    sol_rpc = get_config(parameter="sol_rpc")
    eth_rpc = get_config(parameter="eth_rpc")
    user_time = get_config(parameter="time")
    advanced_mode = get_config(parameter="advanced")
    auto_timer = get_config(parameter="auto_timer")
    await_mints = get_config(parameter="await_mints")
    
    transaction_retry = 0
    max_tasks = 1000
    min_tasks = 500
    
    valid_sol_rpc = validate_sol_rpc(rpc=sol_rpc)
    valid_eth_rpc = validate_eth_rpc(rpc=eth_rpc)
    
    menu = False

    show_banner()

    if sol_rpc and valid_sol_rpc:

        console.print(
            " {:<10} [green]{:<5}[/] [purple]> [/]{}".format("SOL RPC:", "ON", f"{sol_rpc} [purple]>[/] {valid_sol_rpc} ms"))

    else:

        console.print(" {:<10} [red]OFF[/]".format("SOL RPC:"))

    if eth_rpc and valid_eth_rpc:

        console.print(
            " {:<10} [green]{:<5}[/] [purple]> [/]{}".format("ETH RPC:", "ON", eth_rpc))

    else:

        console.print(" {:<10} [red]OFF[/]".format("ETH RPC:"))

    if user_time:

        console.print(
            " {:<10} [green]{:<5}[/] [purple]> [/]{}".format("Time:", "ON", user_time))

    else:

        console.print(" {:<10} [red]OFF[/]".format("Time:"))
    
    print()

    console.print("[cyan] [1][/] CandyMachine mint")
    console.print("[cyan] [2][/] MagicEden mint")
    console.print("[cyan] [3][/] MagicEden sniper")
    console.print("[cyan] [4][/] Contract mint")
    console.print("[cyan] [5][/] OpenSea sniper")
    console.print("[cyan] [6][/] SOL wallets manager")
    console.print("[cyan] [7][/] MagicEden sweeper")
    console.print("[cyan] [8][/] FamousFox sniper")
    console.print("[cyan] [9][/] LaunchMyNFT mint")
    console.print("[cyan] [10][/] CoralCube sniper")
    console.print("[cyan] [11][/] MonkeLabs mint")
    console.print("[cyan] [12][/] Node health checker\n")
    
    mode = get_module()

    clear()

    while True:

        if menu:

            break

        if mode in [1, 2, 3, 6, 7, 8, 9, 10, 11]:

            wallets = get_sol_wallets()

            if not wallets:

                console.input(
                    "[yellow] ERROR![/] [red]Invalid wallets data / No wallets loaded [/]", password=True)

                break

            if not valid_sol_rpc:

                console.input(
                    "[yellow] ERROR![/] [red]Invalid or unreachable RPC [/]", password=True)

                break

        if mode in [4, 5]:

            if not valid_eth_rpc:

                console.input(
                    "[yellow] ERROR![/] [red]Invalid or unreachable RPC [/]", password=True)

                break
    
            
        if mode == 1:

            console.print(create_table_wallets(wallets))
            print()

            user_cmid = str(console.input(
                "[purple] >>[/] Candy Machine ID: ")).strip()

            clear()

            if user_cmid.lower() == "e":

                break

        if mode == 2:

            while True:
                
                if helheim_auth:
                        
                    console.print(create_table_wallets(wallets))
                    print()

                    collection_url = str(console.input(
                        "[purple] >>[/] MagicEden launchpad collection URL: ")).lower()
                    clear()

                    if collection_url == "e":
                        menu = True
                        break

                    with console.status("[yellow]Searching for collection[/]", spinner="bouncingBar", speed=1.5):

                        collection = get_launchpad_collection(collection_url)

                    if collection:

                        CM = collection["cmid"]
                        PROGRAM = SolanaPrograms.ME_PROGRAM
                        DROP_TIME = collection["date"]
                        
                        console.print(create_table_launchpad(collection))
                        print()

                        proceed = Prompt.ask(
                            "[purple] >>[/] Start mint?", choices=["y", "n"])
                        clear()

                        if proceed == "y":

                            break

                        else:
                            
                            pass

                    else:
                        console.print(
                            "[yellow] ERROR![/] [red]Collection not found\n [/]")
                else:
                    
                    console.input(
                        "[yellow] ERROR![/] [red]MagicEden launchpad unavailable [/]", password=True)
                    
                    menu = True
                    
                    break
                                  
        if mode == 3:

            console.print(create_table_wallets(wallets))
            print()
            
            wallet_choices = [wallet["name"].lower() for wallet in wallets] + ["e"]

            selected_wallet = Prompt.ask(
                "[purple] >>[/] Choose sniper wallet", choices=wallet_choices)

            if selected_wallet == "e":

                break

            wallet = [wallet for wallet in wallets if selected_wallet ==
                      wallet["name"].lower()][0]

            clear()


            sniper_default_filters = [
                "Collection",
                "MinPrice",
                "MaxPrice",
                "UnderFloor(%)",
                "MinRank",
                "MaxRank",
                "Attributes",
                "AutoListByPrice(%)",
                "AutoListByFloor(%)"
            ] 
            
            filters = sniper_default_filters
            
            clear()
            
            create_csv_file(file_name="me-sniper", columns=filters)
            
            console.print("[green] Sniper file created successfuly ![/]\n")                 

            start_sniper = Prompt.ask(
                "[purple] >>[/] Are you sure you want to continue? This will start the sniper instantly", choices=["y", "n"])
            
            print()

            if start_sniper == "y":
                
                sniper_data = []
                kill_sniper = False
                sniper_start = False
                current_floors = {}
                
                cached_collections = {}
                
                current_txs = []
                until_tx = None
                                
                privkey = wallet["privkey"]
                tasks = wallet["tasks"]
                pubkey = wallet["address"]
                
                monitorSniperFileT = Thread(
                    target=monitor_me_sniper_file,
                    args=["me-sniper"],
                    daemon=True
                )
                
                monitorSniperFileT.start()
                
                monitorCollectionsFloorT = Thread(
                    target=monitor_me_collection_floor,
                    daemon=True
                )
                
                monitorCollectionsFloorT.start()
                
                magic_eden = MagicEden(
                    rpc=sol_rpc,
                    privkey=privkey,
                )
                
                console.print(logger(f"[SNIPER] [cyan][COLLECTIONS ~ 0][/] [yellow]Loading file data and initialazing...[/]"))
                
                for _ in range(tasks):

                    while True:
                                                
                        if kill_sniper:
                            
                            break
                        
                        if sniper_data:
                            
                            loaded_collections = {}

                            for collection in sniper_data:
                                
                                symbol = collection["Collection"]
                                
                                if symbol not in cached_collections.values():
                                    
                                    collection_metadata = get_me_collection_metadata(symbol=symbol)

                                    if collection_metadata:
                                        
                                        collection_creators = collection_metadata["creators"]
                                        collection_update_auth = collection_metadata["updateAuthority"]
                                        
                                        collection_identifier = "".join(collection_creators + [collection_update_auth])
                                        
                                        loaded_collections[collection_identifier] = symbol
                                        cached_collections[collection_identifier] = symbol
                                        
                                        sniper_start = True
                                else:
                                    
                                    collection_identifier = list(cached_collections.keys())[list(cached_collections.values()).index(symbol)]
                                    loaded_collections[collection_identifier] = symbol
                                                        
                            status = f"[SNIPER] [cyan][COLLECTIONS ~ {len(loaded_collections)}][/]"
                            
                            last_txs = get_account_last_txs(
                                account="1BWutmTvYPwDtmw9abTkS4Ssr8no61spGAvW1X6NDix", 
                                limit=10, 
                                commitment="confirmed",
                                until=until_tx
                            )
                                                        
                            ready_to_purchase = False
                            
                            if last_txs:
                                
                                for tx in last_txs:
                                    
                                    signature = tx["signature"]
                                    
                                    if signature not in current_txs:

                                        current_txs.append(signature)
                                        
                                        console.print(logger(f"{status} [yellow]Fetching new data...[/]"))

                                        listing_info = magic_eden.check_tx_is_listing(tx=signature)
                                                                                
                                        if listing_info:
                                            
                                            mint_address = listing_info["mint"]
                                            seller = listing_info["seller"]
                                            price_in_sol = lamports_to_sol(listing_info["price"])
                                            price_in_lamports = listing_info["price"]
                                            escrow_pubkey = listing_info["escrow"]
                                            
                                            nft_metadata = get_nft_metadata(mint_key=mint_address)
                                            
                                            if nft_metadata:
                                                
                                                nft_name = nft_metadata["data"]["name"]
                                                nft_creators = nft_metadata["data"]["creators"]
                                                nft_update_auth = nft_metadata["update_authority"]
                                                
                                                to_match_identifier = "".join(nft_creators + [nft_update_auth])
                                                
                                                if to_match_identifier in loaded_collections.keys():
                                                                                                        
                                                    to_match_symbol = loaded_collections[to_match_identifier]
                                                    
                                                    matching_listing = False

                                                    for collection in sniper_data:
                                                        
                                                        if collection["Collection"] == to_match_symbol:
                                                            
                                                            min_sol = collection["MinPrice"]
                                                            max_sol = collection["MaxPrice"]
                                                            under_floor = collection["UnderFloor(%)"]
                                                            min_rank = collection["MinRank"]
                                                            max_rank = collection["MaxRank"]
                                                            autolist_by_price = collection["AutoListByPrice(%)"]
                                                            autolist_by_floor = collection["AutoListByFloor(%)"]
                                                            attributes = collection["Attributes"]
                                                            collection_floor = collection["Floor"]
                                                                
                                                            matching_listing = True
                                                            
                                                            break
                                                
                                                    if matching_listing:
                                                        
                                                        valid_listing = False
                                                        
                                                        if min_sol is not None and max_sol is not None:
                                                            
                                                            if min_sol <= price_in_sol <= max_sol:
                                                                
                                                                valid_listing = True
                                                                                                                        
                                                        elif under_floor is not None and collection_floor is not None:
                                                            
                                                            max_possible_price = collection_floor - (collection_floor * (under_floor/100))
                                                            
                                                            if price_in_sol <= max_possible_price:
                                                                
                                                                valid_listing = True
                                                                
                                                        if valid_listing:
                                                                                                                        
                                                            console.print(logger(f"{status} [yellow]Found possible NFT[/] [purple]>[/] [yellow]{nft_name}[/]"))
                                                            
                                                            if attributes or (min_rank is not None and max_rank is not None):
                                                                
                                                                nft_to_validate_data = CoralCube.get_nft_data(mint=mint_address)
                                                                
                                                                if nft_to_validate_data:
                                                                    
                                                                    is_valid_snipe = validate_cc_purchase_results(
                                                                        nft_to_validate_data, 
                                                                        filters=attributes,
                                                                        min_rank=min_rank,
                                                                        max_rank=max_rank
                                                                    )
                                                                    
                                                                    if is_valid_snipe:
                                                                        
                                                                        ready_to_purchase = True
                                                                        
                                                                        break
                                                                    
                                                                    else:
                                    
                                                                        console.print(logger(f"{status} [red]Rank or attributes do not match[/]"))
                                                                else:
                                                                    
                                                                    console.print(logger(f"{status} [red]Unable to get NFT data[/]"))
                                                            
                                                            else:
                                                                
                                                                ready_to_purchase = True
                                                                
                                                                break
                                                            
                                            else:
                                                
                                                console.print(logger(f"{status} [red]Unable to get NFT data (node)[/]"))
                                                
                                if len(current_txs) >= 500:

                                    current_txs = current_txs[-30:]

                                until_tx = last_txs[0]["signature"]
                                
                            elif last_txs is None:
                                    
                                console.print(logger(f"{status} [red]Unable to fetch new data (node)[/]"))
                                    
                            if ready_to_purchase:
                                                        
                                console.print(logger(f"{status} [yellow]Sniped {nft_name}[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))
                    
                                console.print(logger(f"{status} [yellow]Purchasing...[/]"))

                                tx_hash = magic_eden.buy_nft_api(
                                    seller=seller,
                                    price=price_in_lamports,
                                    mint=mint_address
                                )

                                if tx_hash:

                                    console.print(logger(f"{status} [green]Purchased {nft_name}[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))

                                    if autolist_by_floor is not None or autolist_by_price is not None:
                                        
                                        listing_price = None
                                        
                                        if autolist_by_price is not None:

                                            listing_price = (price_in_sol + (price_in_sol * autolist_by_price/100))
                                                
                                        elif autolist_by_floor is not None and collection_floor:
                                                                                                
                                            listing_price = (collection_floor + (collection_floor * autolist_by_floor/100))
                                        
                                        if listing_price:
                                            
                                            listing_price = round(listing_price, 3)
                                            
                                            console.print(logger(f"{status} [yellow]Listing {nft_name}[/] [purple]>[/] [cyan]{listing_price} SOL[/]"))
                                                    
                                            tx_hash = magic_eden.list_nft(
                                                seller=pubkey,
                                                mint=mint_address,
                                                price=sol_to_lamports(listing_price)
                                            )
                                            
                                            if tx_hash:
                                                                
                                                console.print(logger(f"{status} [green]Listed {nft_name}[/] [purple]>[/] [cyan]{listing_price} SOL[/]"))

                                            else:
                                                
                                                console.print(logger(f"{status} [red]Unable to list {nft_name}[/]"))
                                    
                                    break

                                else:

                                    console.print(logger(f"{status} [red]Purchase failed[/]"))
                
                    if kill_sniper:
                        
                        break
                
                kill_sniper = True
                        
                console.input(
                    "\n\n [purple]>>[/] Press ENTER to exit ", password=True)

                menu = True

                break

            clear()

        if mode == 4:

            wallets = get_eth_wallets()

            if wallets:

                console.print(create_table_contract(wallets))
                print()

                commit = Prompt.ask(
                    "[purple] >>[/] Do you want to start the minting process?", choices=["y", "n"])

                if commit == "n":

                    menu = True

            else:

                console.input(
                    "[yellow] ERROR![/] [red]Invalid minting contract setup file [/]", password=True)

                menu = True
                
        if mode == 5:

            wallets = get_eth_sniper_wallets()

            if wallets:
                
                console.print(create_table_wallets(wallets))
                print()
                
                wallet_choices = [wallet["name"].lower() for wallet in wallets] + ["e"]

                selected_wallet = Prompt.ask(
                    "[purple] >>[/] Choose sniper wallet", choices=wallet_choices)

                if selected_wallet == "e":

                    break

                wallet = [
                    wallet for wallet in wallets if selected_wallet == wallet["name"].lower()][0]

                clear()

                console.print(create_table_wallets([wallet]))
                print()

                url = str(console.input(
                    "[purple] >>[/] OpenSea collection URL: ")).lower()
                clear()

                if url == "e":

                    break

                with console.status("[yellow]Downloading collection data[/]", spinner="bouncingBar", speed=1.5):
                    
                    valid_collection = False
                    
                    if check_marketplace_url(url):

                        symbol = get_collection_symbol(url)
                        collection_metadata = get_os_collection_metadata(symbol)
                        
                        if collection_metadata:
                            
                            valid_collection = True
                            
                            collection_attributes = collection_metadata["attributes"]
                            

                if valid_collection:

                    sniper_default_filters = [
                        "Cancel",
                        "MinPrice",
                        "MaxPrice",
                        "Gas"
                    ]
                    
                    filters = sniper_default_filters + collection_attributes
                    
                    create_csv_file(file_name="os-sniper", columns=filters)
                    clear()
                    
                    console.print("[green] Sniper file created successfuly ![/]\n") 

                    start_sniper = Prompt.ask(
                        "[purple] >>[/] Are you sure you want to continue? This will start the sniper instantly", choices=["y", "n"])
                    print()

                    if start_sniper == "y":

                        privkey = wallet["privkey"]
                        address = wallet["address"]
                        tasks = wallet["tasks"]
                        
                        sniper_data = {}
                        kill_sniper = False
                        status = None
                        
                        monitorSniperFileT = Thread(
                            target=monitor_os_sniper_file,
                            args=["os-sniper"],
                            daemon=True
                        )
                        
                        monitorSniperFileT.start()
                        
                        monitorCollectionFloorT = Thread(
                            target=monitor_os_collection_floor,
                            args=[symbol],
                            daemon=True
                        )
                        
                        monitorCollectionFloorT.start()
                        
                        open_sea = OpenSea(
                            rpc=eth_rpc,
                            privkey=privkey
                        )
                        
                        for task in range(1, tasks + 1):

                            while True:
                                
                                if sniper_data:
                                    
                                    if sniper_data["Cancel"]:
                                        
                                        kill_sniper = True
                                        
                                        break

                                    min_eth = sniper_data["MinPrice"]
                                    max_eth = sniper_data["MaxPrice"]
                                    gas = sniper_data["Gas"]
                                    
                                    open_sea.gas_fee = gas
                                    
                                    attributes = [{"name": key, "values": [value]} for key, value in sniper_data.items() if key not in sniper_default_filters and value and key in collection_attributes]

                                    status = f"[SNIPER] [cyan][{symbol.upper()}] [{min_eth}-{max_eth} ETH] [GAS ~ {gas}]"
                                    
                                    if attributes:
                                        
                                        status += f"[cyan] [FILTERS ~ {len(attributes)}][/]"

                                    console.print(
                                        logger(f"{status} [yellow]Fetching new data..."))
                                    
                                    listings = OpenSea.get_listed_nfts(
                                        symbol=symbol,
                                        min_eth=min_eth,
                                        max_eth=max_eth,
                                        filters=attributes
                                    )

                                    if listings:
                                        
                                        asset = listings[0]["node"]["asset"]
                                        
                                        console.print(logger(f"{status} [yellow]Found possible NFT"))
                                        
                                        token_id = asset["tokenId"]
                                        price = int(asset["orderData"]["bestAsk"]["paymentAssetQuantity"]["quantity"])
                                        name = asset["name"]
                                    
                                        console.print(logger(f"{status} [yellow]Sniped {name}[/] [purple]>[/] [cyan]{round(float(price/(10**18)), 2)} ETH[/]"))
                                        
                                        console.print(
                                            logger(f"{status} [yellow]Purchasing..."))

                                        tx_hash = open_sea.buy_nft(
                                            symbol=symbol,
                                            token_id=token_id,
                                            price=price
                                        )

                                        if tx_hash:

                                            console.print(logger(
                                                f"{status} [green]Purchase successful[/] [purple]>[/] [cyan]{price/(10**18)} ETH[/]"))
                                            
                                            break
                                            
                                        else:

                                            console.print(
                                                logger(f"{status} [red]Purchase failed"))
                                else:
                                     
                                    console.print("[red] Invalid sniper file data or format[/]")
                                    
                                    time.sleep(0.5)

                            
                            if kill_sniper:
                                
                                break
                        
                        kill_sniper = True
                        
                        console.input(
                            "\n\n [purple]>>[/] Press ENTER to exit ", password=True)

                        menu = True

                        break
                
                else:

                    clear()

                    console.print("[yellow] ERROR![/] [red]Invalid collection URL\n[/]")
                
            else:

                console.input("[yellow] ERROR![/] [red]Invalid parameters provided for sniper wallet [/]", password=True)

                menu = True

        if mode == 6:

            while True:
                    
                wallets_nfts = []

                operation_type = Prompt.ask(
                    "[purple] >>[/] What would you like to do?", choices=["l", "d", "u", "ts", "tn", "b", "e"])

                if operation_type == "e":

                    break

                clear()

                with console.status(f"[yellow]Downloading wallets data[/]", spinner="bouncingBar", speed=1.5):
                    
                    for wallet in wallets:

                        if operation_type in ["l", "ts", "tn", "b"]:

                            wallet_nfts = MagicEden.get_wallet_nfts(wallet["address"])

                        elif operation_type in ["d", "u"]:

                            wallet_nfts = MagicEden.get_wallet_listed(wallet["address"])                        
                        
                        if wallet_nfts is None:
                            
                            break
                        
                        balance = get_wallet_balance(wallet["address"], blockchain="sol")

                        nfts_data = []

                        for nft in wallet_nfts:
                            
                            if operation_type in ["l", "ts", "tn", "b"]:

                                nfts_data.append({"mint": nft["mintAddress"], "name": nft["title"], "token": nft["id"]})

                            elif operation_type in ["d", "u"]:

                                nfts_data.append({"mint": nft["initializerDepositTokenMintAddress"], "name": nft["title"], "token": nft["initializerDepositTokenAccount"], "price": lamports_to_sol(nft["takerAmount"])})
                        
                        sorted_names = sorted([nft["name"] for nft in nfts_data])

                        sorted_nfts_data = []
                        
                        for _ in range(len(sorted_names)):
                            
                            leader_name = sorted_names.pop(0)
                            
                            for nft in nfts_data:
                                                        
                                if nft["name"] == leader_name:
                                
                                    sorted_nfts_data.append(nft)
                                    
                                    break
                            
                        wallets_nfts.append({
                            "name": wallet["name"],
                            "address": wallet["address"],
                            "privkey": wallet["privkey"],
                            "balance": balance,
                            "nfts": sorted_nfts_data
                        })


                    if wallet_nfts is None:
                        
                        clear()
                        
                        console.print("[yellow] ERROR![/] [red]Unable to get wallets data\n[/]")
                    
                    else:
                        
                        break
                    
            for i, wallet in enumerate(wallets_nfts):

                wallet_address = wallet["address"]
                wallet_nfts = wallet["nfts"]
                wallet_balance = wallet["balance"]

                console.print(
                    "[purple] >>[/] {:<10} [green]{}[/]\n".format(f"Wallet {i}:", wallet_address))

                console.print(
                    "[purple]  >[/] {:<10} [cyan]{}[/]\n".format(f"Balance:", round(lamports_to_sol(wallet_balance), 2)))

                if wallet_nfts:

                    for j, nft in enumerate(wallet_nfts):

                        nft_name = nft["name"]

                        if operation_type in ["l", "ts", "tn", "b"]:
                            
                            console.print("[purple]  >[/] {:<10} [yellow]{}[/]".format(f"NFT {j}:", nft_name))
                        
                        elif operation_type in ["d", "u"]:

                            console.print("[purple]  >[/] {:<10} [yellow]{}[/] [cyan]{}[/]".format(f"NFT {j}:", nft_name, nft["price"]))
                            
                else:

                    if operation_type in ["l", "ts", "tn", "b"]:

                        console.print("[purple]  >[/] [yellow]No NFT's found on this wallet")

                    elif operation_type in ["d", "u"]:

                        console.print("[purple]  >[/] [yellow]No NFT's listed by this wallet")
                print()

            print()

            if operation_type in ["l", "d", "u", "tn", "b"]:

                raw_wallets_nfts = {}

                wallets_to_operate = get_range_to_operate(
                    operation="wallets")

                if wallets_to_operate == "e":

                    break

                for i in wallets_to_operate:

                    nfts_to_operate = get_range_to_operate(
                        operation="nfts", wallet_to_operate=i)

                    raw_wallets_nfts[i] = nfts_to_operate

                    if nfts_to_operate == "e":

                        break

                if nfts_to_operate == "e":

                    break

                clear()

                show_selected_nfts()

                print()

                if operation_type in ["l", "u"]:

                    listing_price = get_listing_price()

                    if listing_price == "e":

                        break

                elif operation_type in ["d", "b"]:
                    
                    if operation_type == "d":
                        
                        console.input("[purple] >>[/] Press ENTER to continue with the delisting process ", password=True)
                        
                    elif operation_type == "b":
                        
                        console.input("[purple] >>[/] Press ENTER to continue with the burn process ", password=True)
                        
                elif operation_type == "tn":

                    wallet_to_transfer = get_wallet_to_transfer()

                    if wallet_to_transfer == "e":

                        break

                clear()

                trs = []

                for wallet, nfts in raw_wallets_nfts.items():

                    privkey = wallets_nfts[wallet]["privkey"]
                    pubkey = wallets_nfts[wallet]["address"]
                    
                    for nft in nfts:

                        nft_data = wallets_nfts[wallet]["nfts"][nft]

                        name = nft_data["name"]
                        mint_address = nft_data["mint"]
                        token = nft_data["token"]

                        if operation_type in ["l", "u"]:

                            if operation_type == "l":

                                console.print(logger(f"[MANAGER] [cyan][OPERATION ~ List][/] [yellow]Listing {name} at {listing_price}[/]"))

                            elif operation_type == "u":

                                console.print(logger(f"[MANAGER] [cyan][OPERATION ~ Update][/] [yellow]Updating {name} price to {listing_price}[/]"))
                            
                            manager = MagicEden(
                                rpc=sol_rpc,
                                privkey=privkey
                            )
                            
                            operationT = Thread(
                                target=manager.list_nft,
                                args=[pubkey, mint_address, sol_to_lamports(listing_price)]
                            )

                        elif operation_type == "d":

                            delisting_price = nft_data["price"]

                            console.print(logger(f"[MANAGER] [cyan][OPERATION ~ Delist][/] [yellow]Delisting {name}[/]"))
                            
                            manager = MagicEden(
                                rpc=sol_rpc,
                                privkey=privkey
                            )
                            
                            operationT = Thread(
                                target=manager.delist_nft,
                                args=[pubkey, mint_address, sol_to_lamports(delisting_price)]
                            )

                        elif operation_type == "tn":

                            dest_wallet = wallets_nfts[wallet_to_transfer]["address"]
                            dest_name = wallets_nfts[wallet_to_transfer]["name"]

                            wallet_manager = SolWalletManager(
                                rpc=sol_rpc,
                                privkey=privkey
                            )
                            
                            console.print(logger(f"[MANAGER] [cyan][OPERATION ~ Transfer NFT][/] [yellow]Transfering {name} to {dest_name.upper()}[/]"))

                            operationT = Thread(
                                target=wallet_manager.transfer_nft,
                                args=[mint_address, dest_wallet]
                            )

                        elif operation_type == "b":
                            
                            console.print(logger(f"[MANAGER] [cyan][OPERATION ~ Burn][/] [yellow]Burning {name}[/]"))
                            
                            wallet_manager = SolWalletManager(
                                rpc=sol_rpc,
                                privkey=privkey
                            )
                            
                            operationT = Thread(
                                target=wallet_manager.burn_nft,
                                args=[mint_address]
                            )
                            
                        operationT.start()
                        trs.append(operationT)

                for tr in trs:

                    tr.join()

                print("\n")

                console.input("[purple] >>[/] Press ENTER to go back to the menu ", password=True)

                break

            elif operation_type in ["ts"]:

                raw_wallets_balances = {}

                wallets_to_operate = get_range_to_operate(
                    operation="wallets")

                if wallets_to_operate == "e":

                    break

                for i in wallets_to_operate:

                    balance_to_operate = get_balance_to_transfer(i)

                    raw_wallets_balances[i] = balance_to_operate

                    if balance_to_operate == "e":

                        break

                if balance_to_operate == "e":

                    break
                
                wallet_to_transfer = get_wallet_to_transfer()

                if wallet_to_transfer == "e":

                    break

                clear()

                trs = []

                dest_wallet = wallets_nfts[wallet_to_transfer]["address"]
                dest_name = wallets_nfts[wallet_to_transfer]["name"]
                total_transfer_amount = round(lamports_to_sol(sum(list(raw_wallets_balances.values()))), 2)

                for wallet, balance in raw_wallets_balances.items():

                    privkey = wallets_nfts[wallet]["privkey"]

                    wallet_manager = SolWalletManager(
                        rpc=sol_rpc,
                        privkey=privkey
                    )
                    
                    console.print(logger(f"[MANAGER] [cyan][OPERATION ~ Transfer SOL][/] [yellow]Transfering {lamports_to_sol(balance)} SOL to {dest_name.upper()}[/]"))

                    operationT = Thread(
                        target=wallet_manager.transfer_sol,
                        args=[balance, dest_wallet]
                    )

                    operationT.start()
                    trs.append(operationT)

                for tr in trs:

                    tr.join()

                print("\n")

                console.input("[purple] >>[/] Press ENTER to go back to the menu ", password=True)

                break
        
        if mode == 7:
            
            console.print(create_table_wallets(wallets))
            print()
            
            wallet_choices = [wallet["name"].lower() for wallet in wallets] + ["e"]

            selected_wallet = Prompt.ask("[purple] >>[/] Choose sweeper wallet", choices=wallet_choices)

            if selected_wallet == "e":

                break

            wallet = [wallet for wallet in wallets if selected_wallet ==
                      wallet["name"].lower()][0]

            clear()

            while True:

                console.print(create_table_wallets([wallet]))
                print()

                url = str(console.input("[purple] >>[/] Marketplace collection URL: ")).lower().strip()
                clear()

                if url == "e":
                    menu = True
                    break

                with console.status("[yellow]Downloading collection data[/]", spinner="bouncingBar", speed=1.5):
                    
                    valid_collection = False    

                    if check_marketplace_url(url):

                        symbol = get_collection_symbol(url)
                        collection_metadata = get_me_collection_metadata(symbol)

                        if collection_metadata:
                            
                            valid_collection = True
                                
                            collection_attributes  = collection_metadata["attributes"]

                if valid_collection:
                    
                    sweeper_default_filters = [
                        "Amount",
                        "MaxFunds",
                        "UnderPrice",
                        "MinRank",
                        "MaxRank",
                    ] 
                    
                    filters = sweeper_default_filters + collection_attributes
                    
                    clear()
                    
                    if create_csv_file(file_name="me-sweeper", columns=filters):
                    
                        console.print("[green] Sweeper file created successfuly ![/]\n")                 

                        start_sweeper = Prompt.ask(
                            "[purple] >>[/] Are you sure you want to continue? This will start the sweeper instantly", choices=["y", "n"])
                        
                    else:
                        
                        console.print("[red] Unexpected error while creating sweeper file[/]\n")    
                        
                        start_sweeper = "n"
                        
                    print()
                    
                    if start_sweeper == "y":
                        
                        privkey = wallet["privkey"]
                        
                        while True:
                            
                            sweeper_data = get_sweeper_data(file_name="me-sweeper")
                            
                            if sweeper_data:
                                
                                break
                            
                            else:
                                
                                console.print("[red] Invalid sniper file data or format[/]")
                                        
                                time.sleep(0.5)
                        
                        amount = sweeper_data["Amount"]
                        max_funds = sweeper_data["MaxFunds"]
                        under_price = sweeper_data["UnderPrice"]
                        min_rank = sweeper_data["MinRank"]
                        max_rank = sweeper_data["MaxRank"]

                        if amount:
                            
                            max_funds = under_price = None
                        
                        elif max_funds:
                            
                            amount = under_price = None
                            
                        elif under_price:
                            
                            amount = max_funds = None
                            
                        attributes = {key: value for key, value in sweeper_data.items() if key not in sweeper_default_filters and value and key in collection_attributes}
                        
                        if amount is not None:
                            
                            status = status = f"[SWEEPER] [cyan][{symbol.upper()}] [AMOUNT ~ {amount}][/]"
                        
                        elif max_funds is not None:
                            
                            status = status = f"[SWEEPER] [cyan][{symbol.upper()}] [FUNDS ~ {max_funds} SOL][/]"
                        
                        elif under_price is not None:
                            
                            status = status = f"[SWEEPER] [cyan][{symbol.upper()}] [MAX PRICE ~ {under_price} SOL][/]"
                            
                        if min_rank is not None and max_rank is not None:
                                            
                            status += f"[cyan] [{min_rank}-{max_rank} RANK][/]"
                        
                        if attributes:
                            
                            status += f"[cyan] [FILTERS ~ {len(attributes)}][/]"
                            
                        while True:
                            
                            console.print(logger(f"{status} [yellow]Fetching listed NFT's[/]"))
                            
                            matching_nfts = MagicEden.get_listed_nfts(
                                symbol=symbol,
                                limit=100
                                
                            )
                            
                            if matching_nfts:
                                
                                break
                            
                            else:
                                
                                console.print(logger(f"{status} [red]Error while fetching listings[/]"))
                        
                        console.print(logger(f"{status} [yellow]Found collection listings[/]"))
                        
                        total_purchased = 0
                        total_spent = 0
                        
                        valid_nfts = []
                        
                        for nft in matching_nfts:
                                
                            name = nft["title"]
                            price = nft["price"]
                                
                            valid_nft = False
                            
                            console.print(logger(f"{status} [yellow]Validating {name} [purple]>[/] [cyan]{price} SOL[/]"))
                            
                            if not under_price or under_price < price:
                                                                        
                                valid_nft = validate_me_purchase_results(
                                    nft_data=nft,
                                    filters=attributes,
                                    min_rank=min_rank,
                                    max_rank=max_rank
                                )                               
                                
                            if valid_nft:
                                
                                total_purchased += 1
                                total_spent += price
                                
                                if amount is not None and total_purchased > amount:
                                    
                                    console.print(logger(f"{status} [yellow]Reached max amount[/]"))
                                    
                                    break
                                
                                if max_funds is not None and total_spent >= max_funds:
                                    
                                    console.print(logger(f"{status} [yellow]Reached max expenses[/]"))
                                    
                                    break
                                    
                                console.print(logger(f"{status} [green]Validated {name} [purple]>[/] [cyan]{price} SOL[/]"))

                                valid_nfts.append(nft)
                                
                            else:
                                
                                console.print(logger(f"{status} [red]Invalid {name} [purple]>[/] [cyan]{price} SOL[/]"))
                                
                            time.sleep(0.1)

                        console.print(logger(f"{status} [yellow]Found {len(valid_nfts)} NFT's[/] [purple]>[/] [cyan]{total_spent} SOL[/]"))
                        
                        sniper = MagicEden(
                            rpc=sol_rpc,
                            privkey=privkey
                        )
                        
                        trs = []                            

                        for nft in valid_nfts:
                            
                            name = nft["title"]
                            seller = nft["owner"]
                            mint_address = nft["mintAddress"]
                            price = nft["price"]
                            creators = [creator["address"] for creator in nft["creators"]]
                            escrow_pubkey = nft["escrowPubkey"]
                                                        
                            console.print(logger(f"{status} [yellow]Purchasing {name}[/] [purple]>[/] [cyan]{price}[/]"))
                            
                            buyT = Thread(
                                target=sniper.buy_nft_api,
                                args=[
                                    seller,
                                    sol_to_lamports(price),
                                    mint_address,
                                ]
                            )
                            
                            buyT.start()
                            trs.append(buyT)
                        
                        for tr in trs:
                            
                            tr.join()
                            
                        console.input("\n\n [purple]>>[/] Press ENTER to exit ", password=True)

                        menu = True

                        break
                
                
                    else:
                        
                        clear()
                        
                else:

                    clear()

                    console.print(
                        "[yellow] ERROR![/] [red]Invalid collection URL\n[/]")
                    
        if mode == 8:
            
            console.print(create_table_wallets(wallets))
            print()
            
            wallet_choices = [wallet["name"].lower() for wallet in wallets] + ["e"]

            selected_wallet = Prompt.ask(
                "[purple] >>[/] Choose sniper wallet", choices=wallet_choices)

            if selected_wallet == "e":

                break

            wallet = [wallet for wallet in wallets if selected_wallet ==
                      wallet["name"].lower()][0]

            clear()

            while True:

                console.print(create_table_wallets([wallet]))
                print()

                token_mint = str(console.input(
                    "[purple] >>[/] WhiteList token address: ")).strip()
                clear()

                if token_mint == "e":
                    
                    menu = True
                    
                    break

                with console.status("[yellow]Downloading token data[/]", spinner="bouncingBar", speed=1.5):
                    
                    valid_token = check_spl_token(token_mint=token_mint)    
                    

                if valid_token:
                    
                    sniper_default_filters = [
                        "Cancel",
                        "MinPrice",
                        "MaxPrice"
                    ] 
                    
                    filters = sniper_default_filters
                    
                    clear()
                    
                    if create_csv_file(file_name="fff-sniper", columns=filters):
                    
                        console.print("[green] Sniper file created successfuly ![/]\n")                 

                        start_sniper = Prompt.ask(
                            "[purple] >>[/] Are you sure you want to continue? This will start the sniper instantly", choices=["y", "n"])
                        
                        print()

                        if start_sniper == "y":
                            
                            sniper_data = {}
                            kill_sniper = False
                            current_txs = []
                            until_tx = None
                            
                            privkey = wallet["privkey"]
                            tasks = wallet["tasks"]
                            
                            monitorSniperFileT = Thread(
                                target=monitor_fff_sniper_file,
                                args=["fff-sniper"],
                                daemon=True
                            )
                            
                            monitorSniperFileT.start()
                            
                            famous_fox = FamousFox(
                                rpc=sol_rpc,
                                privkey=privkey,
                            )
                            
                            for _ in range(tasks):

                                while True:
                                    
                                    if sniper_data:
                                        
                                        if sniper_data["Cancel"]:
                                            
                                            kill_sniper = True
                                            
                                            break
                                        
                                        min_sol = sniper_data["MinPrice"]
                                        max_sol = sniper_data["MaxPrice"]

                                        status = f"[SNIPER] [cyan][{token_mint}] [{min_sol}-{max_sol} SOL][/]"

                                        last_txs = get_account_last_txs(
                                            account="8BYmYs3zsBhftNELJdiKsCN2WyCBbrTwXd6WG4AFPr6n", 
                                            limit=10, 
                                            commitment="confirmed",
                                            until=until_tx
                                        )
                                                                                
                                        if last_txs:
                                            
                                            for tx in last_txs:
                                                
                                                signature = tx["signature"]
                                                
                                                if signature not in current_txs:

                                                    current_txs.append(signature)
                                                    
                                                    console.print(logger(f"{status} [yellow]Fetching new data...[/]"))

                                                    listing_info = famous_fox.check_tx_is_listing(tx=signature)
                                                    
                                                    if listing_info:
                                                        
                                                        price_in_sol = lamports_to_sol(listing_info["price"])
                                                        price_in_lamports = listing_info["price"]
                                                        mint_address = listing_info["mint"]
                                                        seller = listing_info["seller"]
                                                            
                                                        if min_sol <= price_in_sol <= max_sol and mint_address == token_mint:

                                                            console.print(logger(
                                                                f"{status} [yellow]Sniped token[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))
                                                            
                                                            tx_hash = famous_fox.buy_token(
                                                                mint=token_mint,
                                                                price=price_in_lamports,
                                                                seller=seller
                                                            )
                                                            
                                                            if tx_hash:

                                                                console.print(logger(
                                                                    f"{status} [green]Purchase successful[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))
                                                                
                                                                break

                                                            else:

                                                                console.print(logger(
                                                                    f"{status} [red]Purchase failed[/]"))
                                            
                                            if len(current_txs) >= 500:
            
                                                current_txs = current_txs[-30:]

                                            until_tx = last_txs[0]["signature"]
                                            
                                        elif last_txs is None:
                                                
                                            console.print(logger(f"{status} [red]Unable to fetch new data (node)[/]"))
                                          
                                    else:
                                        
                                        console.print("[red] Invalid sniper file data or format[/]")
                                        
                                        time.sleep(0.5)
                            
                                if kill_sniper:
                                    
                                    break
                            
                            kill_sniper = True
                                    
                            console.input(
                                "\n\n [purple]>>[/] Press ENTER to exit ", password=True)

                            menu = True

                            break

                        clear()
                    
                    else:
                        
                        clear()
                        
                        console.print("[yellow] ERROR![/][red] Unexpected error while creating sniper file[/]\n")    
                        
                        start_sniper = "n"
                        

                else:

                    clear()

                    console.print(
                        "[yellow] ERROR![/] [red]Invalid WhiteList token\n[/]")

        if mode == 9:
            
            console.print(create_table_wallets(wallets))
            print()

            user_cmid = str(console.input(
                "[purple] >>[/] Candy Machine ID: ")).strip()

            clear()

            if user_cmid.lower() == "e":

                break
        
        if mode == 10:

            console.print(create_table_wallets(wallets))
            print()
            
            wallet_choices = [wallet["name"].lower() for wallet in wallets] + ["e"]

            selected_wallet = Prompt.ask(
                "[purple] >>[/] Choose sniper wallet", choices=wallet_choices)

            if selected_wallet == "e":

                break

            wallet = [wallet for wallet in wallets if selected_wallet ==
                      wallet["name"].lower()][0]

            clear()


            sniper_default_filters = [
                "Collection",
                "MinPrice",
                "MaxPrice",
                "UnderFloor(%)",
                "MinRank",
                "MaxRank",
                "Attributes",
                "AutoListByPrice(%)",
                "AutoListByFloor(%)"
            ] 
            
            filters = sniper_default_filters
            
            clear()
            
            create_csv_file(file_name="cc-sniper", columns=filters)
            
            console.print("[green] Sniper file created successfuly ![/]\n")                 

            start_sniper = Prompt.ask(
                "[purple] >>[/] Are you sure you want to continue? This will start the sniper instantly", choices=["y", "n"])
            
            print()

            if start_sniper == "y":
                
                sniper_data = []
                kill_sniper = False
                sniper_start = False
                current_floors = {}
                
                cached_collections = {}
                
                current_txs = []
                until_tx = None
                                
                privkey = wallet["privkey"]
                tasks = wallet["tasks"]
                pubkey = wallet["address"]
                
                monitorSniperFileT = Thread(
                    target=monitor_cc_sniper_file,
                    args=["cc-sniper"],
                    daemon=True
                )
                
                monitorSniperFileT.start()
                
                monitorCollectionsFloorT = Thread(
                    target=monitor_cc_collection_floor,
                    daemon=True
                )
                
                monitorCollectionsFloorT.start()
                
                coral_cube = CoralCube(
                    rpc=sol_rpc,
                    privkey=privkey,
                )
                
                console.print(logger(f"[SNIPER] [cyan][COLLECTIONS ~ 0][/] [yellow]Loading file data and initialazing...[/]"))
                
                for _ in range(tasks):

                    while True:
                                                
                        if kill_sniper:
                            
                            break
                        
                        if sniper_data:

                            loaded_collections = {}

                            for collection in sniper_data:
                                
                                symbol = collection["Collection"]
                                
                                if symbol not in cached_collections.values():
                                    
                                    collection_metadata = get_cc_collection_metadata(symbol=symbol)

                                    if collection_metadata:
                                        
                                        collection_creators = collection_metadata["creators"]
                                        collection_update_auth = collection_metadata["updateAuthority"]
                                        
                                        collection_identifier = "".join(collection_creators + [collection_update_auth])
                                        
                                        loaded_collections[collection_identifier] = symbol
                                        cached_collections[collection_identifier] = symbol
                                        
                                        sniper_start = True
                                else:
                                    
                                    collection_identifier = list(cached_collections.keys())[list(cached_collections.values()).index(symbol)]
                                    loaded_collections[collection_identifier] = symbol
                                                        
                            status = f"[SNIPER] [cyan][COLLECTIONS ~ {len(loaded_collections)}][/]"
                            
                            last_txs = get_account_last_txs(
                                account="hausS13jsjafwWwGqZTUQRmWyvyxn9EQpqMwV1PBBmk", 
                                limit=10, 
                                commitment="confirmed",
                                until=until_tx
                            )
                            
                            ready_to_purchase = False
                            
                            if last_txs:
                                
                                for tx in last_txs:
                                    
                                    signature = tx["signature"]
                                    
                                    if signature not in current_txs:

                                        current_txs.append(signature)
                                        
                                        console.print(logger(f"{status} [yellow]Fetching new data...[/]"))

                                        listing_info = coral_cube.check_tx_is_listing(tx=signature)
                                        
                                        if listing_info:
                                                                                    
                                            mint_address = listing_info["mint"]
                                            seller = listing_info["seller"]
                                            price_in_sol = lamports_to_sol(listing_info["price"])
                                            price_in_lamports = listing_info["price"]
                                            
                                            nft_metadata = get_nft_metadata(mint_key=mint_address)
                                            
                                            if nft_metadata:
                                                
                                                nft_name = nft_metadata["data"]["name"]
                                                nft_creators = nft_metadata["data"]["creators"]
                                                nft_update_auth = nft_metadata["update_authority"]
                                                
                                                to_match_identifier = "".join(nft_creators + [nft_update_auth])
                                                
                                                if to_match_identifier in loaded_collections.keys():
                                                                                                        
                                                    to_match_symbol = loaded_collections[to_match_identifier]
                                                    
                                                    matching_listing = False

                                                    for collection in sniper_data:
                                                        
                                                        if collection["Collection"] == to_match_symbol:
                                                            
                                                            min_sol = collection["MinPrice"]
                                                            max_sol = collection["MaxPrice"]
                                                            under_floor = collection["UnderFloor(%)"]
                                                            min_rank = collection["MinRank"]
                                                            max_rank = collection["MaxRank"]
                                                            autolist_by_price = collection["AutoListByPrice(%)"]
                                                            autolist_by_floor = collection["AutoListByFloor(%)"]
                                                            attributes = collection["Attributes"]
                                                            collection_floor = collection["Floor"]
                                                                
                                                            matching_listing = True
                                                            
                                                            break
                                                
                                                    if matching_listing:
                                                        
                                                        valid_listing = False
                                                        
                                                        if min_sol is not None and max_sol is not None:
                                                            
                                                            if min_sol <= price_in_sol <= max_sol:
                                                                
                                                                valid_listing = True
                                                                                                                        
                                                        elif under_floor is not None and collection_floor is not None:
                                                            
                                                            max_possible_price = collection_floor - (collection_floor * (under_floor/100))
                                                            
                                                            if price_in_sol <= max_possible_price:
                                                                
                                                                valid_listing = True
                                                                
                                                        if valid_listing:
                                                                                                                        
                                                            console.print(logger(f"{status} [yellow]Found possible NFT[/] [purple]>[/] [yellow]{nft_name}[/]"))
                                                            
                                                            if attributes or (min_rank is not None and max_rank is not None):
                                                                
                                                                nft_to_validate_data = CoralCube.get_nft_data(mint=mint_address)
                                                                
                                                                if nft_to_validate_data:
                                                                    
                                                                    is_valid_snipe = validate_cc_purchase_results(
                                                                        nft_to_validate_data, 
                                                                        filters=attributes,
                                                                        min_rank=min_rank,
                                                                        max_rank=max_rank
                                                                    )
                                                                    
                                                                    if is_valid_snipe:
                                                                        
                                                                        ready_to_purchase = True
                                                                        
                                                                        break
                                                                    
                                                                    else:
                                    
                                                                        console.print(logger(f"{status} [red]Rank or attributes do not match[/]"))
                                                                else:
                                                                    
                                                                    console.print(logger(f"{status} [red]Unable to get NFT data[/]"))
                                                            else:
                                                                
                                                                ready_to_purchase = True
                                                                
                                                                break
                                            else:
                                                
                                                console.print(logger(f"{status} [red]Unable to get NFT data (node)[/]"))
                                                
                                if len(current_txs) >= 500:

                                    current_txs = current_txs[-30:]

                                until_tx = last_txs[0]["signature"]
                                
                            elif last_txs is None:
                                    
                                console.print(logger(f"{status} [red]Unable to fetch new data (node)[/]"))
                                    
                            if ready_to_purchase:
                                                
                                console.print(logger(f"{status} [yellow]Sniped {nft_name}[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))
                                        
                                console.print(logger(f"{status} [yellow]Purchasing...[/]"))

                                tx_hash = coral_cube.buy_nft(
                                    seller=seller,
                                    mint=mint_address,
                                    price=price_in_lamports,
                                    creators=nft_creators
                                )

                                if tx_hash:

                                    console.print(logger(f"{status} [green]Purchased {nft_name}[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))

                                    if autolist_by_floor is not None or autolist_by_price is not None:
                                        
                                        listing_price = None
                                        
                                        if autolist_by_price is not None:

                                            listing_price = (price_in_sol + (price_in_sol * autolist_by_price/100))
                                                
                                        elif autolist_by_floor is not None and collection_floor:
                                                                                                
                                            listing_price = (collection_floor + (collection_floor * autolist_by_floor/100))
                                        
                                        if listing_price:
                                            
                                            listing_price = round(listing_price, 3)
                                            
                                            console.print(logger(f"{status} [yellow]Listing {nft_name}[/] [purple]>[/] [cyan]{listing_price} SOL[/]"))
                                            
                                            tx_hash = coral_cube.list_nft(
                                                seller=pubkey,
                                                mint=mint_address,
                                                price=sol_to_lamports(listing_price)
                                            )
                                            
                                            if tx_hash:
                                                                
                                                console.print(logger(f"{status} [green]Listed {nft_name}[/] [purple]>[/] [cyan]{listing_price} SOL[/]"))

                                            else:
                                                
                                                console.print(logger(f"{status} [red]Unable to list {nft_name}[/]"))
                                        
                                    break

                                else:

                                    console.print(logger(f"{status} [red]Purchase failed[/]"))
                
                    if kill_sniper:
                        
                        break
                
                kill_sniper = True
                        
                console.input(
                    "\n\n [purple]>>[/] Press ENTER to exit ", password=True)

                menu = True

                break

            clear()

        if mode == 11:
                        
            console.print(create_table_wallets(wallets))
            print()

            user_cmid = str(console.input(
                "[purple] >>[/] Mint URL: ")).strip()

            clear()

            if user_cmid.lower() == "e":

                break
        
        if mode == 12:
            
            if not valid_sol_rpc:

                console.input(
                    "[yellow] ERROR![/] [red]Invalid or unreachable RPC [/]", password=True)

                break
            
            check_node_health()                
                
            console.input("\n\n [purple]>>[/] Press ENTER to exit ", password=True)
            
            break
         
        if not menu:

            if mode in [1, 2, 4, 9, 11]:

                if mode == 4:

                    start = True

                elif mode in [1, 2, 9, 11]:
                    
                    if mode in [1, 9, 11]:

                        with console.status("[yellow]Validating Candy Machine ID[/]", spinner="bouncingBar", speed=1.5):
                            
                            if is_URL(url=user_cmid):
                                
                                if mode == 9:
                                    
                                    user_cmid = get_lmn_candy_machine(url=user_cmid)
                                
                                elif mode == 1:
                                    
                                    user_cmid = get_cmv2_candy_machine(url=user_cmid)
                                
                                elif mode == 11:
                                    
                                    user_cmid = get_ml_candy_machine(url=user_cmid)
                                    
                            if user_cmid:
                                
                                if mode in [1,9,11]:
                                        
                                    program = check_cmid(user_cmid["REACT_APP_CONFIG_KEY"] if mode == 11 else user_cmid)
                                    
                                    if program:
                                        
                                        if mode == 1 and program == SolanaPrograms.CMV2_PROGRAM:
                                            
                                            CM = user_cmid
                                            PROGRAM = program
                                            
                                        elif mode == 9 and program == SolanaPrograms.LMN_PROGRAM:

                                            CM = user_cmid
                                            PROGRAM = program
                                            
                                        elif mode == 11 and program == SolanaPrograms.ML_PROGRAM:
                                            
                                            CM = user_cmid
                                            PROGRAM = SolanaPrograms.ML_PROGRAM
                                    
                    if CM:

                        start = True

                    else:
                        
                        start = False
                        
                        clear()

                        console.print(
                            "[yellow] ERROR![/] [red]Invalid Candy Machine ID or mint not available[/]\n")

                if start:
                    
                    first_commit = False
                    
                    while True:

                        clear()

                        if wallets:

                            if mode in [1, 2, 9]:

                                with console.status(f"[yellow]Downloading candy machine data[/]", spinner="bouncingBar", speed=1.5):

                                    cm_metadata = asyncio.run(get_account_metadata("CandyMachine", CM, PROGRAM))
                                    
                                    if mode == 1:
                                        
                                        pda_account = get_collection_pda_account(cmid=CM)

                                        collection_set_metadata = asyncio.run(get_account_metadata("CollectionPDA", pda_account, PROGRAM))

                                    if cm_metadata:
                                        
                                        if mode in [1, 9]:

                                            DROP_TIME = int(cm_metadata.data.go_live_date)

                                    else:

                                        clear()

                                        console.print(
                                            "[red] ERROR![/] [yellow]Failed to fetch candy machine data\n[/]")

                                        break

                            elif mode == 11:
                                
                                DROP_TIME = int(CM["REACT_APP_CANDY_START_DATE"])
                                
                            trs = []

                            if user_time:

                                now = datetime.now().strftime("%H:%M:%S")
                                today_date = datetime.now().strftime("%Y-%m-%d")
                                
                                DROP_TIME = int(datetime.fromisoformat(f"{today_date}T{user_time}.000").timestamp())
                                
                                if user_time < now:
                                    
                                    DROP_TIME += 86400
                            
                            if first_commit:
                                
                                DROP_TIME = int(time.time())
                                
                            for wallet in wallets:

                                if wallet["tasks"]:

                                    mintT = Thread(target=mint, args=[wallet])
                                    mintT.start()
                                    trs.append(mintT)

                            for tr in trs:
                                tr.join()

                            if mode in [1, 2, 9, 11]:

                                print()
                                show_cm_status(cm=CM, program=PROGRAM)
                            
                            first_commit = True

                        else:

                            break

                        print("\n")

                        status = Prompt.ask(
                            "[purple]>>[/] Insert 'e' to exit or 'r' to retry mint", choices=["e", "r"])

                        print("\n")

                        if status == "e":

                            menu = True

                            break
