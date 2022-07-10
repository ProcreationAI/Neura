import requests
import time

def send_message(channel_id: int, msg: str):
    
    try:
        
        payload = {
            "content": msg
        }
        
        res = requests.post(f"https://discord.com/api/v7/channels/{channel_id}/messages", headers=headers, json=payload)
        
        return res.status_code == 200
    
    except Exception as e:
        
        print(e)
        
def add_role(user_id: int, role_id: int):
    
    try:

        res = requests.put(f"https://discord.com/api/v7/guilds/{server_id}/members/{user_id}/roles/{role_id}", headers=headers)
        
        return res.status_code == 200
    
    except Exception as e:
        
        print(e)
        
        return None
    
def remove_role(user_id: int, role_id: int):
    
    try:
        
        res = requests.delete(f"https://discord.com/api/v7/guilds/{server_id}/members/{user_id}/roles/{role_id}", headers=headers)
        
        return res.status_code == 200
    
    except Exception as e:
        
        print(e)
        
        return None

def get_members():
    
    params = {
        "limit": 1000
    }
    
    try:
        
        res = requests.get(f"https://discord.com/api/v7/guilds/{server_id}/members", headers=headers, params=params)

        return res.json() if res.status_code == 200 else None
       
    except Exception as e:
        
        print(e)
        
        return None
        
        
needed_roles = [995039308975190086, 995039332882714705]

neuron_role = 934453813828534294

server_id = 910231756760829972

logs_channel_id = 921022038074871879

token = "OTM3NjYzMDU2NDcxNzg1NDgy.GLUXu3.3_c9RD6P7G6I2LG-ux_k7mgNSaSlP4paHg8i_U"

headers = {
    'authorization': "Bot " + token
}


while True:
        
    members = get_members()

    for member in members:

        user_roles = [int(role) for role in member["roles"]]
        user_id = int(member["user"]["id"])
        
        if all(role in user_roles for role in needed_roles):
            
            if neuron_role not in user_roles:

                add_role(user_id=user_id, role_id=neuron_role)
                
        else:
            
            if neuron_role in user_roles:
                
                remove_role(user_id=user_id, role_id=neuron_role)
    
    time.sleep(3)
    
