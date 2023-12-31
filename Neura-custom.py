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
import websocket

from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.blockhash import Blockhash

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
    BifrostLaunchpad,
    ExchangeArt
)

from utils.constants import Bot, Custom, Discord, SolanaPrograms, SolanaEndpoints, Keys, IDLs
from utils.bot import logger, get_config, get_hwid, set_app_title
from utils.bypass import create_tls_payload, start_tls

from utils.solana import (
    sol_to_lamports, 
    lamports_to_sol, 
    get_uri_metadata, 
    get_nft_metadata, 
    get_program_account_idl, 
    get_pub_from_priv, 
    get_wallet_balance, 
    get_blockhash, 
    get_last_account_txs,
    get_wallet_nfts,
    get_websocket_url
)


def get_sol_wallets():

    wallets = []

    try:

        with open('sol-wallets.csv', 'r') as f:
                
            reader = csv.DictReader(f)

            for wallet in reader:

                privkey = wallet["privateKey"]
                name = wallet["name"]
                tasks = wallet["tasks"]
                
                name = name if len(name) <= 9 else name[:9]
                tasks = int(tasks) if int(tasks) > 0 else 0
                address = get_pub_from_priv(privkey)
                        
                if address:

                    wallets.append(

                        {
                            "name": name.upper(),
                            "address": address,
                            "privkey": privkey,
                            "tasks": tasks
                        }

                    )

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

