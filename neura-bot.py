import json
import discord
from discord.ext import commands
import requests
from threading import Thread
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import re
import base58
import base64
from datetime import datetime
from dhooks import Embed
import cloudscraper
from solana.rpc.async_api import AsyncClient
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from anchorpy import Program, Wallet, Provider
from base58 import b58decode

try:
        
    from modules import NeuraDB
    from lib import AccountClient
    
except:
    
    from neuradb import NeuraDB
    from idl_fetcher import AccountClient
    
def is_URL(url):

    try:
        requests.get(url, timeout=3)
        return True

    except:
        pass


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



def get_IDs(url: str, script: str):

    global IDS

    split_url = urlsplit(url)
    url = f"{split_url.scheme}://{split_url.netloc}{script}"

    if is_URL(url):

        try:
            res = str(requests.get(url, timeout=2).content.decode())
        except:
            return None

        invalid_ids = ["cndy", "Token", "meta", "111", "fair", "gatem"]

        possible_ids = re.findall(
            'PublicKey\(\"(.*?)\"\)', res) + re.findall('[a-zA-z ]+[= ]+\"(.*?)\"', res)

        for id in possible_ids:

            if re.match("^[A-Za-z0-9]*$", id):

                if not any(invalid in id for invalid in invalid_ids):

                    try:

                        if id not in IDS and len(base58.b58decode(id)) == 32:

                            IDS.append(id)
                    except:

                        pass


def check_ID(id: str):

    global CM

    try:

        client = Client(sol_rpc)
        
        res = client.get_account_info(id)

        owner = res["result"]["value"]["owner"]
        data = res["result"]["value"]["data"][0]

        data = str(base64.b64decode(data))

        website = re.search("(?P<url>https?://[^\s]+)", data)

        if not CM:

            if owner == "cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ" and website:

                CM = id

    except:
        pass


def get_owner(account: str):

    try:

        client = Client(sol_rpc)
        
        res = client.get_account_info(account)

        return res["result"]["value"]["owner"]

    except:
        
        return None



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
                            
                    return accs
    except:
        
        return None


def get_ml_items_redeemed(index_key: str):
    
    try:
        
        client = Client("https://api.mainnet-beta.solana.com")

        res = client.get_account_info(index_key, encoding="base58")

        data = res["result"]["value"]["data"][0]

        data = list(bytes(b58decode(data)))

        return (data[1] << 8) + data[0]
    
    except:
        
        return None
    
def create_success_embed(text: str):

    embed = Embed(
        description=f"**{text}**",
        color=0x45D14A
    )

    return embed


def create_error_embed(text: str):

    embed = Embed(
        description=f"**{text}**",
        color=0xDA2A2A
    )

    return embed

def get_me_collection_stats(symbol: str):
    
    
    try:
        
        scraper = cloudscraper.create_scraper()

        return scraper.get(f"https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/{symbol}").json()["results"]

    except:
        
        return None
    
def get_me_collection_info(symbol: str):
    
    
    try:
        
        scraper = cloudscraper.create_scraper()

        return scraper.get(f"https://api-mainnet.magiceden.io/collections/{symbol}").json()

    except:
        
        return None

def get_cc_collection_data(symbol: str):
    
    try:
        
        scraper = cloudscraper.create_scraper()

        return scraper.get(f"https://api.coralcube.io/v1/getItems?offset=0&page_size=24&ranking=price_asc&symbol={symbol}").json()["collection"]

    except:
        
        return None
    
async def get_cm_metadata(cmid: str, prog: str):

    try:

        program = None

        if prog == "me":

            program_id = PublicKey(
                "CMZYPASGWeTz7RNGHaRJfCq2XQ5pYK6nDvVQxzkH51zb")

        elif prog == "v2":

            program_id = PublicKey(
                "cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ")

        elif prog == "lmn":
            
            program_id = PublicKey(
                "ArAA6CZC123yMJLUe4uisBEgvfuw2WEvex9iFmFCYiXv")
            
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
        
        candyMachine = await AccountClient.fetch_custom(program.account['CandyMachine'], PublicKey(cmid))

        await program.close()
        await client.close()

        return candyMachine

    except:
        
        await client.close()

        if program:

            await program.close()

        return None


