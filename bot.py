import discord
from dotenv import load_dotenv
import logging
import os
from discord.ext import commands

extensions = [
    "cogs.clan_battle",
    "cogs.help"
]

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(filename='logs/bot.log', level=logging.INFO, format=formatter)

bot = commands.Bot(command_prefix="ちぇる")
bot.remove_command("help")

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    logging.info(f"Name: {bot.user.name}")
    logging.info(f"ID: {bot.user.id}")
    await bot.change_presence(activity=discord.Game(name="「ちぇるへるぷ」でヘルプが見れます。"))


@bot.event
async def on_command_error(ctx: commands.Context, exception):
    logging.error(f"ctx.message.content: {ctx.message.content}")
    logging.error(f"ctx.args: {ctx.args}")
    logging.error(f"ctx.command_failed: {ctx.command_failed}")
    if not ctx.command:
        return
    await ctx.channel.send(exception)

bot.run(DISCORD_BOT_TOKEN)
