import json
import requests
import re, uuid

hardware_id = ':'.join(re.findall('..', '%012x' % uuid.getnode()))


res = requests.post("http://192.168.1.52:8080/renewal-auth", json={
    "hwid": hardware_id,
    "license": "NEURA-28S9-CRM5-OADC-5CMQ"
})

res = res.json()

print(json.dumps(res, indent=3))

if res["success"]:
    
    username = res["license"]["user"]["username"]
    
    print(f"Welcome back, {username}!")