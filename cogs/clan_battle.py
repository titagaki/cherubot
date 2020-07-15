import config
import discord
from discord.ext import commands
import logging


class ClanBattle(commands.Cog):
    digit_emoji = (
        "\N{DIGIT ZERO}\N{COMBINING ENCLOSING KEYCAP}",
        "\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}",
        "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",
        "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}",
        "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",
        "\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}",
        "\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}",
        "\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}",
        "\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}",
        "\N{DIGIT NINE}\N{COMBINING ENCLOSING KEYCAP}",
    )

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config()
        self.data = ClanBattleData()

    @commands.command(name='ぼす', aliases=['ぼ'])
    async def boss(self, ctx):
        msg = await ctx.channel.send("今のボスは誰ですか？")

        for emoji in self.digit_emoji[1:6]:
            await msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        reaction_msg = reaction.message

        if user.id != self.bot.user.id and reaction_msg.author.id == self.bot.user.id:
            num = self.emoji_to_digit(reaction.emoji)
            if num is None:
                return

            boss_name = self.to_boss_name(num)
            if boss_name is None:
                return

            self.data.set(reaction_msg.guild, key="current_boss", val=num)

            logging.info(f"on_reaction_add():"
                         f" guild.id = {reaction_msg.guild.id}, member.id = {user.id}, boss_num = {num}")
            await self.notify(guild=reaction_msg.guild, channel=reaction_msg.channel, boss_num=num)
            msg = await reaction_msg.channel.send("%sですね。ありがとうございます先輩。" % boss_name)

            for emoji in self.digit_emoji[1:6]:
                await reaction_msg.remove_reaction(emoji, self.bot.user)

            for emoji in self.digit_emoji[1:6]:
                await msg.add_reaction(emoji)

    @commands.command(name='よび', aliases=['よ'])
    async def reserve(self, ctx, boss_num: int):
        boss_name = self.to_boss_name(boss_num)
        if boss_name is None:
            await ctx.channel.send("ちぇるよび [1〜5の数字]で入力をおねがいします。")
            return

        self.add_reserve(guild=ctx.guild, member=ctx.author, boss_num=boss_num)
        logging.info(f"reserve():"
                     f" guild.id = {ctx.guild.id}, member.id = {ctx.author.id}, boss_num = {boss_num}")
        await ctx.channel.send("わかりました。%sになったらお呼びしますね。" % boss_name)

    def add_reserve(self, guild, member, boss_num):
        if guild is None:
            return
        reserved_data = self.data.get(guild=guild, key='reserved')

        idx = boss_num - 1
        for m in reserved_data[idx]:
            if m.id == member:
                return
        reserved_data[idx].append(member)

    async def notify(self, guild, channel, boss_num):
        if guild is None:
            return
        reserved_data = self.data.get(guild=guild, key='reserved')
        idx = boss_num - 1

        if len(reserved_data[idx]) > 0:
            mention = []
            ids = []
            for m in reserved_data[idx]:
                mention.append(m.mention)
                ids.append(m.id)

            reserved_data[idx].clear()
            logging.info('notify(): ids = ' + ' '.join(map(str, ids)))
            await channel.send(' '.join(mention))

    def emoji_to_digit(self, emoji):
        if emoji in self.digit_emoji:
            return self.digit_emoji.index(emoji)
        return None

    def to_boss_name(self, num):
        clan_battle_boss_name = self.config.get('clan_battle_boss_name')
        if 1 <= num <= len(clan_battle_boss_name):
            return clan_battle_boss_name[num - 1]
        return None


class ClanBattleData:
    data = {}

    def init_data(self, guild):
        self.data[guild.id] = {
            'reserved': {i: [] for i in range(5)},
            'current_boss': None
        }

    def set(self, guild, key, val):
        if guild.id not in self.data.keys():
            self.init_data(guild)

        self.data[guild.id][key] = val

    def get(self, guild, key):
        if guild.id not in self.data.keys():
            self.init_data(guild)

        return self.data[guild.id][key]

    def get_all(self, guild):
        if guild.id not in self.data.keys():
            self.init_data(guild)

        return self.data[guild.id]


def setup(bot):
    bot.add_cog(ClanBattle(bot))
