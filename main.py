import os
import discord
from dotenv import load_dotenv
from stuff import instructions, helps, wrong_channel, trade_init_msg, shop_init_msg, no_permission, \
    trade_introduction, shop_introduction
from other import get_role_names

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')


class DiscordCoinClient(discord.Client):
    trade_channel = None
    shop_channel = None

    async def get_balance(self, member):
        pass

    async def trade_add_item(self, member): # Эти три функции не могут работать из-за проблем с web3py
        pass

    async def shop_add_item(self, member):
        pass

    async def trade_init(self, c):
        trade_channel = c
        await trade_channel.send(trade_init_msg)
        await trade_channel.send(trade_introduction)

    async def shop_init(self, c):
        shop_channel = c
        await shop_channel.send(shop_init_msg)
        await shop_channel.send(shop_introduction)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(f'Hi, {member.name}! Notice that we have our currency on {guild}!')

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content == '!DSC help':
            response = f"We're always here to help you, {message.author}! \n{helps}"
            await message.channel.send(response)

        if message.content == '!DSC init':
            await message.author.create_dm()
            await message.author.dm_channel.send(f'Hi, {message.author}, here are the instructions:\n{instructions}')

        if message.content == '!DSC transact':
            if message.channel != message.author.dm_channel:
                response = f'Be careful, {message.author}! {wrong_channel}'
                await message.channel.send(response)
            else:
                response = f"Slug"
                await message.author.dm_channel.send(response)

        if message.content == '!DSC trade-init':
            if 'Всевышний' in get_role_names(message.author.roles):
                await self.trade_init(message.channel)
            else:
                response = no_permission
                await message.author.create_dm()
                await message.author.dm_channel.send(response)

        if message.content == '!DSC shop-init':
            if 'Всевышний' in get_role_names(message.author.roles):
                await self.shop_init(message.channel)
            else:
                response = no_permission
                await message.author.create_dm()
                await message.author.dm_channel.send(response)

        if message.content == '!DSC shop-add-item':
            if 'Всевышний' not in get_role_names(message.author.roles):
                response = no_permission
                await message.channel.send(response)
            elif message.channel != message.author.dm_channel:
                response = f'Be careful, {message.author}! {wrong_channel}'
                await message.channel.send(response)
            else:
                await self.shop_add_item()

        if message.content == '!DSC trade-add-item':
            if message.channel != message.author.dm_channel:
                response = f'Be careful, {message.author}! {wrong_channel}'
                await message.channel.send(response)
            else:
                await self.trade_add_item()

        if message.content == '!DSC get_balance':
            if message.channel != message.author.dm_channel:
                response = f'Be careful, {message.author}! {wrong_channel}'
                await message.channel.send(response)
            else:
                await self.get_balance(message.author)


client = DiscordCoinClient()
client.run(token)
