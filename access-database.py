from modules.neuradb import NeuraDB
import random
import string
import requests

API_KEY = 'sk_2jzfeU6qkb2BDuGHfDj89AJAYCe6chEu'

def get_license(license_key):

    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
            
        req = requests.get(f'https://api.metalabs.io/v4/licenses/{license_key}', headers=headers)
        
        if req.status_code == 200:
            
            return req.json()

        return None

    except:
        
        return None

def update_license(license_key, hardware_id):
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'metadata': {
            'hwid': hardware_id
        }
    }

    try:
            
        req = requests.patch(
            f'https://api.metalabs.io/v4/licenses/{license_key}',
            headers=headers,
            json=payload
        )

        if req.status_code == 200:
            
            return True

        return None
    
    except:
        
        return None


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



database = NeuraDB(
    host="eu02-sql.pebblehost.com",
    user="customer_253216_neura",
    password="$7YDLyaCk-4zJpvkoLkU",
    database="customer_253216_neura"
)


a = database.get_column_data("holders", "pubkey")


print(a)


