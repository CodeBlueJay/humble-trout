import discord, discum, re, os, sys
from lists import *

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = discum.Client(token='MTI3MzA2NDkxNTEyNDQ5MDMwMg.Gt9zKh.O0is9DcDhc-7SxAtKH0EKCJ5PcIuEbt96ayjx8', log=False)

class CountryModal(discord.ui.Modal):
    def __init__(self, title, field_name, embed, field_index, user_id, offers):
        super().__init__(title=title)
        self.field_name = field_name
        self.embed = embed
        self.field_index = field_index
        self.user_id = user_id
        self.offers = offers
        self.country_name = discord.ui.TextInput(label="Country Name", placeholder="Enter the country name")
        self.add_item(self.country_name)

    async def on_submit(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You can't edit this embed.", ephemeral=True)
            return
        self.offers.append(self.country_name.value)
        self.embed.set_field_at(self.field_index, name=self.field_name, value="\n".join(self.offers), inline=False)
        await interaction.response.edit_message(embed=self.embed)

class TradeView(discord.ui.View):
    def __init__(self, embed, user_id):
        super().__init__()
        self.embed = embed
        self.user_id = user_id
        self.your_offers = []
        self.their_offers = []

    @discord.ui.button(label="Add Your Balls", style=discord.ButtonStyle.primary)
    async def add_your_balls(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = CountryModal(title="Add Your Balls", field_name="Your offer", embed=self.embed, field_index=0, user_id=self.user_id, offers=self.your_offers)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Add Their Balls", style=discord.ButtonStyle.secondary)
    async def add_their_balls(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = CountryModal(title="Add Their Balls", field_name="Their offer", embed=self.embed, field_index=1, user_id=self.user_id, offers=self.their_offers)
        await interaction.response.send_modal(modal)

async def update_trade(message):
    embedVar = discord.Embed(title="Ballsdex Trading Comparison", description="Add balls down below", color=0x0000ff)
    embedVar.add_field(name="Your offer", value="*Empty*", inline=False)
    embedVar.add_field(name="Their offer", value="*Empty*", inline=False)
    view = TradeView(embed=embedVar, user_id=message.author.id)
    await message.channel.send(embed=embedVar, view=view)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith('!t') or message.content.startswith('!rarity'):
            parts = message.content.split(' ', 1)
            if len(parts) > 1:
                user_input = parts[1].strip().lower()
                full_name = alternate_names.get(user_input, user_input)
                full_name_key = full_name.lower()
                capitalized_full_name = full_name.title()
                if full_name_key in countryballs:
                    rarity = countryballs[full_name_key].capitalize()
                    await message.channel.send(f"{capitalized_full_name} is t{rarity}")
                else:
                    if user_input in countryballs:
                        capitalized_full_name = user_input.title()
                        rarity = countryballs[user_input]
                        await message.channel.send(f"{capitalized_full_name} is t{rarity}")
                    else:
                        await message.channel.send(f"{capitalized_full_name} is not a countryball.")
        elif message.content.startswith('!h'):
            embedVar = discord.Embed(title="Commands", description="List of commands", color=0x0000ff)
            embedVar.add_field(name="`!t <country>`, `!rarity <country>`", value="Get the rarity of a countryball", inline=False)
            embedVar.add_field(name="`!h`, `!help`", value="Get a list of commands", inline=False)
            embedVar.add_field(name="`!rates <country>`, `!r <country>`", value="Find the worth of a country in terms of T1", inline=False)
            embedVar.add_field(name="`!spawn-rates`", value="Get the spawn rates for shiny and mythical countryballs", inline=False)
            embedVar.add_field(name="`!check-trade`", value="Determine if a trade is W or L", inline=False)
            await message.channel.send(embed=embedVar)
        elif "You caught" in message.content:
            countryball = message.content.split("You caught")[1].split("!")[0]
            parts = message.content.split("You caught")[1].split("!")[1].strip().split(", ")
            countryball_id = parts[0].split("#")[1]
            stats = parts[1].split("/")
            stat1 = int(stats[0].replace('%', ''))
            stat2 = int(stats[1].replace('%', ''))
            net_stats = stat1 + stat2
            if net_stats >= -40 and net_stats <= -20:
                rating = "1"
            elif net_stats >= -19 and net_stats <= 0:
                rating = "2"
            elif net_stats >= 1 and net_stats <= 20:
                rating = "3"
            elif net_stats >= 21 and net_stats <= 40:
                rating = "4"
            user_input = countryball.lower()
            full_name = alternate_names.get(user_input, user_input)
            full_name_key = full_name.lower()
            capitalized_full_name = full_name.title()
            if full_name_key in countryballs:
                rarity = countryballs[full_name_key].capitalize()
            else:
                if user_input in countryballs:
                    capitalized_full_name = user_input.title()
                    rarity = countryballs[user_input]
            await message.channel.send(f"Countryball: `{countryball}`\nID: `{countryball_id}`\nRarity: `t{rarity}`\nStats: `{stat1}%/{stat2}%`\nNet Stats: `{net_stats}%`\nRating: `{rating}`")
        elif "!rates" in message.content or "!r" in message.content:
            parts = message.content.split(' ', 1)
            if len(parts) > 1:
                user_input_2 = parts[1].strip().lower()
                full_name_2 = alternate_names.get(user_input_2, user_input_2)
                full_name_key_2 = full_name_2.lower()
                capitalized_full_name_2 = full_name_2.title()
                
                if full_name_key_2 in countryballs:
                    rarity = countryballs[full_name_key_2]
                    if rarity in rates:
                        rate = rates[rarity]
                        await message.channel.send(f"{capitalized_full_name_2} is worth {rate}t1")
                    else:
                        await message.channel.send(f"Rarity {rarity} not found in rates.")
                else:
                    await message.channel.send(f"{capitalized_full_name_2} is not a countryball.")
        elif message.content.startswith("!spawn-rates"):
            embedVar = discord.Embed(title="Shiny and Mythical Spawn Rates", description="Spawn rates for shiny and mythical countryballs", color=0x0000ff)
            embedVar.add_field(name="Shiny", value="1/2048", inline=False)
            embedVar.add_field(name="Mythical", value="1/10000", inline=False)
            await message.channel.send(embed=embedVar)
        elif message.content.startswith("!check-trade"):
            await update_trade(message)

client.run('MTI3Mjc0NzA1NjIyMTUxOTkwNA.Gxn-We.QDzgqop3stBReopfsrod1ceGSswwNJmNe-tTRQ')
bot.gateway.run(auto_reconnect=True)