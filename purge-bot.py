import json
from discord.ext import commands
from discord.utils import get
import discord
from dhooks import Embed, Webhook
from solana.rpc.api import Client
from datetime import datetime
import time

intents = discord.Intents.default()
intents.members = True

token = "OTM3NjYzMDU2NDcxNzg1NDgy.GLUXu3.3_c9RD6P7G6I2LG-ux_k7mgNSaSlP4paHg8i_U"

client = commands.Bot(command_prefix="%", intents=intents)

server_id = 910231756760829972

needed_roles = ["holder", "renewal"]


@client.event
async def on_ready():
            
    guild = client.get_guild(server_id)
    
    neuron_role = discord.utils.get(guild.roles, name="NEURON")

    for member in guild.members:
        
        user_roles = [role.name.lower() for role in member.roles]

        if all(role in user_roles for role in needed_roles):
            
            if "neuron" not in user_roles:
                
                await member.add_roles(neuron_role)
                
        else:
            
            if "neuron" in user_roles:
                
                await member.remove_roles(neuron_role)
    
    
    client.run(token)

