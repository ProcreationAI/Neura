import json
import cloudscraper
from solana.keypair import Keypair
from solana.publickey import PublicKey
from anchorpy import Program, Wallet, Provider
from solana.rpc.async_api import AsyncClient
import requests
from bs4 import BeautifulSoup
import asyncio
from dhooks import Embed, Webhook
import time

try:
    
    from lib import AccountClient
    
except:
    
    from idl_fetcher import AccountClient
    
async def get_account_metadata(name: str, account: str, prog: str):

    try:

        program = None

        if prog == "CMZYPASGWeTz7RNGHaRJfCq2XQ5pYK6nDvVQxzkH51zb":

            program_id = PublicKey(
                "CMZYPASGWeTz7RNGHaRJfCq2XQ5pYK6nDvVQxzkH51zb")

        elif prog == "cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ":

            program_id = PublicKey(
                "cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ")

        elif prog == "ArAA6CZC123yMJLUe4uisBEgvfuw2WEvex9iFmFCYiXv":
            
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
        
        candyMachine = await AccountClient.fetch_custom(program.account[name], PublicKey(account))

        await program.close()
        await client.close()

        return candyMachine

    except:
                
        await client.close()

        if program:

            await program.close()

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

sol_rpc = "https://api.mainnet-beta.solana.com"
scraper = cloudscraper.create_scraper()


headers = {
    'Accept': '*/*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://www.launchmynft.io',
    'Referer': 'https://www.launchmynft.io/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
    'X-Meili-API-Key': '3ee2cafe84ad0f0a28b2e8aea31df1f0e7adeed45973b24f0ab60307da150383',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

json_data = {
    'facetsDistribution': [
        'type',
    ],
    'attributesToCrop': [
        'description:50',
    ],
    'filter': [
        [
            'type="Solana"',
        ],
        'soldOut = false',
    ],
    'attributesToHighlight': [
        '*',
    ],
    'limit': 1,
    'sort': [
        'deployed:desc',
    ],
    'q': '',
}

last_collection = None

webhook = "https://discord.com/api/webhooks/981326567613538336/l4SjS3_jC8BDm0PGjHqx1ziV1lP0yfH65hzMTIcnze9pJkb2ARlnCuQQQ6fzrexpHeuF"

while True:
    
    collection = scraper.post('https://search.launchmynft.io/indexes/collections/search', headers=headers, json=json_data).json()["hits"][0]

    if collection.get("description") and collection.get("collectionCoverUrl") and collection.get("collectionBannerUrl"):
        
        id = collection["id"]
        
        if last_collection is None or id != last_collection:
            
            last_collection = id
            
            name = collection["collectionName"]
            owner = collection["owner"]
            description = collection["description"]
            
            url = f"https://www.launchmynft.io/collections/{owner}/{id}"
            
            cmid = get_lmn_candy_machine(url=url)

            if cmid:
                
                metadata = asyncio.run(get_account_metadata(name="CandyMachine", account=cmid, prog="ArAA6CZC123yMJLUe4uisBEgvfuw2WEvex9iFmFCYiXv"))
                
                if metadata:

                    supply = metadata.data.items_available
                    price = metadata.data.price
                    date = metadata.data.go_live_date
                    mints_per_user = metadata.data.mints_per_user or ":infinity:"
                    whitelist = ":white_check_mark:" if metadata.data.whitelist else ":x:"

                    try:    
                        
                        metadata_url = metadata.data.base_url
                        
                        res = requests.get(metadata_url + "/0.json").json()
                        
                        nft_img = res["image"]
                        
                    except:
                        
                        metadata_url = None
                        
                    if metadata_url:
                            
                        embed = Embed(
                            color=0x6436CB,
                            description=description
                        )
                        
                        embed.set_title(title=name, url=url)
                        
                        embed.add_field(name="**Candy Machine ID**", value=f"`{cmid}`", inline=False)
                        embed.add_field(name="**Creator**", value=f"`{owner}`", inline=False)
                        embed.add_field(name="**Supply**", value=str(supply))
                        embed.add_field(name="**Price**", value=str(price/(10**9)))
                        embed.add_field(name="**Date**", value=f"<t:{date}>", inline=False)
                        embed.add_field(name="**Wallet limit**", value=str(mints_per_user))
                        embed.add_field(name="**Whitelist**", value=str(whitelist))
                    
                        embed.set_thumbnail(url=nft_img)
                        
                        Webhook(webhook).send(embed=embed)
    time.sleep(10)