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
import asyncio
from dateutil import tz
import requests
from bs4 import BeautifulSoup
from base64 import b64decode
import borsh
from borsh import types as btypes
from dhooks import Embed, Webhook

from solana.rpc.api import Client
from solana.rpc import types
from solana.publickey import PublicKey
from solana.blockhash import Blockhash
from solana.rpc.commitment import Commitment

from modules import (
    CandyMachinev2,
    MagicEdenLaunchpad,
    MagicEden,
    FamousFox,
    LaunchMyNftLaunchpad,
    CoralCube,
    NeuraDB,
    MonkeLabsLaunchpad,
    SolWalletManager,
    BifrostAuth,
    BifrostLaunchpad
)

from utils.constants import Bot, Discord, SolanaPrograms, SolanaEndpoints, Keys
from utils.bot import logger, get_config, get_hwid, set_app_title
from utils.bypass import create_tls_payload, start_tls
from utils.solana import sol_to_lamports, lamports_to_sol, get_uri_metadata, get_nft_metadata, get_program_account_idl, get_pub_from_priv, get_wallet_balance, get_blockhash, get_last_account_txs


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

                    address = get_pub_from_priv(privkey)

                    if address:

                        try:

                            tasks = int(tasks) if int(tasks) > 0 else 0

                            if mode in [1, 2, 7, 9] and tasks:
                                    
                                """ if tasks > max_tasks:

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


def clear(newline: bool = True):

    if Bot.USER_OS == "darwin":

        os.system("clear")

    elif Bot.USER_OS == "win32":

        os.system('cls')

    if newline:

        print()

def mint(wallet: dict, recent_blockhash: Blockhash):

    name = wallet["name"]
    tasks = wallet["tasks"]
    privkey = wallet["privkey"]

    trs = []

    show_drop_time = datetime.fromtimestamp(DROP_TIME).strftime("%H:%M:%S")
            
    for i in range(tasks):
        
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

        if mode == 7:
            
            createtxT = Thread(
                target=send_lmn_tx,
                args=[privkey, sol_rpc, recent_blockhash, status],
                daemon=True
            )

        if mode == 9:
            
            createtxT = Thread(
                target=send_ml_tx,
                args=[privkey, sol_rpc, recent_blockhash, status],
                daemon=True
            )
            
        createtxT.start()
        trs.append(createtxT)
    
    for tr in trs:
        
        tr.join()


def send_cmv2_tx(privkey: str, rpc: str, blockhash: Blockhash, status: str):

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

    except Exception as e:
        
        print(e)
        
        console.print(logger(f"{status} [red]Error while creating tx (node)[/]\n"), end="")

        return
        
    simulated = True

    if advanced_mode:

        console.print(logger(f"{status} [yellow]Simulating transaction[/]\n"), end="")

        simulated = candy.simulate_transaction()
        
        if simulated:

            console.print(logger(f"{status} [yellow]Simulation successful[/]\n"), end="")

        else:
            
            console.print(logger(f"{status} [red]Simulation failed[/]\n"), end="")

    if simulated:
            
        console.print(logger(f"{status} [yellow]Sending transaction[/]\n"), end="")

        tx = candy.send_transaction()
    
        if tx:

            console.print(logger(f"{status} [green]Mint successful with hash: {tx}[/]\n"), end="")

            return

        elif tx is None:

            console.print(logger(f"{status} [red]Unable to confirm tx[/]\n"), end="")

        elif tx is False:
            
            console.print(logger(f"{status} [red]Error while sending tx[/]\n"), end="")
        

def send_ml_tx(privkey: str, rpc: str, blockhash: Blockhash, status: str):

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
    
    console.print(logger(f"{status} [yellow]Sending transaction[/]\n"), end="")

    tx = launchpad.send_transaction()

    if tx:

        console.print(logger(f"{status} [green]Mint successful with hash: {tx}[/]\n"), end="")

        return

    elif tx is None:

        console.print(logger(f"{status} [red]Unable to confirm tx[/]\n"), end="")

    elif tx is False:
        
        console.print(logger(f"{status} [red]Error while sending tx[/]\n"), end="")


def send_lmn_tx(privkey: str, rpc: str, blockhash: Blockhash, status: str):
    
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

    console.print(logger(f"{status} [yellow]Sending transaction[/]\n"), end="")

    tx = launchpad.send_transaction()

    if tx:

        console.print(logger(f"{status} [green]Mint successful with hash: {tx}[/]\n"), end="")

        return

    elif tx is None:

        console.print(logger(f"{status} [red]Unable to confirm tx[/]\n"), end="")

    elif tx is False:
        
        console.print(logger(f"{status} [red]Error while sending tx[/]\n"), end="")
                
        
def send_me_tx(privkey: str, rpc: str, blockhash: Blockhash, status: str):

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
    
    
    console.print(logger(f"{status} [yellow]Sending transaction[/]\n"), end="")
    
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

                console.print(logger(f"{status} [green]Mint successful with hash: {tx}[/]\n"), end="")
                
                return

            elif tx is None:

                console.print(logger(f"{status} [red]Unable to confirm tx[/]\n"), end="")
                
            elif tx is False:

                console.print(logger(f"{status} [red]Error while sending tx[/]\n"), end="")
        
        else:

            console.print(logger(f"{status} [red]Unable to sign tx[/]\n"), end="")

    else:

        console.print(logger(f"{status} [red]Error while signing tx[/]\n"), end="")


def send_sniper_webhook(mint: str, tx: str, price: float, sniping_time: float, webhook: str):
    
    nft_data = MagicEden.get_nft_data(mint=mint)
    
    if nft_data:
        
        name = nft_data["title"]
        img = nft_data["img"]
        url = f"https://magiceden.io/item-details/{mint}"
        tx_url = f"https://explorer.solana.com/tx/{tx}"
        
        embed = Embed(
            timestamp="now"
        )
        
        embed.color = Discord.EMBED_COLOR
        embed.description = "`SUCCESSFUL SNIPE`"
        
        embed.set_title(name, url)
        embed.set_thumbnail(img)
        embed.set_footer(Discord.EMBED_FOOTER_TXT, Discord.EMBED_FOOTER_IMG)
        
        embed.add_field("**Price**", f"{price} SOL", inline=False)
        #embed.add_field("**Speed**", f"{sniping_time} s", inline=False)
        embed.add_field("**Transaction**", f"[Explorer]({tx_url})", inline=False)
        
        try:
            
            Webhook(Discord.SUCCESS_WH).send(embed=embed)
            
            if webhook:
                
                Webhook(webhook).send(embed=embed)
            
        except:
            
            pass
 
            
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
        
    except:
        
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
        
        payload = create_tls_payload(
            url=url,
            method="GET",
            headers={}
        )
        
        res = requests.post("http://127.0.0.1:3000", json=payload, timeout=3).json()

        return res["statusCode"] == 200
    
    except:
        
        return False
    
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
                            "b": btypes.string,
                            "c": btypes.u32,
                            "d": btypes.u32,
                            "e": btypes.string,
                            "f": btypes.u16,
                            "g": btypes.fixed_array(btypes.u8, 32),
                            "h": btypes.fixed_array(btypes.u8, 32),
                            "i": btypes.u16,
                            "j": btypes.u64,
                            "k": btypes.fixed_array(btypes.u8, 32),
                            "l": btypes.u32,
                            "collectionKey": btypes.fixed_array(btypes.u8, 32),
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


def get_collection_pda_account(cmid: str):
    
    return str(PublicKey.find_program_address(
        seeds=[
            "collection".encode("utf-8"),
            bytes(PublicKey(cmid)),
        ],
        program_id=PublicKey(SolanaPrograms.CMV2_PROGRAM)
    )[0])


def wallet_is_holder(pubkey: str, hashlist: list):

    user_nfts = get_wallet_nfts(wallet=pubkey)
    
    if user_nfts:
        
        for nft in user_nfts:

            if nft in hashlist:

                return nft

    return False

def check_dc_token(token: str):
    
    try:
                
        headers = {
            'authorization': token
        }

        return requests.get("https://discord.com/api/v7/users/@me", headers=headers).json()
        
    except:
        
        return None

    

def get_local_time(_time: int):

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    utc = datetime.fromtimestamp(_time).replace(tzinfo=from_zone)
    return int(utc.astimezone(to_zone).timestamp())


def create_table_launchpad(collection: dict):

    global DROP_TIME
    
    _time = get_local_time(DROP_TIME)
    
    table = Table()

    table.add_column("NAME", justify="center", style="yellow")
    table.add_column("TIME (LOCAL)", justify="center", style="yellow")
    table.add_column("CANDY MACHINE ID",
                     justify="center", style="green")
    table.add_column("SUPPLY", justify="center", style="cyan")
    table.add_column("PRICE", justify="center", style="cyan")
    
    table.add_row(collection["name"], datetime.fromtimestamp(_time).strftime("%H:%M:%S"), collection["cmid"], str(collection["supply"]), str(lamports_to_sol(collection["price"])) + " SOL")

    return table


def validate_me_purchase_results(nft_data: dict, filters: dict, min_rank: int = None, max_rank: int = None):
    
    if filters:
        
        attributes = nft_data["attributes"]
        
        if attributes:
            
            nft_attributes = [{"trait_type": attribute["trait_type"].lower().strip(), "value": attribute["value"].lower().strip()} for attribute in attributes]

            wanted_attributes = [{"trait_type": attribute["trait_type"].lower().strip(), "value": attribute["value"].lower().strip()} for attribute in filters]        
            
            if not all(attr in nft_attributes for attr in wanted_attributes):
                    
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
            
            nft_attributes = [{"trait_type": attribute["trait_type"].lower().strip(), "value": attribute["value"].lower().strip()} for attribute in attributes]

            wanted_attributes = [{"trait_type": attribute["trait_type"].lower().strip(), "value": attribute["value"].lower().strip()} for attribute in filters]        
            
            if not all(attr in nft_attributes for attr in wanted_attributes):
                    
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

def get_me_highest_attribute_floor(collection_attributes: list, nft_attributes: list) -> int | None:
            
    highest_floor = 0

    for nattr in nft_attributes:
        
        for cattr in collection_attributes:
            
            if nattr == cattr["attribute"]:
                
                if cattr["floor"] > highest_floor:
                    
                    highest_floor = cattr["floor"]

    if highest_floor:
            
        return highest_floor

    return None

def check_marketplace_url(url):

    split_url = urlsplit(url)

    if "magiceden.io" in split_url.netloc:

        return "/marketplace/" in split_url.path and is_URL(url)

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
        
        nft_metadata = get_nft_metadata(mint_key=mint, rpc=sol_rpc)
        
        if nft_metadata:
            
            uri = nft_metadata["data"]["uri"]
            
            uri_metadata = get_uri_metadata(uri=uri)
                
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
        
        nft_metadata = get_nft_metadata(mint_key=mint, rpc=sol_rpc)
        
        if nft_metadata:
            
            uri = nft_metadata["data"]["uri"]
            
            uri_metadata = get_uri_metadata(uri=uri)
                
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

                            filtered_attributes.append({"trait_type": trait, "value": value})
                        
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

                            filtered_attributes.append({"trait_type": trait, "value": value})
                        
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


def get_drop_time():

    if PROGRAM in [SolanaPrograms.CMV2_PROGRAM, SolanaPrograms.LMN_PROGRAM]:

        meta = asyncio.run(get_program_account_idl("CandyMachine", CM, PROGRAM, sol_rpc))

        return int(meta.data.go_live_date)

    elif PROGRAM == SolanaPrograms.ME_PROGRAM:

        collection = MagicEdenLaunchpad.get_collection_info(collection_url)

        return collection["date"] if collection else None

    elif PROGRAM == SolanaPrograms.ML_PROGRAM:
        
        return int(CM["REACT_APP_CANDY_START_DATE"])
    

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
                
                console.print(logger(f"[BOT] [yellow]Found time reschedule to {show_new_time}[/]\n"), end="")



def wait_for_mints():
        
    while True:
        
        current_minted = None
        
        if mode in [1,2,7]:
                
            metadata = asyncio.run(get_program_account_idl("CandyMachine", CM, PROGRAM, sol_rpc))   
            
            if metadata:
                
                if PROGRAM in [SolanaPrograms.CMV2_PROGRAM, SolanaPrograms.LMN_PROGRAM]:
                    
                    current_minted = metadata.items_redeemed
                    
                elif PROGRAM == SolanaPrograms.ME_PROGRAM:
                    
                    current_minted = metadata.items_redeemed_normal
                
        elif mode == 9:
            
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
        
        for wallet in wallets:

            balance = get_wallet_balance(wallet["address"], sol_rpc)

            table.add_row(wallet["name"], wallet["address"], str(wallet["tasks"]), str(round(lamports_to_sol(balance), 2)))

        return table


def get_cm_mints_status(cm: str | dict, program: str):

    available = redeemed = None
    
    if program in [SolanaPrograms.CMV2_PROGRAM, SolanaPrograms.ME_PROGRAM, SolanaPrograms.LMN_PROGRAM]:
            
        metadata = asyncio.run(get_program_account_idl(
            "CandyMachine",
            account=cm,
            prog=program,
            rpc=sol_rpc
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
        
    elif program == SolanaPrograms.ML_PROGRAM:
        
        available = int(cm["REACT_APP_INDEX_CAP"])
        redeemed = get_ml_items_redeemed(index_key=cm["REACT_APP_INDEX_KEY"])
        
    if available and redeemed:
            
        minted = int((redeemed/available) * 100)

        return available, redeemed, minted
    

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

                return None

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

                return None

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

            wallet = console.input("[purple] >>[/] Select wallet to transfer: ")

            if wallet == "e":

                return None

            wallet = int(wallet)

            if wallet in range(0, len(wallets_nfts)):

                return wallet

        except:

            pass

        console.print("[red]    Invalid wallet provided[/]")


def get_listing_price():

    while True:

        price = console.input("[purple] >>[/] Insert a price for listing: ")

        try:

            if price == "e":

                return None

            return float(price)

        except ValueError:

            pass

        console.print("[red]    Invalid price provided[/]")


def show_selected_nfts():

    for i, wallet in enumerate(wallets_nfts):

        wallet_address = wallet["address"]
        wallet_nfts = wallet["nfts"]
        wallet_balance = wallet["balance"]

        console.print("[purple] >>[/] {:<10} [green]{}[/]\n".format(f"Wallet {i}:", wallet_address))

        console.print("[purple]  >[/] {:<10} [cyan]{}[/]\n".format(f"Balance:", round(lamports_to_sol(wallet_balance), 2)))

        if wallet_nfts:

            for j, nft in enumerate(wallet_nfts):

                nft_name = nft["name"]

                if i in wallets_to_operate and j in raw_wallets_nfts[i]:

                    if operation_type in ["l", "ts", "tn", "b"]:
                        
                        console.print("[purple]  >[/] {:<10} [yellow]{}[/]".format(f"NFT {j}:", f"[purple]> [/]{nft_name}"))
                    
                    elif operation_type in ["d", "u"]:

                        console.print("[purple]  >[/] {:<10} [yellow]{}[/] [cyan]{}[/]".format(f"NFT {j}:", f"[purple]> [/]{nft_name}", nft["price"]))
                        
                else:
                    
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

    options = list(range(1, 11))

    while True:

        try:

            mode = int(console.input("[purple] >>[/] Select a module to use: "))

            if mode in options:

                return mode

        except ValueError:

            pass

        except KeyboardInterrupt:

            exit(0)

        console.print("[red]    Invalid option provided[/]")




set_app_title(f"Neura - {Bot.VERSION}")
console = Console(highlight=False, log_path=False)

try:
    
    import helheim
    
    helheim.auth(Keys.CF_API_KEY)
    
    helheim_auth = True
    
except:
    
    helheim_auth = True
    

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

    if Bot.USER_OS == "darwin":
        
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

                        console.input("[yellow] ERROR![/] [red]Invalid or already in use beta key [/]", password=True)

                else:
                        
                    neura_hashlist = database.get_column_data("holders", "nft")

                    if neura_hashlist:
                        
                        holder_pubkey = get_pub_from_priv(nft_holder)

                        if holder_pubkey:
                            
                            holder_nft = wallet_is_holder(pubkey=holder_pubkey, hashlist=neura_hashlist)

                            if holder_nft:

                                access = database.check_holder_access(holder_nft, holder_pubkey, user_hwid)

                                if access:

                                    break

                                else:
                                    
                                    console.input("[yellow] ERROR![/] [red]Provided Neura NFT pass is already in use [/]", password=True)

                            else:
                                console.input("[yellow] ERROR![/] [red]Provided holder wallet has no Neura NFT pass [/]", password=True)
                        else:

                            console.input("[yellow] ERROR![/] [red]Invalid holder wallet provided[/]", password=True)
                            
                    else:

                        console.input("[yellow] ERROR![/] [red]Neura database is unreachable, please contact support [/]", password=True)
            else:
                console.input("[yellow] ERROR![/] [red]Unable to connect with the Nuera database, please restart and if the problem persists, contact Neura support [/]", password=True)
        else:
            console.input("[yellow] ERROR![/] [red]Invalid holder private key or beta access code [/]", password=True)

    else:
        console.input("[yellow] ERROR![/] [red]Unable to get device info, please contact support[/]", password=True)

database.close_connection()

while True:

    clear()

    try:
        
        start_tls()

        break

    except:

        console.input("[yellow] ERROR![/] [red]Some of the Neura config files are missing, please contact support [/]", password=True)

    
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
    await_mints = get_config(parameter="await_mints")
    success_webhook = get_config(parameter="webhook")
    
    max_tasks = 1000
    min_tasks = 500
    
    valid_sol_rpc = validate_sol_rpc(rpc=sol_rpc)
    
    menu = False

    show_banner()

    if sol_rpc and valid_sol_rpc:

        console.print(" {:<10} [green]{:<5}[/] [purple]> [/]{}".format("SOL RPC:", "ON", f"{sol_rpc} [purple]>[/] {valid_sol_rpc} ms"))

    else:

        console.print(" {:<10} [red]OFF[/]".format("SOL RPC:"))

    if user_time:

        show_user_time = datetime.fromtimestamp(user_time).strftime("%H:%M:%S")
        
        console.print(" {:<10} [green]{:<5}[/] [purple]> [/]{}".format("Time:", "ON", show_user_time))

    else:

        console.print(" {:<10} [red]OFF[/]".format("Time:"))
    
    print()

    console.print("[cyan] [1][/] CandyMachine mint")
    console.print("[cyan] [2][/] MagicEden mint")
    console.print("[cyan] [3][/] MagicEden sniper")
    console.print("[cyan] [4][/] SOL wallets manager")
    console.print("[cyan] [5][/] MagicEden sweeper")
    console.print("[cyan] [6][/] FamousFox sniper")
    console.print("[cyan] [7][/] LaunchMyNFT mint")
    console.print("[cyan] [8][/] CoralCube sniper")
    console.print("[cyan] [9][/] MonkeLabs mint")
    console.print("[cyan] [10][/] Bifrost mint")
    console.print("[cyan] [11][/] Node health checker\n")
    
    mode = get_module()

    clear()

    while True:

        if menu:

            break

        wallets = get_sol_wallets()

        if not wallets:

            console.input("[yellow] ERROR![/] [red]Invalid wallets data / No wallets loaded [/]", password=True)

            break

        if not valid_sol_rpc:

            console.input("[yellow] ERROR![/] [red]Invalid or unreachable RPC [/]", password=True)

            break
    
            
        if mode == 1:

            console.print(create_table_wallets(wallets))
            print()

            user_cmid = str(console.input("[purple] >>[/] Candy Machine ID: ")).strip()

            clear()

            if user_cmid.lower() == "e":

                break

        if mode == 2:

            while True:
                
                if helheim_auth:
                        
                    console.print(create_table_wallets(wallets))
                    print()

                    collection_url = str(console.input("[purple] >>[/] MagicEden launchpad collection URL: ")).lower()
                    clear()

                    if collection_url == "e":
                        menu = True
                        break

                    with console.status("[yellow]Searching for collection[/]", spinner="bouncingBar", speed=1.5):

                        collection = MagicEdenLaunchpad.get_collection_info(collection_url)

                    if collection:

                        CM = collection["cmid"]
                        PROGRAM = SolanaPrograms.ME_PROGRAM
                        DROP_TIME = collection["date"]
                        
                        console.print(create_table_launchpad(collection))
                        print()

                        proceed = Prompt.ask("[purple] >>[/] Start mint?", choices=["y", "n"])
                        clear()

                        if proceed == "y":

                            break

                    else:
                        
                        console.print("[yellow] ERROR![/] [red]Collection not found\n [/]")
                        
                else:
                    
                    console.input("[yellow] ERROR![/] [red]MagicEden launchpad unavailable [/]", password=True)
                    
                    menu = True
                    
                    break
                                  
        if mode == 3:

            console.print(create_table_wallets(wallets))
            print()
            
            wallet_choices = [wallet["name"].lower() for wallet in wallets] + ["e"]

            selected_wallet = Prompt.ask("[purple] >>[/] Choose sniper wallet", choices=wallet_choices)

            if selected_wallet == "e":

                break

            wallet = [wallet for wallet in wallets if selected_wallet == wallet["name"].lower()][0]

            clear()
                        
            console.print(create_table_wallets([wallet]))

            print()
            
            start_sniper = Prompt.ask("[purple] >>[/] Are you sure you want to continue? This will start the sniper instantly", choices=["y", "n"])
            
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
                            
                            last_txs = get_last_account_txs(
                                rpc=sol_rpc,
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

                                        start_time = time.time()
                                        
                                        listing_info = magic_eden.check_tx_is_listing(tx=signature)
                                                                                
                                        if listing_info:
                                            
                                            mint_address = listing_info["mint"]
                                            seller = listing_info["seller"]
                                            price_in_sol = lamports_to_sol(listing_info["price"])
                                            price_in_lamports = listing_info["price"]
                                            escrow_pubkey = listing_info["escrow"]
                                            
                                            nft_metadata = get_nft_metadata(mint_key=mint_address, rpc=sol_rpc)
                                            
                                            if nft_metadata:
                                                
                                                nft_name = nft_metadata["data"]["name"]
                                                nft_creators = nft_metadata["data"]["creators"]
                                                nft_update_auth = nft_metadata["update_authority"]
                                                nft_uri = nft_metadata["data"]["uri"]
                                                
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
                                                                
                                                                nft_marketplace_data = CoralCube.get_nft_data(mint=mint_address)
                                                                
                                                                if nft_marketplace_data:
                                                                    
                                                                    is_valid_snipe = validate_cc_purchase_results(
                                                                        nft_marketplace_data, 
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

                                final_time = time.time()
                                
                                sniping_time = round(final_time - start_time, 1)
                                
                                tx_hash = magic_eden.buy_nft_api(
                                    seller=seller,
                                    price=price_in_lamports,
                                    mint=mint_address
                                )

                                if tx_hash:

                                    console.print(logger(f"{status} [green]Purchased {nft_name}[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))
                                    
                                    send_sniper_webhook(
                                        mint=mint_address,
                                        tx=tx_hash,
                                        price=price_in_sol,
                                        sniping_time=sniping_time,
                                        webhook=success_webhook or None
                                    )
                                    
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

            while True:
                    
                wallets_nfts = []

                operation_type = Prompt.ask("[purple] >>[/] What would you like to do?", choices=["l", "d", "u", "ts", "tn", "b", "e"])

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
                        
                        balance = get_wallet_balance(wallet["address"], sol_rpc)

                        nfts_data = []

                        for nft in wallet_nfts:
                                                        
                            if operation_type in ["l", "ts", "tn", "b"]:

                                if nft.get("collectionName") or nft["onChainCollection"].get("key"):
                                    
                                    nfts_data.append({"mint": nft["mintAddress"], "name": nft["title"], "token": nft["id"], "symbol": nft.get("collectionName") or nft["onChainCollection"].get("key"), "attributes": nft["attributes"]})

                            elif operation_type in ["d", "u"]:

                                nfts_data.append({"mint": nft["initializerDepositTokenMintAddress"], "name": nft["title"], "token": nft["initializerDepositTokenAccount"], "price": lamports_to_sol(nft["takerAmount"]), "attributes": nft["attributes"], "symbol": nft.get("collectionSymbol") or nft.get("onChainCollectionAddress")})
                            
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

            if operation_type == "e":

                break
            
            for i, wallet in enumerate(wallets_nfts):

                wallet_address = wallet["address"]
                wallet_nfts = wallet["nfts"]
                wallet_balance = wallet["balance"]

                console.print("[purple] >>[/] {:<10} [green]{}[/]\n".format(f"Wallet {i}:", wallet_address))

                console.print("[purple]  >[/] {:<10} [cyan]{}[/]\n".format(f"Balance:", round(lamports_to_sol(wallet_balance), 2)))

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

                wallets_to_operate = get_range_to_operate(operation="wallets")

                if wallets_to_operate is None:

                    break

                for i in wallets_to_operate:

                    nfts_to_operate = get_range_to_operate(operation="nfts", wallet_to_operate=i)

                    raw_wallets_nfts[i] = nfts_to_operate

                    if nfts_to_operate is None:

                        break

                if nfts_to_operate is None:

                    break

                clear()

                show_selected_nfts()

                print()

                if operation_type in ["l", "u"]:

                    listing_price = get_listing_price()

                    if listing_price is None:

                        break
                    
                    list_by_trait = listing_price == 0.0

                elif operation_type in ["d", "b"]:
                    
                    if operation_type == "d":
                        
                        console.input("[purple] >>[/] Press ENTER to continue with the delisting process ", password=True)
                        
                    elif operation_type == "b":
                        
                        console.input("[purple] >>[/] Press ENTER to continue with the burn process ", password=True)
                        
                elif operation_type == "tn":

                    wallet_to_transfer = get_wallet_to_transfer()

                    if wallet_to_transfer is None:

                        break

                clear()

                trs = []

                current_collection = None
                collection_attributes = None
                
                for wallet, nfts in raw_wallets_nfts.items():

                    privkey = wallets_nfts[wallet]["privkey"]

                    me_manager = MagicEden(
                        rpc=sol_rpc,
                        privkey=privkey
                    )
                    
                    wallet_manager = SolWalletManager(
                        rpc=sol_rpc,
                        privkey=privkey
                    )
                    
                    for nft in nfts:

                        nft_data = wallets_nfts[wallet]["nfts"][nft]

                        name = nft_data["name"]
                        mint_address = nft_data["mint"]
                        token = nft_data["token"]
                        
                        if operation_type in ["l", "u"]:
                            
                            symbol = nft_data["symbol"]
                            attributes = nft_data["attributes"]
                            
                            if list_by_trait:
                                
                                listing_price = 0
                                
                                if symbol != current_collection:
                                    
                                    collection_attributes = MagicEden.get_collection_attributes(symbol)
                                    
                                if collection_attributes:
                                    
                                    highest_attribute_floor = get_me_highest_attribute_floor(collection_attributes, attributes)
                                    
                                    if highest_attribute_floor:
                                        
                                        listing_price = lamports_to_sol(highest_attribute_floor)
                                    
                            if operation_type == "l":

                                console.print(logger(f"[MANAGER] [cyan][OPERATION ~ List][/] [yellow]Listing {name} at {listing_price} SOL[/]"))

                            elif operation_type == "u":

                                console.print(logger(f"[MANAGER] [cyan][OPERATION ~ Update][/] [yellow]Updating {name} price to {listing_price} SOL[/]"))
                            
                            operationT = Thread(
                                target=me_manager.list_nft,
                                args=[mint_address, sol_to_lamports(listing_price)]
                            )

                        elif operation_type == "d":

                            delisting_price = nft_data["price"]

                            console.print(logger(f"[MANAGER] [cyan][OPERATION ~ Delist][/] [yellow]Delisting {name}[/]"))
                            
                            operationT = Thread(
                                target=me_manager.delist_nft,
                                args=[mint_address, sol_to_lamports(delisting_price)]
                            )

                        elif operation_type == "tn":

                            dest_wallet = wallets_nfts[wallet_to_transfer]["address"]
                            dest_name = wallets_nfts[wallet_to_transfer]["name"]

                            console.print(logger(f"[MANAGER] [cyan][OPERATION ~ Transfer NFT][/] [yellow]Transfering {name} to {dest_name.upper()}[/]"))

                            operationT = Thread(
                                target=wallet_manager.transfer_nft,
                                args=[mint_address, dest_wallet]
                            )

                        elif operation_type == "b":
                            
                            console.print(logger(f"[MANAGER] [cyan][OPERATION ~ Burn][/] [yellow]Burning {name}[/]"))
                            
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

                wallets_to_operate = get_range_to_operate(operation="wallets")

                if wallets_to_operate is None:

                    break

                for i in wallets_to_operate:

                    balance_to_operate = get_balance_to_transfer(i)

                    raw_wallets_balances[i] = balance_to_operate

                    if balance_to_operate is None:

                        break

                if balance_to_operate is None:

                    break
                
                wallet_to_transfer = get_wallet_to_transfer()

                if wallet_to_transfer is None:

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
        
        if mode == 5:
            
            console.print(create_table_wallets(wallets))
            print()
            
            wallet_choices = [wallet["name"].lower() for wallet in wallets] + ["e"]

            selected_wallet = Prompt.ask("[purple] >>[/] Choose sweeper wallet", choices=wallet_choices)

            if selected_wallet == "e":

                break

            wallet = [wallet for wallet in wallets if selected_wallet == wallet["name"].lower()][0]

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
                    
                    clear()
                    
                    console.print(create_table_wallets([wallet]))
                    
                    print()
                    
                    start_sweeper = Prompt.ask("[purple] >>[/] Are you sure you want to continue? This will start the sweeper instantly", choices=["y", "n"])
                        
                    print()
                    
                    if start_sweeper == "y":
                        
                        privkey = wallet["privkey"]
                        
                        console.print(logger(f"[SWEEPER] [cyan][{symbol.upper()}][/] [yellow]Loading file data and initialazing...[/]"))

                        while True:
                            
                            sweeper_data = get_sweeper_data(file_name="me-sweeper")
                            
                            if sweeper_data:
                                
                                break

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
                        
                        attributes = [{"trait_type": key, "value": value} for key, value in sweeper_data.items() if value and key in collection_attributes]
                        
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

                    console.print("[yellow] ERROR![/] [red]Invalid collection URL\n[/]")
                    
        if mode == 6:
            
            console.print(create_table_wallets(wallets))
            print()
            
            wallet_choices = [wallet["name"].lower() for wallet in wallets] + ["e"]

            selected_wallet = Prompt.ask("[purple] >>[/] Choose sniper wallet", choices=wallet_choices)

            if selected_wallet == "e":

                break

            wallet = [wallet for wallet in wallets if selected_wallet == wallet["name"].lower()][0]

            clear()

            while True:

                console.print(create_table_wallets([wallet]))
                print()

                token_mint = str(console.input("[purple] >>[/] WhiteList token address: ")).strip()
                clear()

                if token_mint == "e":
                    
                    menu = True
                    
                    break

                with console.status("[yellow]Downloading token data[/]", spinner="bouncingBar", speed=1.5):
                    
                    valid_token = check_spl_token(token_mint=token_mint)    
                    

                if valid_token:
                    
                    clear()
                
                    console.print(create_table_wallets([wallet]))
                    
                    print()
                    
                    start_sniper = Prompt.ask("[purple] >>[/] Are you sure you want to continue? This will start the sniper instantly", choices=["y", "n"])
                    
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

                                    last_txs = get_last_account_txs(
                                        rpc=sol_rpc,
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

                    console.print("[yellow] ERROR![/] [red]Invalid WhiteList token\n[/]")

        if mode == 7:
            
            console.print(create_table_wallets(wallets))
            print()

            user_cmid = str(console.input("[purple] >>[/] Candy Machine ID: ")).strip()

            clear()

            if user_cmid.lower() == "e":

                break
        
        if mode == 8:

            console.print(create_table_wallets(wallets))
            print()
            
            wallet_choices = [wallet["name"].lower() for wallet in wallets] + ["e"]

            selected_wallet = Prompt.ask("[purple] >>[/] Choose sniper wallet", choices=wallet_choices)

            if selected_wallet == "e":

                break

            wallet = [wallet for wallet in wallets if selected_wallet == wallet["name"].lower()][0]

            clear()
            
            console.print(create_table_wallets[wallet])       

            start_sniper = Prompt.ask("[purple] >>[/] Are you sure you want to continue? This will start the sniper instantly", choices=["y", "n"])
            
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
                            
                            last_txs = get_last_account_txs(
                                rpc=sol_rpc,
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

                                        start_time = time.time()
                                        
                                        listing_info = coral_cube.check_tx_is_listing(tx=signature)
                                        
                                        if listing_info:
                                                                                    
                                            mint_address = listing_info["mint"]
                                            seller = listing_info["seller"]
                                            price_in_sol = lamports_to_sol(listing_info["price"])
                                            price_in_lamports = listing_info["price"]
                                            
                                            nft_metadata = get_nft_metadata(mint_key=mint_address, rpc=sol_rpc)
                                            
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
                                                                
                                                                nft_marketplace_data = CoralCube.get_nft_data(mint=mint_address)
                                                                
                                                                if nft_marketplace_data:
                                                                    
                                                                    is_valid_snipe = validate_cc_purchase_results(
                                                                        nft_marketplace_data, 
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
                                
                                final_time = time.time()
                                
                                sniping_time = round(final_time - start_time, 1)
                                
                                tx_hash = coral_cube.buy_nft(
                                    seller=seller,
                                    mint=mint_address,
                                    price=price_in_lamports,
                                    creators=nft_creators
                                )

                                if tx_hash:

                                    console.print(logger(f"{status} [green]Purchased {nft_name}[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))

                                    send_sniper_webhook(
                                        mint=mint_address,
                                        tx=tx_hash,
                                        price=price_in_sol,
                                        sniping_time=sniping_time,
                                        webhook=success_webhook or None
                                    )
                                    
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

        if mode == 9:
                        
            console.print(create_table_wallets(wallets))
            print()

            user_cmid = str(console.input("[purple] >>[/] Mint URL: ")).strip()

            clear()

            if user_cmid.lower() == "e":

                break
        
        if mode == 10:
            
            while True:
                
                console.print(create_table_wallets(wallets))
                print()

                collection_url = str(console.input("[purple] >>[/] Bifrost launchpad collection URL: ")).lower()
                clear()

                if collection_url == "e":
                    menu = True
                    break

                with console.status("[yellow]Searching for collection[/]", spinner="bouncingBar", speed=1.5):

                    collection = BifrostLaunchpad.get_collection_info(url=collection_url)

                if collection:

                    CM = collection["cmid"]
                    PROGRAM = SolanaPrograms.BF_PROGRAM
                    DROP_TIME = collection["date"]
                    
                    console.print(create_table_launchpad(collection))
                    print()

                    proceed = Prompt.ask("[purple] >>[/] Start Discord login?", choices=["y", "n"])
                    clear()

                    if proceed == "y":

                        break

                else:
                    
                    console.print("[yellow] ERROR![/] [red]Collection not found\n [/]")
        
        if mode == 11:
            
            if not valid_sol_rpc:

                console.input("[yellow] ERROR![/] [red]Invalid or unreachable RPC [/]", password=True)

                break
            
            check_node_health()                
                
            console.input("\n\n [purple]>>[/] Press ENTER to exit ", password=True)
            
            break
         
        if not menu:

            if mode in [1, 2, 7, 9]:

                if mode in [1, 7, 9]:

                    with console.status("[yellow]Validating Candy Machine ID[/]", spinner="bouncingBar", speed=1.5):
                        
                        if is_URL(url=user_cmid):
                            
                            if mode == 7:
                                
                                user_cmid = get_lmn_candy_machine(url=user_cmid)
                            
                            elif mode == 1:
                                
                                user_cmid = get_cmv2_candy_machine(url=user_cmid)
                            
                            elif mode == 9:
                                
                                user_cmid = get_ml_candy_machine(url=user_cmid)
                                
                        if user_cmid:
                                                   
                            program = check_cmid(user_cmid["REACT_APP_CONFIG_KEY"] if mode == 9 else user_cmid)
                            
                            if program:
                                
                                if mode == 1 and program == SolanaPrograms.CMV2_PROGRAM:
                                    
                                    CM = user_cmid
                                    PROGRAM = program
                                    
                                elif mode == 7 and program == SolanaPrograms.LMN_PROGRAM:

                                    CM = user_cmid
                                    PROGRAM = program
                                    
                                elif mode == 9 and program == SolanaPrograms.ML_PROGRAM:
                                    
                                    CM = user_cmid
                                    PROGRAM = SolanaPrograms.ML_PROGRAM
                                    
                if CM:

                    start = True

                else:
                    
                    start = False
                    
                    clear()

                    console.print("[yellow] ERROR![/] [red]Invalid Candy Machine ID or mint not available[/]\n")

                if start:
                    
                    first_commit = False
                    
                    while True:

                        clear()

                        if mode in [1, 2, 7]:

                            with console.status(f"[yellow]Downloading candy machine data[/]", spinner="bouncingBar", speed=1.5):

                                cm_metadata = asyncio.run(get_program_account_idl("CandyMachine", CM, PROGRAM, sol_rpc))
                                
                                if mode == 1:
                                    
                                    pda_account = get_collection_pda_account(cmid=CM)

                                    collection_set_metadata = asyncio.run(get_program_account_idl("CollectionPDA", pda_account, PROGRAM, sol_rpc))

                                if cm_metadata:
                                    
                                    if mode in [1, 7]:

                                        DROP_TIME = int(cm_metadata.data.go_live_date)

                                else:

                                    clear()

                                    console.print("[red] ERROR![/] [yellow]Failed to fetch candy machine data\n[/]")

                                    break

                        elif mode == 9:
                            
                            DROP_TIME = int(CM["REACT_APP_CANDY_START_DATE"])
                            
                        trs = []

                        if user_time:

                            DROP_TIME = user_time
                        
                        if first_commit:
                            
                            DROP_TIME = int(time.time())

                        show_drop_time = datetime.fromtimestamp(DROP_TIME).strftime("%H:%M:%S")
                        
                        console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Initialazing mint[/]\n".format("ALL", "INIT", show_drop_time)), end="")

                        if mode != 9 or user_time:

                            console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Awaiting for drop time[/]\n".format("ALL", "INIT", show_drop_time)), end="")

                            wait_for_drop(exit_before=3)
                        
                        elif await_mints:
                            
                            console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Awaiting for mints[/]\n".format("ALL", "INIT", show_drop_time)), end="")
                            
                            wait_for_mints()
                            
                        while True:

                            recent_blockhash = get_blockhash(sol_rpc)

                            if recent_blockhash:
                                
                                console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Initialazing transactions[/]\n".format("ALL", "INIT", show_drop_time)), end="")
                                
                                break
                            
                            else:

                                console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [red]Unable to initialize txs (node)[/]\n".format("ALL", "INIT", show_drop_time)), end="")
                                
                        if mode != 9 or user_time:
                            
                            wait_for_drop()

                        for wallet in wallets:

                            mintT = Thread(target=mint, args=[wallet, recent_blockhash])
                            mintT.start()
                            trs.append(mintT)

                        for tr in trs:
                            tr.join()

                        print()
                        
                        mints_status = get_cm_mints_status(CM, PROGRAM)
                        
                        if mints_status:
                                
                            available, redeemed, minted = mints_status
                            
                            console.print(f"[AVAILABLE ~ [green]{available}[/]] [REDEEMED ~ [yellow]{redeemed}[/]] [MINTED ~ [cyan]{minted}%[/]]\n")
                            
                        first_commit = True

                        print("\n")

                        status = Prompt.ask("[purple]>>[/] Insert 'e' to exit or 'r' to retry mint", choices=["e", "r"])

                        print("\n")

                        if status == "e":

                            menu = True

                            break

            elif mode in [10]:
                
                pass
                #user_dc_data = check_dc_token(token=dc_auth_token)


