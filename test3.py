import discord
import requests



def check_dc_token(token: str):
    
    try:
                
        headers = {
            'authorization': token
        }

        return requests.get("https://discord.com/api/v7/users/@me", headers=headers).json()
        
    except:
        
        return None
    
    
    
print(check_dc_token("NDE5MDk3NjE3NDY1ODY4Mjg5.GlxA8N.j2y-0gFtvpbYXPsY5Yq7iFMy4pOA98PxgozYII"))