def get_collection_symbol(url):

    split_url = urlsplit(url)

    return split_url.path.split("/")[-1]


intents = discord.Intents.default()
intents.members = True

token = "OTQxMjcxODgxMTMzMjAzNDg3.YgThwA.k8yFD3A6T1S_G3k4scMJ7LYMCfs"

activity = discord.Activity(
    type=discord.ActivityType.watching, name="Websites")

client = commands.Bot(command_prefix="!", intents=intents,
                      activity=activity, status=discord.Status.online)

sol_rpc = "https://api.mainnet-beta.solana.com"

CHANNEL_ID = 946076013018898530

EMBED_COLOR = 0x6436CB
ICON_URL = "https://cdn.discordapp.com/attachments/921022038074871879/981234960121856110/logo2.png"
IDS = []
CM = None

async def generate_me_embed(url: str) -> Embed:
    
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

        scraper = cloudscraper.create_scraper()
        
        collection = scraper.get(f"https://api-mainnet.magiceden.io/launchpads/{symbol}", headers=headers).json()

        date_str = collection["launchDate"][:-1]

        date = int(datetime.fromisoformat(date_str).timestamp())
        
        name = collection["name"]
        image = collection["image"]
        supply = collection["size"]
        price = collection["price"]

        redeemed =  collection["state"]["itemsRedeemed"]
        available =  collection["state"]["itemsAvailable"]
        
        minted = str(int((redeemed/available) * 100))
        
        cmid = collection["mint"]["candyMachineId"]

        link = url

        embed = Embed(
            color=EMBED_COLOR

        )

        embed.set_title(title=name, url=link)
        embed.add_field(name="**Supply**", value=str(supply))
        embed.add_field(name="**Price**", value=str(price))

        embed.add_field(name="**Launch date**",
                        value=f"<t:{date}>", inline=False)
        embed.add_field(name="**Available**", value=str(available))
        embed.add_field(name="**Redeemed**", value=str(redeemed))
        embed.add_field(name="**Minted**", value=f"{minted} %")
        embed.add_field(name="**Candy Machine ID**",
                        value=f"`{cmid}`", inline=False)

        embed.set_thumbnail(image)
        embed.set_footer("Neura | NFT bot & Alpha group", ICON_URL)

        return embed
    
    except:
                
        return None
    
async def generate_lmn_embed(url: str) -> Embed:
    
    try:
        
        cmid = get_lmn_candy_machine(url=url)
            
        if cmid:
            
            metadata = await get_cm_metadata(cmid=cmid, prog="lmn")
            
            if metadata:
                
                embed = Embed(
                    color=EMBED_COLOR
                )

                launch_date = int(metadata.data.go_live_date)
                items_available = metadata.data.items_available
                items_redeemed = metadata.items_redeemed
                price = float(metadata.data.price/(10**9))

                minted = int((items_redeemed/items_available) * 100)
                
                embed.add_field(name="**Candy Machine ID**", value=f"`{cmid}`")
                embed.add_field(name="**Launch date**",
                                value=f"<t:{launch_date}>", inline=False)
                embed.add_field(name="**Price**", value=str(price), inline=False)
                embed.add_field(name="**Available**",
                                value=str(items_available))
                embed.add_field(name="**Redeemed**", value=str(items_redeemed))
                embed.add_field(name="**Minted**", value=f"{minted}%")
                
                embed.set_footer("Neura | NFT bot & Alpha group", ICON_URL)
                
                return embed
    except:
        
        pass
    
    return None

