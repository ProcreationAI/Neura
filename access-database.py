from modules.neuradb import NeuraDB
import random
import string
import json
import theblockchainapi as api


API_LOG = ""
API_SECRET = ""


def get_cm_nfts(cmid):

    all_nfts = resource.get_all_nfts_from_candy_machine(
        candy_machine_id=cmid,
        network=api.SolanaNetwork.MAINNET_BETA
    )

    all_nfts = str(all_nfts).replace("'", '"').replace(
        "True", "true").replace("False", "false")

    j = json.loads(all_nfts)

    nfts = [nft_data["nft_metadata"]["mint"] for nft_data in j["minted_nfts"]]

    return nfts


def get_API():

    global API_LOG, API_SECRET

    resource = api.TheBlockchainAPIResource(

        api_key_id=API_LOG,
        api_secret_key=API_SECRET
    )

    return resource


def random_string(letter_count, digit_count):

    str1 = ''.join((random.choice(string.ascii_letters)
                   for x in range(letter_count)))
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1)
    random.shuffle(sam_list)
    final_string = "beta" + ''.join(sam_list)

    return final_string


def add_betas(num: int):

    betas = [random_string(10, 10) for _ in range(num)]
    
    success = database.add_betas(betas)

    with open("betas.txt", "w") as f:

        [f.write(f"{beta}\n") for beta in betas]

    return success


def add_nfts(cmid: str):

    nfts = get_cm_nfts(cmid)

    print(f"Found {len(nfts)} NFTs")

    success = database.add_nfts(nfts)

    return success


resource = get_API()

database = NeuraDB(
    host="eu02-sql.pebblehost.com",
    user="customer_253216_neura",
    password="$7YDLyaCk-4zJpvkoLkU",
    database="customer_253216_neura"
)


a = database.get_column_data("holders", "pubkey")


print(a)


