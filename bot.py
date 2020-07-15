import discord
from dotenv import load_dotenv
import logging
import os
from discord.ext import commands

extensions = [
    "cogs.clan_battle"
]

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="ちぇる")

if __name__ == '__main__':
    for extension in extensions:
        print(f"extensions: {extensions}")
        bot.load_extension(extension)


@bot.event
async def on_ready():
    logging.info("Name: {}, ID: {}".format(bot.user.name, bot.user.id))


@bot.event
async def on_command_error(ctx: commands.Context, exception):
    logging.error(f"ctx.message.content: {ctx.message.content}")
    logging.error(f"ctx.args: {ctx.args}")
    logging.error(f"ctx.command_failed: {ctx.command_failed}")
    print(exception)
    if not ctx.command:
        return
    await ctx.channel.send(exception)

bot.run(DISCORD_BOT_TOKEN)
