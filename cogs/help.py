import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content in ['ちぇる']:
            await message.channel.send("ちぇるーん")

    @commands.command(name='へるぷ', aliases=['ぷ', '？', '?'])
    async def help(self, ctx):
        embed = discord.Embed(title="ヘルプ", description="コマンド一覧", color=0x00ffff)
        embed.add_field(name="**ちぇる**", value="ちぇるーん", inline=False)
        embed.add_field(name="**ちぇるぼす**", value="このコマンドを入力してボスを選んでください。", inline=False)
        embed.add_field(name="**ちぇるよび**", value="ボスが来たときに知らせる設定ができます。「ちぇるよび 2」のように入力してください。", inline=False)
        embed.add_field(name="**ちぇるへるぷ**", value="ヘルプを表示します。", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