async def generate_ml_embed(url: str) -> Embed:
    
    try:
        
        accounts = get_ml_candy_machine(url=url)
            
        if accounts:
            
            items_redeemed = get_ml_items_redeemed(index_key=accounts["REACT_APP_INDEX_KEY"])
            
            if items_redeemed is not None:
                
                embed = Embed(
                    color=EMBED_COLOR
                )

                launch_date = int(accounts["REACT_APP_CANDY_START_DATE"])
                items_available = int(accounts["REACT_APP_INDEX_CAP"])
                price = float(int(accounts["REACT_APP_PRICE"])/(10**9))
                cmid = accounts["REACT_APP_CONFIG_KEY"]
                
                minted = int((items_redeemed/items_available) * 100)
                
                embed.add_field(name="**Candy Machine ID**", value=f"`{cmid}`")
                embed.add_field(name="**Launch date**",
                                value=f"<t:{launch_date}>", inline=False)
                embed.add_field(name="**Price**", value=str(price), inline=False)
                embed.add_field(name="**Available**",
                                value=str(items_available))
                embed.add_field(name="**Redeemed**", value=str(items_redeemed))
                embed.add_field(name="**Minted**", value=f"{minted}%")
                
                embed.set_footer("Neura | NFT bot & Alpha group", ICON_URL)
                
                return embed
    except:
        
        pass
    
    return None