def mint(wallet: dict):

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
                args=[privkey, mint_rpc, recent_blockhash, status],
                daemon=True
            )

        if mode == 2:

            createtxT = Thread(
                target=send_me_tx,
                args=[privkey, mint_rpc, recent_blockhash, status],
                daemon=True
            )

        if mode == 7:
            
            createtxT = Thread(
                target=send_lmn_tx,
                args=[privkey, mint_rpc, recent_blockhash, status],
                daemon=True
            )

        if mode == 9:
            
            createtxT = Thread(
                target=send_ml_tx,
                args=[privkey, mint_rpc, recent_blockhash, status],
                daemon=True
            )
        
        if mode == 10:
            
            createtxT = Thread(
                target=send_bf_tx,
                args=[privkey, mint_rpc, max_price, status],
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

    except:
                
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


def send_bf_tx(privkey: str, rpc: str, max_price: float, status: str):

    bf_launchpad = BifrostLaunchpad(
        bf_auth=bf_auth_session,
        privkey=privkey
    )
    
    console.print(logger(f"{status} [yellow]Sending transaction[/]\n"), end="")
    
    raw_txs = bf_launchpad.get_transactions(
        cmid=CM,
        token_bonding=token_bonding,
        max_price=max_price
    )
    
    if raw_txs:
        
        signed_txs = bf_launchpad.sign_transactions(raw_txs)
        
        if signed_txs:
            
            tx_hash = bf_launchpad.send_transactions(signed_txs)
            
            if tx_hash:
                
                console.print(logger(f"{status} [green]Mint successful[/]\n"), end="")

            else:
                
                console.print(logger(f"{status} [red]Unable to confirm tx[/]\n"), end="")
        else:
            
            console.print(logger(f"{status} [red]Error while signing tx[/]\n"), end="")    
    
    else:
        
        console.print(logger(f"{status} [red]Error while sending tx[/]\n"), end="")
        

def send_ea_tx(privkey: str, rpc: str, blockhash: Blockhash, edition_no: int, status: str):

    exchange = ExchangeArt(
        privkey=privkey,
        rpc=rpc,
        contract=collection
    )
    
    mint_info = exchange.get_hmac_code()
    
    if mint_info:
            
        timestamp = mint_info["timestamp"]
        hmac_code = mint_info["hmacCode"]

        try:
            
            exchange.create_transaction(timestamp, hmac_code, edition_no)
            
            exchange.transaction.recent_blockhash = blockhash
        
        except:
                        
            console.print(logger(f"{status} [red]Error while creating tx (node)[/]\n"), end="")
            
            return

        console.print(logger(f"{status} [yellow]Sending transaction[/]\n"), end="")
        
        tx = exchange.send_transaction()
        
        if tx:

            console.print(logger(f"{status} [green]Mint successful with hash: {tx}[/]\n"), end="")
            
            return

        elif tx is None:

            console.print(logger(f"{status} [red]Unable to confirm tx[/]\n"), end="")
            
        elif tx is False:

            console.print(logger(f"{status} [red]Error while sending tx[/]\n"), end="")
    else:
        
        console.print(logger(f"{status} [red]Error while getting mint info[/]\n"), end="")
    
    
        
def send_sniper_webhook(mint: str, tx: str, price: float, webhook: str):
    
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
        embed.add_field("**Transaction**", f"[Explorer]({tx_url})", inline=False)
        
        try:
            
            Webhook(Discord.SUCCESS_WH).send(embed=embed)
            
            Webhook(webhook).send(embed=embed)
            
        except:
            
            pass
 
            
def check_cmid(cmid: str):
    
    global CM
    
    try:
        
        client = Client(mint_rpc)
        
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
                        
                        client = Client(mint_rpc)
                        
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




def get_collection_pda_account(cmid: str):
    
    return str(PublicKey.find_program_address(
        seeds=[
            "collection".encode("utf-8"),
            bytes(PublicKey(cmid)),
        ],
        program_id=PublicKey(SolanaPrograms.CMV2_PROGRAM)
    )[0])


def wallet_is_holder(pubkey: str, hashlist: list):

    user_nfts = get_wallet_nfts(wallet=pubkey, rpc=SolanaEndpoints.MAINNET_RPC)
    
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

        res = requests.get("https://discord.com/api/v7/users/@me", headers=headers)

        return res.json() if res.status_code == 200 else None
        
    except:
        
        return None

    

def get_local_time(_time: int):

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    utc = datetime.fromtimestamp(_time).replace(tzinfo=from_zone)
    return int(utc.astimezone(to_zone).timestamp())


def create_table_launchpad(collection: dict):
    
    _time = get_local_time(DROP_TIME)
    
    table = Table()

    table.add_column("NAME", justify="center", style="yellow")
    table.add_column("TIME (LOCAL)", justify="center", style="yellow")
    table.add_column("CANDY MACHINE ID",justify="center", style="green")
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

    if min_rank is not None and max_rank is not None and nft_data.get("rarity_rank"):
    
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
        
        client = Client(SolanaEndpoints.MAINNET_RPC)
        
        return client.get_token_supply(token_mint).get("result")
    
    except:
        
        return False



def get_collection_symbol(url):

    split_url = urlsplit(url)

    return split_url.path.split("/")[-1]

        
def get_me_collection_metadata(symbol: str):

    last_listed = MagicEden.get_listed_nfts(
        symbol=symbol,
        limit=2
    )

    if last_listed:
        
        last_listed = last_listed[0]
        
        mint = last_listed["mintAddress"]
        
        nft_metadata = get_nft_metadata(mint_key=mint, rpc=mint_rpc)
        
        if nft_metadata:
            
            creators = nft_metadata["data"]["creators"]
        
            update_auth = nft_metadata["update_authority"]
        
            return {
                "creators": creators,
                "updateAuthority": update_auth,
                "attributes": []
            }
    
    return None

def get_cc_collection_metadata(symbol: str):

    last_listed = CoralCube.get_listed_nfts(
        symbol=symbol,
        limit=2
    )

    if last_listed:
        
        last_listed = last_listed[0]
        
        mint = last_listed["mint"]
        
        nft_metadata = get_nft_metadata(mint_key=mint, rpc=mint_rpc)
        
        if nft_metadata:
        
            creators = nft_metadata["data"]["creators"]
        
            update_auth = nft_metadata["update_authority"]
        
            return {
                "creators": creators,
                "updateAuthority": update_auth,
                "attributes": []
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
            
        filtered_attributes = []
        
        if sweeper_data["Attributes"]:
            
            attributes = sweeper_data["Attributes"].split(";")
            
            for attribute in attributes:
                
                trait, value = attribute.split("=")

                filtered_attributes.append({"trait_type": trait, "value": value})
            
        sweeper_data["Attributes"] = filtered_attributes if filtered_attributes else None
        
        return sweeper_data
        
    except:
                
        return None


def fetch_sniper_data(site: str):
    
    global cached_collections, loaded_collections, sniper_start, kill_sniper
    
    while True:
                                
        if not tasks:
            
            kill_sniper = True
            
            ws.close()       
                  
            break
        
        if sniper_data is not None:

            updated_collections = {}
            
            for collection in sniper_data:
                
                symbol = collection["Collection"]
                
                if symbol not in cached_collections.values():
                    
                    if site == "magiceden":
                        
                        collection_metadata = get_me_collection_metadata(symbol=symbol)

                    elif site == "coralcube":
                        
                        collection_metadata = get_cc_collection_metadata(symbol=symbol)

                    if collection_metadata:
                        
                        collection_creators = collection_metadata["creators"]
                        collection_update_auth = collection_metadata["updateAuthority"]
                        
                        collection_identifier = "".join(collection_creators + [collection_update_auth])
                        
                        updated_collections[collection_identifier] = symbol
                        cached_collections[collection_identifier] = symbol

                        sniper_start = True
                else:
                    
                    collection_identifier = list(cached_collections.keys())[list(cached_collections.values()).index(symbol)]
                    updated_collections[collection_identifier] = symbol
            
            loaded_collections = updated_collections
            
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


def monitor_sniper_file(file_name: str):
    
    [None, None]
    
    global sniper_data
    
    [None, None]

    while not kill_sniper:
        
        collections = []
        
        try:
            
            with open(f'{file_name}.csv', 'r') as f:

                reader = csv.reader(f)

                reader = list(reader)
                
            keys = reader[0]
            rows = reader[1:25]
            
        
        except:
                
            rows = []

        for values in rows:
            
            sniper_data_raw = dict(zip(keys, values))
            
            try:
                
                if sniper_data_raw["Collection"]:
                    
                    sniper_data_raw["MinPrice"] = float(sniper_data_raw["MinPrice"]) if sniper_data_raw["MinPrice"] else None
                    sniper_data_raw["MaxPrice"] = float(sniper_data_raw["MaxPrice"]) if sniper_data_raw["MaxPrice"] else None
                    
                    sniper_data_raw["UnderFloor(%)"] = float(sniper_data_raw["UnderFloor(%)"]) if sniper_data_raw["UnderFloor(%)"] else None
                    
                    if (sniper_data_raw["MinPrice"] is None or sniper_data_raw["MaxPrice"] is None) and sniper_data_raw["UnderFloor(%)"] is None:

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
        
def save_me_collection_current_floor(symbol: str):
    
    global current_floors
    

    while True:
            
        last_listed = MagicEden.get_listed_nfts(
            symbol=symbol,
            limit=2
        )

        if last_listed:
        
            floor = last_listed[0]["price"]
                        
            current_floors[symbol] = floor

            break
        
        time.sleep(1)


def save_cc_collection_current_floor(symbol: str):
    
    global current_floors
    
    while True:

        last_listed = CoralCube.get_listed_nfts(
            symbol=symbol,
            limit=2
        )
        
        if last_listed:
        
            floor = lamports_to_sol(last_listed[0]["price"])
                        
            current_floors[symbol] = floor

            break
        
        time.sleep(1)

def monitor_me_collection_floor():
            
    while not kill_sniper:
        
        if sniper_start:
            
            trs = []
            
            for collection in sniper_data:
                
                symbol = collection["Collection"]
                
                showFloorT = Thread(
                    target=save_me_collection_current_floor,
                    args=[symbol],
                    daemon=True
                )
                
                showFloorT.start()
                trs.append(showFloorT)

            for tr in trs:
                
                tr.join()
                
            time.sleep(Custom.FP_MONITOR_POLLING)



def monitor_cc_collection_floor():
            
    while not kill_sniper:
        
        if sniper_start:
            
            trs = []
            
            for collection in sniper_data:
                
                symbol = collection["Collection"]
                
                showFloorT = Thread(
                    target=save_cc_collection_current_floor,
                    args=[symbol],
                    daemon=True
                )
                
                showFloorT.start()
                trs.append(showFloorT)

            for tr in trs:
                
                tr.join()
                
            time.sleep(Custom.FP_MONITOR_POLLING)

def bifrost_dc_login(mint_site: str, dc_auth_token: str) -> None | BifrostAuth:
    
    user_dc_data = check_dc_token(token=dc_auth_token)
    
    console.print(logger(f"[BOT] [yellow]Validating Discord auth token {dc_auth_token}...[/]"))

    if user_dc_data:
        
        console.print(logger("[BOT] [green]Discord auth token validated successfuly[/]"))
        
    else:
        
        console.print(logger("[BOT] [red]Unable to validate Discord auth token[/]"))
        
        return None
        
    user_name = user_dc_data["username"] + "#" + user_dc_data["discriminator"]
    
    bf_auth = BifrostAuth(
        mint_site=mint_site
    )
    
    console.print(logger(f"[BOT] [yellow]Accessing {mint_site} for Discord login...[/]"))
    
    if bf_auth.get_mint_site():
        
        console.print(logger("[BOT] [green]Access successful[/]"))
        
    else:
        
        console.print(logger(f"[BOT] [red]Unable to access {mint_site}[/]"))
        
        return None
    
    console.print(logger("[BOT] [yellow]Generating Discord auth session...[/]"))
    
    if bf_auth.generate_auth_session():
        
        console.print(logger("[BOT] [green]Auth session generated successfuly[/]"))
        
    else:
        
        console.print(logger("[BOT] [red]Unable to generate auth session[/]"))
        
        return None

    console.print(logger("[BOT] [yellow]Generating Discord signin...[/]"))
    
    signin_url = bf_auth.generate_dc_signin()
    
    if signin_url:
        
        console.print(logger("[BOT] [green]Signin generated successfuly[/]"))
        
    else:
        
        console.print(logger("[BOT] [red]Unable to generate signin[/]"))
        
        return None

    console.print(logger(f"[BOT] [yellow]Logging in as {user_name}[/]"))
    
    auth_url = bf_auth.authorize_discord(signin_url=signin_url, dc_auth_token=dc_auth_token)
    
    if auth_url:
        
        console.print(logger("[BOT] [green]Logged in successfuly[/]"))
        
    else:
        
        console.print(logger("[BOT] [red]Unable to login[/]"))
        
        return None
    
    console.print(logger(f"[BOT] [yellow]Waiting for auth callback...[/]"))
    
    if bf_auth.discord_auth_callback(auth_url=auth_url):
        
        console.print(logger("[BOT] [green]Auth callback received successfuly[/]"))
        
    else:
        
        console.print(logger("[BOT] [red]Auth callback failed[/]"))
        
        return None

    return bf_auth


def get_drop_time():

    if PROGRAM in [SolanaPrograms.CMV2_PROGRAM, SolanaPrograms.LMN_PROGRAM]:

        if PROGRAM == SolanaPrograms.CMV2_PROGRAM:
            
            meta = asyncio.run(get_program_account_idl("CandyMachine", CM, PROGRAM, SolanaEndpoints.MAINNET_RPC))

        elif PROGRAM == SolanaPrograms.LMN_PROGRAM:
            
            meta = asyncio.run(get_program_account_idl("CandyMachine", CM, PROGRAM, SolanaEndpoints.MAINNET_RPC, IDLs.LMN_IDL))

        return int(meta.data.go_live_date) if meta else None

    elif PROGRAM in [SolanaPrograms.ME_PROGRAM, SolanaPrograms.BF_PROGRAM]:
        
        if PROGRAM == SolanaPrograms.ME_PROGRAM:
            
            collection = MagicEdenLaunchpad.get_collection_info(collection_url)

        elif PROGRAM == SolanaPrograms.BF_PROGRAM:
            
            collection = BifrostLaunchpad.get_collection_info(collection_url)
        
        return collection["date"] if collection else None

    elif PROGRAM == SolanaPrograms.ML_PROGRAM:
        
        return int(CM["REACT_APP_CANDY_START_DATE"])
    
    elif PROGRAM == SolanaPrograms.EA_PROGRAM:
        
        collection = ExchangeArt.get_collection_info(collection_url)

        return collection["contractGroups"][0]["availableContracts"]["editionSales"][0]["data"]["start"] if collection else None
    

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
                
    
def create_table_wallets(wallets: list):

    with console.status(f"[yellow]Downloading wallets data[/]", spinner="bouncingBar", speed=1.5):

        table = Table(show_lines=True)
        table.add_column("WALLET", style="green", justify="center")
        table.add_column("ADDRESS", style="yellow", justify="center")
        table.add_column("TASKS", style="cyan", justify="center")
        table.add_column("BALANCE", style="cyan", justify="center")
        
        for wallet in wallets:

            balance = get_wallet_balance(wallet["address"], mint_rpc)

            table.add_row(wallet["name"], wallet["address"], str(wallet["tasks"]), str(round(lamports_to_sol(balance), 2)))

        return table


def get_cm_mints_status(cm: str | dict, program: str):

    available = redeemed = None
    
    if program in [SolanaPrograms.CMV2_PROGRAM, SolanaPrograms.ME_PROGRAM, SolanaPrograms.LMN_PROGRAM]:
            
        metadata = asyncio.run(get_program_account_idl(
            "CandyMachine",
            account=cm,
            prog=program,
            rpc=SolanaEndpoints.MAINNET_RPC,
            prog_idl=IDLs.LMN_IDL if program == SolanaPrograms.LMN_PROGRAM else None
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
    
    elif program == SolanaPrograms.EA_PROGRAM:
        
        collection = ExchangeArt.get_collection_info(collection_url)
        
        if collection:
            
            redeemed = collection["contractGroups"][0]["mint"]["masterEditionAccount"]["currentSupply"]
            available = collection["contractGroups"][0]["mint"]["masterEditionAccount"]["maxSupply"]
            
    if available is not None and redeemed is not None:
            
        minted = int((redeemed/available) * 100)

        return available, redeemed, minted
    
    return None

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

            balance = console.input(f"[purple] >>[/] Select an amount to transfer from wallet {i}: ")

            if balance == "e":

                return None

            balance = int(sol_to_lamports(float(balance)))

            wallet_balance = wallets_nfts[wallet]["balance"]

            if balance < wallet_balance:

                return balance

            else:

                return wallet_balance - 2042320

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
        
    for node in [snipe_rpc, mint_rpc]:
            
        for _ in range(3):
            
            try:
                client = Client(node)
                
                chain_client = Client(SolanaEndpoints.MAINNET_RPC)
                
                real_slot = chain_client.get_slot()["result"]
                
                node_slot = client.get_slot()["result"]
                
                delay = real_slot - node_slot if real_slot - node_slot >= 0 else 0
                
                console.print(f" [yellow]Your node[/] [cyan]{node}[/] [yellow]is behind by[/] [white]{delay}[/] [yellow]slots[yellow]")
                
            except:
                
                console.print(f" [red]Unreachable node[/] [cyan]{node}[/]")
                
            time.sleep(0.5)

def get_module():

    options = list(range(1, 10)) + [11, 12]

    while True:

        try:

            mode = int(console.input("[purple] >>[/] Select a module to use: "))

            if mode in options:

                return mode

        except ValueError:

            pass

        except KeyboardInterrupt:

            exit()

        console.print("[red]    Invalid option provided[/]")



set_app_title(f"Neura - {Bot.VERSION}")
console = Console(highlight=False, log_path=False)


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

    mint_rpc = get_config(parameter="mint_rpc")
    snipe_rpc = get_config(parameter="snipe_rpc")
    user_time = get_config(parameter="time")
    advanced_mode = get_config(parameter="advanced")
    success_webhook = get_config(parameter="webhook")
    dc_auth_token = get_config(parameter="discord")
        
    valid_mint_rpc = validate_sol_rpc(rpc=mint_rpc)
    valid_snipe_rpc = validate_sol_rpc(rpc=snipe_rpc)
    
    menu = False

    show_banner()

    if mint_rpc and valid_mint_rpc:

        console.print(" {:<12} [green]{:<6}[/] [purple]> [/]{}".format("Mint RPC", "ON", f"{mint_rpc} [purple]>[/] {valid_mint_rpc} ms"))

    else:

        console.print(" {:<12} [red]OFF[/]".format("Mint RPC"))

    if snipe_rpc and valid_snipe_rpc:

        console.print(" {:<12} [green]{:<6}[/] [purple]> [/]{}".format("Snipe RPC", "ON", f"{snipe_rpc} [purple]>[/] {valid_snipe_rpc} ms"))

    else:

        console.print(" {:<12} [red]OFF[/]".format("Snipe RPC"))
        
    if user_time:

        show_user_time = datetime.fromtimestamp(user_time).strftime("%H:%M:%S")
        
        console.print(" {:<12} [green]{:<6}[/] [purple]> [/]{}".format("Time", "ON", show_user_time))

    else:

        console.print(" {:<12} [red]OFF[/]".format("Time"))
    
    print()

    console.print("[cyan] [1 ][/] CandyMachine mint")
    console.print("[cyan] [2 ][/] MagicEden mint")
    console.print("[cyan] [3 ][/] MagicEden sniper")
    console.print("[cyan] [4 ][/] Wallets manager")
    console.print("[cyan] [5 ][/] MagicEden sweeper")
    console.print("[cyan] [6 ][/] FamousFox sniper")
    console.print("[cyan] [7 ][/] LaunchMyNFT mint")
    console.print("[cyan] [8 ][/] CoralCube sniper")
    console.print("[cyan] [9 ][/] MonkeLabs mint")
    console.print("[cyan] [10][/] Soon...")
    console.print("[cyan] [11][/] ExchangeArt mint")
    console.print("[cyan] [12][/] Node health checker\n")
    
    mode = get_module()

    clear()

    while True:

        if menu:

            break

        wallets = get_sol_wallets()

        if not wallets:

            console.input("[yellow] ERROR![/] [red]Invalid wallets data / No wallets loaded [/]", password=True)

            break

        if not valid_snipe_rpc or not valid_mint_rpc:

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
                
                if True:
                        
                    console.print(create_table_wallets(wallets))
                    print()

                    collection_url = str(console.input("[purple] >>[/] MagicEden collection URL: ")).lower()
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
                loaded_collections = {}
                
                ws_rpc = get_websocket_url(snipe_rpc)
                
                privkey = wallet["privkey"]
                tasks = wallet["tasks"]
                pubkey = wallet["address"]
                
                monitorSniperFileT = Thread(
                    target=monitor_sniper_file,
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
                    rpc=snipe_rpc,
                    privkey=privkey,
                )

                console.print(logger(f"[SNIPER] [cyan][COLLECTIONS ~ {len(loaded_collections)}][/] [yellow]Loading file data and initialazing...[/]"))
                
                def check_me_tx_and_purchase(tx: dict):
                            
                    global tasks
                    
                    status = f"[SNIPER] [cyan][COLLECTIONS ~ {len(loaded_collections)}][/]"

                    listing_data = magic_eden.check_tx_is_listing(tx["signature"])
                    
                    if not listing_data or kill_sniper:
                        
                        return
                                    
                    console.print(logger(f"{status} [yellow]Fetching new data...[/]"))

                    mint_address = listing_data["mint"]
                    seller = listing_data["seller"]
                    price_in_sol = lamports_to_sol(listing_data["price"])
                    price_in_lamports = listing_data["price"]
                    escrow_pubkey = listing_data["escrow"]
                    
                    nft_metadata = get_nft_metadata(mint_key=mint_address, rpc=mint_rpc)
                    
                    if not nft_metadata:
                        
                        console.print(logger(f"{status} [red]Unable to get NFT data (node)[/]"))
                        
                        return
                
                    nft_name = nft_metadata["data"]["name"]
                    nft_creators = nft_metadata["data"]["creators"]
                    nft_update_auth = nft_metadata["update_authority"]
                    nft_uri = nft_metadata["data"]["uri"]

                    to_match_identifier = "".join(nft_creators + [nft_update_auth])
                    
                    if to_match_identifier not in loaded_collections.keys():
                        
                        return
                                            
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
                
                    if not matching_listing:
                        
                        return
                    
                    valid_listing = None
                    
                    if min_sol is not None and max_sol is not None:
                        
                        valid_listing = min_sol <= price_in_sol <= max_sol
                                            
                    if (valid_listing is not False) and under_floor is not None and collection_floor is not None:
                        
                        max_possible_price = collection_floor - (collection_floor * (under_floor/100))
                            
                        valid_listing = price_in_sol <= max_possible_price
                            
                    if not valid_listing:
                        
                        return
                                                            
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
                            
                            if not is_valid_snipe:
                                
                                console.print(logger(f"{status} [red]Rank or attributes do not match[/]"))
                                
                                return

                        else:
                            
                            console.print(logger(f"{status} [red]Unable to get NFT data[/]"))
                            
                            return

                                            
                    console.print(logger(f"{status} [yellow]Sniped {nft_name}[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))
        
                    console.print(logger(f"{status} [yellow]Purchasing...[/]"))
                    
                    tx_hash = magic_eden.buy_nft_api(
                        seller=seller,
                        price=price_in_lamports,
                        mint=mint_address
                    )

                    if not tx_hash:
                        
                        console.print(logger(f"{status} [red]Purchase failed[/]"))

                        return
                    
                    console.print(logger(f"{status} [green]Purchased {nft_name}[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))
                    
                    tasks -= 1
                    
                    send_sniper_webhook(
                        mint=mint_address,
                        tx=tx_hash,
                        price=price_in_sol,
                        webhook=success_webhook
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
                
                def on_open_me(ws: websocket.WebSocket):

                    ws.send(json.dumps(
                        {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "logsSubscribe",
                        "params": [
                            {
                            "mentions": [ "M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K" ]
                            },
                            {
                            "commitment": "confirmed"
                            }
                        ]
                        }
                    ))
                
                def on_message_me(_, msg):
                    
                    if not sniper_start or not tasks:
                        
                        return 
                    
                    tx = json.loads(msg)["params"]["result"]["value"]

                    logs = "".join(tx["logs"])
                    
                    if not tx["err"] and "Instruction: Sell" in logs:
                        
                        snipeT = Thread(
                            target=check_me_tx_and_purchase,
                            args=[tx],
                            daemon=True
                        )
                        
                        snipeT.start()
                                    
                
                if tasks:
                        
                    fetchT = Thread(
                        target=fetch_sniper_data,
                        args=["magiceden"],
                        daemon=True
                    )
                    
                    fetchT.start()
                    
                    while True:
                        
                        ws = websocket.WebSocketApp(url=ws_rpc, on_open=on_open_me, on_message=on_message_me)
                        
                        ws.run_forever()
                        
                        if kill_sniper:
                            
                            break
                        
                        ws.close()
                    
                console.input("\n\n [purple]>>[/] Press ENTER to exit ", password=True)

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
                        
                        balance = get_wallet_balance(wallet["address"], mint_rpc)

                        nfts_data = []

                        for nft in wallet_nfts:
                                                        
                            if operation_type in ["l", "ts", "tn", "b"]:

                                if nft.get("collectionName") or (nft.get("onChainCollection") and nft["onChainCollection"].get("key")) or operation_type in ["tn", "b"]:
                                    
                                    nfts_data.append(
                                        {
                                            "mint": nft["mintAddress"],
                                            "name": nft["title"], 
                                            "token": nft["id"],
                                            "symbol": nft.get("collectionName") or nft["onChainCollection"].get("key"),
                                            "attributes": nft["attributes"]
                                        }
                                    )                                    

                            elif operation_type in ["d", "u"]:

                                nfts_data.append(
                                    {
                                        "mint": nft["initializerDepositTokenMintAddress"],
                                        "name": nft["title"], 
                                        "token": nft["initializerDepositTokenAccount"],
                                        "symbol": nft.get("collectionSymbol") or nft.get("onChainCollectionAddress"),
                                        "price": lamports_to_sol(nft["takerAmount"]), 
                                        "attributes": nft["attributes"] 
                                    }
                                )
                            
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
                        rpc=mint_rpc,
                        privkey=privkey
                    )
                    
                    wallet_manager = SolWalletManager(
                        rpc=snipe_rpc,
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
                        rpc=mint_rpc,
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
                        attributes = sweeper_data["Attributes"]
                        
                        if amount:
                            
                            max_funds = under_price = None
                        
                        elif max_funds:
                            
                            amount = under_price = None
                            
                        elif under_price:
                            
                            amount = max_funds = None
                                                
                        if amount is not None:
                            
                            status = f"[SWEEPER] [cyan][{symbol.upper()}] [AMOUNT ~ {amount}][/]"
                        
                        elif max_funds is not None:
                            
                            status = f"[SWEEPER] [cyan][{symbol.upper()}] [FUNDS ~ {max_funds} SOL][/]"
                        
                        elif under_price is not None:
                            
                            status = f"[SWEEPER] [cyan][{symbol.upper()}] [MAX PRICE ~ {under_price} SOL][/]"
                            
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
                            rpc=snipe_rpc,
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
                            rpc=snipe_rpc,
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
                                        rpc=snipe_rpc,
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
                loaded_collections = {}
                
                ws_rpc = get_websocket_url(snipe_rpc)
                
                privkey = wallet["privkey"]
                tasks = wallet["tasks"]
                pubkey = wallet["address"]
                
                monitorSniperFileT = Thread(
                    target=monitor_sniper_file,
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
                    rpc=snipe_rpc,
                    privkey=privkey,
                )

                console.print(logger(f"[SNIPER] [cyan][COLLECTIONS ~ {len(loaded_collections)}][/] [yellow]Loading file data and initialazing...[/]"))
                
                def check_cc_tx_and_purchase(tx: dict):
                            
                    global tasks
                    
                    status = f"[SNIPER] [cyan][COLLECTIONS ~ {len(loaded_collections)}][/]"

                    listing_data = coral_cube.check_tx_is_listing(tx["signature"])
                    
                    if not listing_data or kill_sniper:
                        
                        return
                                    
                    console.print(logger(f"{status} [yellow]Fetching new data...[/]"))

                    mint_address = listing_data["mint"]
                    seller = listing_data["seller"]
                    price_in_sol = lamports_to_sol(listing_data["price"])
                    price_in_lamports = listing_data["price"]
                    
                    nft_metadata = get_nft_metadata(mint_key=mint_address, rpc=mint_rpc)
                    
                    if not nft_metadata:
                        
                        console.print(logger(f"{status} [red]Unable to get NFT data (node)[/]"))
                        
                        return
                
                    nft_name = nft_metadata["data"]["name"]
                    nft_creators = nft_metadata["data"]["creators"]
                    nft_update_auth = nft_metadata["update_authority"]
                    nft_uri = nft_metadata["data"]["uri"]

                    to_match_identifier = "".join(nft_creators + [nft_update_auth])
                    
                    if to_match_identifier not in loaded_collections.keys():
                        
                        return
                                            
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
                
                    if not matching_listing:
                        
                        return
                    
                    valid_listing = None
                    
                    if min_sol is not None and max_sol is not None:
                        
                        valid_listing = min_sol <= price_in_sol <= max_sol
                                            
                    if (valid_listing is not False) and under_floor is not None and collection_floor is not None:
                        
                        max_possible_price = collection_floor - (collection_floor * (under_floor/100))
                            
                        valid_listing = price_in_sol <= max_possible_price
                            
                    if not valid_listing:
                        
                        return
                                                            
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
                            
                            if not is_valid_snipe:
                                
                                console.print(logger(f"{status} [red]Rank or attributes do not match[/]"))
                                
                                return

                        else:
                            
                            console.print(logger(f"{status} [red]Unable to get NFT data[/]"))
                            
                            return

                                            
                    console.print(logger(f"{status} [yellow]Sniped {nft_name}[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))
        
                    console.print(logger(f"{status} [yellow]Purchasing...[/]"))
                    
                    tx_hash = coral_cube.buy_nft(
                        seller=seller,
                        price=price_in_lamports,
                        mint=mint_address,
                        creators=nft_creators
                    )

                    if not tx_hash:
                        
                        console.print(logger(f"{status} [red]Purchase failed[/]"))

                        return
                    
                    console.print(logger(f"{status} [green]Purchased {nft_name}[/] [purple]>[/] [cyan]{price_in_sol} SOL[/]"))
                    
                    tasks -= 1
                    
                    send_sniper_webhook(
                        mint=mint_address,
                        tx=tx_hash,
                        price=price_in_sol,
                        webhook=success_webhook
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
                                mint=mint_address,
                                price=sol_to_lamports(listing_price)
                            )
                            
                            if tx_hash:
                                                
                                console.print(logger(f"{status} [green]Listed {nft_name}[/] [purple]>[/] [cyan]{listing_price} SOL[/]"))

                            else:
                                
                                console.print(logger(f"{status} [red]Unable to list {nft_name}[/]"))
                
                def on_open_cc(ws: websocket.WebSocket):

                    ws.send(json.dumps(
                        {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "logsSubscribe",
                        "params": [
                            {
                            "mentions": [ "29xtkHHFLUHXiLoxTzbC7U8kekTwN3mVQSkfXnB1sQ6e" ]
                            },
                            {
                            "commitment": "confirmed"
                            }
                        ]
                        }
                    ))
                
                def on_message_cc(_, msg):
                    
                    if not sniper_start or not tasks:
                        
                        return 
                    
                    tx = json.loads(msg)["params"]["result"]["value"]

                    logs = "".join(tx["logs"])
                    
                    if not tx["err"] and "Instruction: Sell" in logs:
                        
                        snipeT = Thread(
                            target=check_cc_tx_and_purchase,
                            args=[tx],
                            daemon=True
                        )
                        
                        snipeT.start()
                                    
                if tasks:
                        
                    fetchT = Thread(
                        target=fetch_sniper_data,
                        args=["coralcube"],
                        daemon=True
                    )
                    
                    fetchT.start()
                    
                    while True:
                        
                        ws = websocket.WebSocketApp(url=ws_rpc, on_open=on_open_cc, on_message=on_message_cc)
                        
                        ws.run_forever()
                        
                        if kill_sniper:
                            
                            break
                        
                        ws.close()
                    
                console.input("\n\n [purple]>>[/] Press ENTER to exit ", password=True)

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

                collection_url = str(console.input("[purple] >>[/] Bifrost collection URL: ")).lower()
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

                    proceed = Prompt.ask("[purple] >>[/] Start Discord auth login?", choices=["y", "n"])
                    clear()

                    if proceed == "y":
                        
                        while True:
                                
                            bf_auth_session = bifrost_dc_login(collection_url, dc_auth_token)
                            print()
                            
                            if bf_auth_session:
                                
                                status = Prompt.ask("[purple]>>[/] Insert 'r' to refresh auth session or 'm' to start mint", choices=["r", "m"])
                                
                            else:
                                
                                status = Prompt.ask("[purple]>>[/] Insert 'e' to exit or 'r' to retry Discord auth login", choices=["e", "r"])
                            
                            clear()
                            
                            if status in ["e", "m"]:
                                
                                break
                        
                        if status == "e":
                            
                            menu = True
                            
                        break
                else:
                    
                    console.print("[yellow] ERROR![/] [red]Collection not found\n [/]")
        
        if mode == 11:
            
            while True:
                
                if True:
                        
                    console.print(create_table_wallets(wallets))
                    print()

                    collection_url = str(console.input("[purple] >>[/] ExchangeArt collection URL: "))
                    clear()

                    if collection_url == "e":
                        menu = True
                        break

                    with console.status("[yellow]Searching for collection[/]", spinner="bouncingBar", speed=1.5):

                        collection = ExchangeArt.get_collection_info(collection_url)

                    if collection:
                        
                        contract = collection["contractGroups"][0]
                        
                        CM = contract["availableContracts"]["editionSales"][0]["keys"]["mintKey"]
                        PROGRAM = SolanaPrograms.EA_PROGRAM
                        DROP_TIME = contract["availableContracts"]["editionSales"][0]["data"]["start"]
                        
                        info_to_show = {
                            "name": contract["mint"]["name"],
                            "price": contract["availableContracts"]["editionSales"][0]["data"]["price"],
                            "supply": contract["mint"]["masterEditionAccount"]["maxSupply"],
                            "cmid": CM,
                            "date": DROP_TIME
                        }
                        
                        console.print(create_table_launchpad(info_to_show))
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
        
        if mode == 12:
            
            if not valid_mint_rpc or not valid_snipe_rpc:

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
                                        
                    while True:

                        clear()

                        if mode in [1, 2, 7]:

                            with console.status(f"[yellow]Downloading candy machine data[/]", spinner="bouncingBar", speed=1.5):
                                
                                if mode in [1, 2]:
                                
                                    cm_metadata = asyncio.run(get_program_account_idl("CandyMachine", CM, PROGRAM, SolanaEndpoints.MAINNET_RPC))
                                
                                else:
                                    
                                    cm_metadata = asyncio.run(get_program_account_idl("CandyMachine", CM, PROGRAM, SolanaEndpoints.MAINNET_RPC, prog_idl=IDLs.LMN_IDL))

                                if mode == 1:
                                    
                                    pda_account = get_collection_pda_account(cmid=CM)

                                    collection_set_metadata = asyncio.run(get_program_account_idl("CollectionPDA", pda_account, PROGRAM, SolanaEndpoints.MAINNET_RPC))

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

                        show_drop_time = datetime.fromtimestamp(DROP_TIME).strftime("%H:%M:%S")
                        
                        console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Initialazing mint[/]\n".format("ALL", "INIT", show_drop_time)), end="")

                        if mode != 9 or user_time:

                            console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Awaiting for drop time[/]\n".format("ALL", "INIT", show_drop_time)), end="")

                            wait_for_drop(exit_before=3)
                            
                        while True:

                            recent_blockhash = get_blockhash(mint_rpc)

                            if recent_blockhash:
                                
                                console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Initialazing transactions[/]\n".format("ALL", "INIT", show_drop_time)), end="")
                                
                                break
                            
                            else:

                                console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [red]Unable to initialize txs (node)[/]\n".format("ALL", "INIT", show_drop_time)), end="")
                                
                        if mode != 9 or user_time:
                            
                            wait_for_drop()

                        for wallet in wallets:

                            mintT = Thread(target=mint, args=[wallet])
                            mintT.start()
                            trs.append(mintT)

                        for tr in trs:
                            tr.join()

                        print()
                        
                        mints_status = get_cm_mints_status(CM, PROGRAM)
                        
                        if mints_status:
                                
                            available, redeemed, minted = mints_status
                            
                            console.print(f"[AVAILABLE ~ [green]{available}[/]] [REDEEMED ~ [yellow]{redeemed}[/]] [MINTED ~ [cyan]{minted}%[/]]\n")
                            
                        print("\n")

                        status = Prompt.ask("[purple]>>[/] Insert 'e' to exit or 'r' to retry mint", choices=["e", "r"])

                        print("\n")

                        if status == "e":

                            menu = True

                            break
                        
                        DROP_TIME = int(time.time())

            elif mode == 10:
                            
                bf_launchpad = BifrostLaunchpad(
                    bf_auth=bf_auth_session
                )
                
                while True:

                    clear()                        

                    with console.status(f"[yellow]Downloading candy machine data[/]", spinner="bouncingBar", speed=1.5):
                                                
                        cm_metadata = bf_launchpad.get_cm_state(CM)
                        
                        if not cm_metadata:

                            clear()

                            console.print("[red] ERROR![/] [yellow]Failed to fetch candy machine data\n[/]")

                            break

                    trs = []

                    if user_time:

                        DROP_TIME = user_time

                    show_drop_time = datetime.fromtimestamp(DROP_TIME).strftime("%H:%M:%S")
                    
                    console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Initialazing mint[/]\n".format("ALL", "INIT", show_drop_time)), end="")

                    console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Awaiting for drop time[/]\n".format("ALL", "INIT", show_drop_time)), end="")

                    wait_for_drop(exit_before=3)
                        
                    while True:
                        
                        token_mint = cm_metadata["tokenMint"]
                        
                        bonding_info = bf_launchpad.get_bonding_info(token_mint)
                        
                        if bonding_info:
                            
                            token_bonding = bonding_info["publicKey"]
                                                        
                            console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Initialazing transactions[/]\n".format("ALL", "INIT", show_drop_time)), end="")
                            
                            break
                        
                        else:

                            console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [red]Unable to initialize txs (node)[/]\n".format("ALL", "INIT", show_drop_time)), end="")
                                                    
                    wait_for_drop()
                        
                    bonding_price = bf_launchpad.get_bonding_price(token_bonding)

                    max_price = bf_launchpad.get_max_price(bonding_price or cm_metadata["price"])
                    
                    for wallet in wallets:

                        mintT = Thread(target=mint, args=[wallet])
                        mintT.start()
                        trs.append(mintT)

                    for tr in trs:
                        tr.join()

                    print()
                    
                    mints_status = get_cm_mints_status(CM, PROGRAM)
                    
                    if mints_status:
                            
                        available, redeemed, minted = mints_status
                        
                        console.print(f"[AVAILABLE ~ [green]{available}[/]] [REDEEMED ~ [yellow]{redeemed}[/]] [MINTED ~ [cyan]{minted}%[/]]\n")
                        
                    print("\n")

                    status = Prompt.ask("[purple]>>[/] Insert 'e' to exit or 'r' to retry mint", choices=["e", "r"])

                    print("\n")

                    if status == "e":

                        menu = True

                        break
                    
                    DROP_TIME = int(time.time())
                       
            elif mode == 11:
                                    
                if user_time:

                    DROP_TIME = user_time

                show_drop_time = datetime.fromtimestamp(DROP_TIME).strftime("%H:%M:%S")
                
                console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Initialazing mint[/]\n".format("ALL", "INIT", show_drop_time)), end="")

                console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Awaiting for drop time[/]\n".format("ALL", "INIT", show_drop_time)), end="")

                wait_for_drop()
                
                kill_websocket = False
                
                ws_rpc = get_websocket_url(mint_rpc)
                        
                mint_auth = str(PublicKey.find_program_address(
                    seeds=[
                        "metadata".encode("utf-8"),
                        bytes(PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")),
                        bytes(PublicKey(CM)),
                        "edition".encode("utf-8")
                    ],
                    program_id=PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")
                )[0])
                
                show_drop_time = datetime.fromtimestamp(DROP_TIME).strftime("%H:%M:%S")

                def on_open_ea(ws: websocket.WebSocket):

                    ws.send(json.dumps(
                        {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "accountSubscribe",
                        "params": [
                            mint_auth,
                            {
                            "encoding": "jsonParsed",
                            "commitment": "processed"
                            }
                        ]
                        }
                    ))
                    
                def on_message_ea(_, message):
                    
                    global kill_websocket
                    
                    data = json.loads(message)["params"]["result"]["value"]["data"][0]
                    
                    data = b64decode(data)

                    if len(data) != 282:
                        
                        console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [red]Collection is oos[/]\n".format("ALL", "FETCH", show_drop_time)), end="")
                        
                        kill_websocket = True
                        
                        return     
                                
                    minted = int.from_bytes(data[1:9], "little")
                    available = int.from_bytes(data[10:18], "little")
                    
                    blockhash = get_blockhash(mint_rpc)
                    
                    trs = []
                    
                    for wallet in wallets:
                        
                        name = wallet["name"]
                        tasks = wallet["tasks"]
                        privkey = wallet["privkey"]
                        
                        status = "[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/]".format(name, f"{minted}/{available}", show_drop_time)

                        if tasks:
                                
                            mintT = Thread(target=send_ea_tx, args=[privkey, mint_rpc, blockhash, minted, status])
                            mintT.start()
                            trs.append(mintT)
                    
                    for tr in trs:
                        
                        tr.join()

                def spam_logs_status():
                    
                    while True:
                        
                        console.print(logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ {:<10}] [TIME ~ {:<6}][/] [yellow]Awaiting for new edition[/]\n".format("ALL", "FETCH", show_drop_time)), end="")

                        time.sleep(0.5)

                        if kill_websocket:
                            
                            break
                        
                spamT = Thread(
                    target=spam_logs_status,
                    daemon=True
                )
                
                spamT.start()
                
                while True:
                    
                    ws = websocket.WebSocketApp(url=ws_rpc, on_open=on_open_ea, on_message=on_message_ea)

                    ws.run_forever()
                    
                    if kill_websocket:
                        
                        break
                    
                    ws.close()
                
                print()
                
                mints_status = get_cm_mints_status(CM, PROGRAM)
                
                if mints_status:
                        
                    available, redeemed, minted = mints_status
                    
                    console.print(f"[AVAILABLE ~ [green]{available}[/]] [REDEEMED ~ [yellow]{redeemed}[/]] [MINTED ~ [cyan]{minted}%[/]]\n")
                    
                print("\n")

                console.input("[purple]>>[/] Press ENTER to exit ", password=True)

                print("\n")

                menu = True

                break
                