async def generate_cmv2_embed(url: str):
    
    global CM, IDS

    IDS = []
    CM = None

    scripts = get_scripts(url)

    if scripts:

        trs = []

        for script in scripts:

            getidsT = Thread(target=get_IDs,
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

                checkidsT = Thread(target=check_ID,
                                    args=[id],
                                    daemon=True)
                checkidsT.start()
                trs.append(checkidsT)

            for tr in trs:
                tr.join()

            if CM:

                embed = Embed(
                    color=EMBED_COLOR
                )

                metadata = await get_cm_metadata(CM, prog="v2")

                launch_date = int(metadata.data.go_live_date)
                items_available = metadata.data.items_available
                items_redeemed = metadata.items_redeemed
                price = float(metadata.data.price/(10**9))
                civic = ":white_check_mark:" if metadata.data.gatekeeper else ":x:"

                minted = str(int((items_redeemed/items_available) * 100))
                embed.add_field(name="**Candy Machine ID**", value=f"`{CM}`")
                embed.add_field(name="**Launch date**",
                                value=f"<t:{launch_date}>", inline=False)
                embed.add_field(name="**Civic**", value=civic, inline=False)
                embed.add_field(name="**Price**", value=str(price), inline=False)
                embed.add_field(name="**Available**",
                                value=str(items_available))
                embed.add_field(name="**Redeemed**", value=str(items_redeemed))
                embed.add_field(name="**Minted**", value=f"{minted}%")

                embed.set_footer("Neura | NFT bot & Alpha group", ICON_URL)
                
                return embed
            
@client.command(name="scrape")
async def scrape_collection(ctx, url: str):

    if CHANNEL_ID != int(ctx.channel.id):
        
        return
    
    if is_URL(url):
        
        if "magiceden.io" in url:
            
            embed = await generate_me_embed(url=url)     
        
        elif "launchmynft.io" in url:
            
            embed = await generate_lmn_embed(url=url)
        
        elif "monkelabs.io" in url:
            
            embed = await generate_ml_embed(url=url)
            
        else:
            
            embed = await generate_cmv2_embed(url=url)
            
        if embed:
                    
            await ctx.send(embed=embed)
                    
        else:
            
            await ctx.send(embed=create_error_embed("NO CMID FOUND FOR THIS MINT URL"))

    else:
        
        await ctx.send(embed=create_error_embed("INVALID MINT URL"))


@client.command(name="magiceden")
async def get_me_collection(ctx, symbol: str):
    
    if CHANNEL_ID != int(ctx.channel.id):
        
        return
    
    url = "https://magiceden.io/marketplace/" + symbol
    
    try:
        
        volumes = get_me_collection_stats(symbol)
        data = get_me_collection_info(symbol)
        
        if volumes and data:

            floor = float(volumes["floorPrice"]/(10**9))
            listed = int(volumes["listedCount"])
            avg_sale = float(volumes["avgPrice24hr"]/(10**9))
            volume = int(volumes["volumeAll"]/(10**9))
            
            img = data["image"]
            name = data["name"]
            
            socials = ""

            if "twitter" in data.keys() and data["twitter"]:
                twitter = data["twitter"]
                socials += f"[Twitter]({twitter}) "
            if "discord" in data.keys() and data["discord"]:
                discord = data["discord"]
                socials += f"[Discord]({discord}) "
            if "website" in data.keys() and data["website"]:
                website = data["website"]
                socials += f"[Webiste]({website}) "

            embed = Embed(
                color=EMBED_COLOR
            )
            
            embed.set_title(title=name, url=url)
            
            embed.add_field(name="**Floor**", value=str(floor) + " ◎")
            embed.add_field(name="**Listed**", value=str(listed), inline=False)
            embed.add_field(name="**Avg sale**", value=str(avg_sale) + " ◎", inline=False)
            embed.add_field(name="**Volume**", value=str(volume) + " ◎")
            
            embed.set_thumbnail(url=img)
            embed.set_footer("Neura | NFT bot & Alpha group", ICON_URL)
            
            if socials:
                
                embed.add_field(name="**Socials**", value=socials, inline=False)
            
            
            await ctx.send(embed=embed)
        
        else:
            
            await ctx.send(embed=create_error_embed("INVALID COLLECTION"))

    except:
        
        await ctx.send(embed=create_error_embed("ERROR WHILE FETCHING DATA"))

@client.command(name="coralcube")
async def get_cc_collection(ctx, symbol: str):

    if CHANNEL_ID != int(ctx.channel.id):
        
        return
    
    url = "https://coralcube.io/collection/" + symbol
    
    try:
        
        data = get_cc_collection_data(symbol)
        
        if data:

            floor = float(data["floor_price"]/(10**9))
            listed = int(data["listed_count"])
            volume = int(data["volume"]/(10**9))
            
            img = data["image"]
            name = data["name"]
            
            socials = ""

            if "twitter" in data.keys() and data["twitter"]:
                twitter = data["twitter"]
                socials += f"[Twitter]({twitter}) "
            if "discord" in data.keys() and data["discord"]:
                discord = data["discord"]
                socials += f"[Discord]({discord}) "
            if "website" in data.keys() and data["website"]:
                website = data["website"]
                socials += f"[Webiste]({website}) "

            embed = Embed(
                color=EMBED_COLOR
            )
            
            embed.set_title(title=name, url=url)
            
            embed.add_field(name="**Floor**", value=str(floor) + " ◎")
            embed.add_field(name="**Listed**", value=str(listed), inline=False)
            embed.add_field(name="**Volume**", value=str(volume) + " ◎")
            
            embed.set_thumbnail(url=img)
            embed.set_footer("Neura | NFT bot & Alpha group", ICON_URL)
            
            if socials:
                
                embed.add_field(name="**Socials**", value=socials, inline=False)
            
            
            await ctx.send(embed=embed)
        
        else:
            
            await ctx.send(embed=create_error_embed("INVALID COLLECTION"))

    except:
        
        await ctx.send(embed=create_error_embed("ERROR WHILE FETCHING DATA"))
    
@client.command(name="resetholder")
async def reset_holder(ctx, nft_mint: str):
    
    if CHANNEL_ID != int(ctx.channel.id):
        
        return
    
    try:
        
        database = NeuraDB(
            host="eu02-sql.pebblehost.com",
            user="customer_253216_neura",
            password="$7YDLyaCk-4zJpvkoLkU",
            database="customer_253216_neura"
        )
        
        neura_nfts = database.get_column_data("holders", "nft")

        if nft_mint in neura_nfts:
                
            success = database.clear_specific_hold(nft=nft_mint)
            
            if success:
                
                await ctx.send(embed=create_success_embed("HOLDER RESET SUCCESSFUL"))
            
            else:

                await ctx.send(embed=create_error_embed("HOLDER RESET FAILED"))
            
        else:
            
            await ctx.send(embed=create_error_embed("INVALID NEURA NFT ADDRESS"))
            
    
    except:
        
        await ctx.send(embed=create_error_embed("DATABASE UNREACHABLE"))
        
        return

    
client.run(token)
