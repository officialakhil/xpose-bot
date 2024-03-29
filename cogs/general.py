import discord
from discord.ext import commands
from cogs.utils.paginator import Pages
import itertools
import asyncio
from datetime import datetime
import config


class HelpPaginator(Pages):
    def __init__(self, help_command, ctx, entries, *, per_page=4):
        super().__init__(ctx, entries=entries, per_page=per_page)
        self.reaction_emojis.append(
            ("\N{BLACK QUESTION MARK ORNAMENT}", self.show_bot_help)
        )
        self.total = len(entries)
        self.help_command = help_command
        self.prefix = help_command.clean_prefix

    def get_bot_page(self, page):
        cog, description, commands = self.entries[page - 1]
        inst = self.bot.get_cog(cog)
        if hasattr(inst, "name"):
            self.title = f"{inst.name} Commands"
        else:
            self.title = f"{cog} Commands"
        self.description = description
        return commands

    def prepare_embed(self, entries, page, *, first=False):
        self.embed.clear_fields()
        self.embed.description = self.description
        self.embed.title = self.title

        # if self.get_page is self.get_bot_page:
        value = "For more help, please visit the [documentation](https://xposebot.com)."
        self.embed.add_field(name="Support", value=value, inline=False)

        self.embed.set_footer(
            text=f'Use "{self.prefix}help [command]" for more info on a command. | Designed by WCL Tech Team',
            icon_url=config.logo,
        )
        self.embed.set_thumbnail(url=config.logo)
        for entry in entries:
            signature = f"{self.prefix}{entry.qualified_name} {entry.signature}"
            self.embed.add_field(
                name=signature, value=entry.short_doc or "No help given", inline=False
            )

        if self.maximum_pages:
            self.embed.set_author(
                name=f"Page {page}/{self.maximum_pages} ({self.total} commands)"
            )

    async def show_help(self):
        """shows this message"""

        self.embed.title = "Paginator help"
        self.embed.description = "Hello! Welcome to the help page."

        messages = [f"{emoji} {func.__doc__}" for emoji, func in self.reaction_emojis]
        self.embed.clear_fields()
        self.embed.add_field(
            name="What are these reactions for?",
            value="\n".join(messages),
            inline=False,
        )

        self.embed.set_footer(
            text=f"We were on page {self.current_page} before this message."
        )
        await self.message.edit(embed=self.embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

    async def show_bot_help(self):
        """Shows how to use the bot"""

        self.embed.title = "Using the bot"
        self.embed.description = "Hello! Welcome to the help page."
        self.embed.clear_fields()

        entries = (
            ("<argument>", "This means the argument is __**required**__."),
            ("[argument]", "This means the argument is __**optional**__."),
            ("[A|B]", "This means the it can be __**either A or B**__."),
            (
                "[argument...]",
                "This means you can have multiple arguments.\n"
                "Now that you know the basics, it should be noted that...\n"
                "__**You do not type in the brackets!**__",
            ),
        )

        self.embed.add_field(
            name="How do I use this bot?",
            value="Reading the bot signature is pretty simple.",
        )

        for name, value in entries:
            self.embed.add_field(name=name, value=value, inline=False)

        self.embed.set_footer(
            text=f"We were on page {self.current_page} before this message."
        )
        await self.message.edit(embed=self.embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())


class PaginatedHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "cooldown": commands.Cooldown(1, 3.0, commands.BucketType.member),
                "help": "Shows help about the bot, a command, or a category",
            }
        )

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = "|".join(command.aliases)
            fmt = f"[{command.name}|{aliases}]"
            if parent:
                fmt = f"{parent} {fmt}"
            alias = fmt
        else:
            alias = command.name if not parent else f"{parent} {command.name}"
        return f"{alias} {command.signature}"

    async def send_bot_help(self, mapping):
        def key(c):
            return c.cog_name or "\u200bNo Category"

        bot = self.context.bot
        entries = await self.filter_commands(bot.commands, sort=True, key=key)
        nested_pages = []
        per_page = 9
        total = 0

        for cog, commands in itertools.groupby(entries, key=key):
            commands = sorted(commands, key=lambda c: c.name)
            if len(commands) == 0:
                continue
            if cog == "Jishaku":
                continue
            total += len(commands)
            actual_cog = bot.get_cog(cog)
            # get the description if it exists (and the cog is valid) or return Empty embed.
            description = (actual_cog and actual_cog.description) or discord.Embed.Empty
            nested_pages.extend(
                (cog, description, commands[i : i + per_page])
                for i in range(0, len(commands), per_page)
            )
        ordered_pages = sorted(nested_pages, key=lambda x: bot.get_cog(x[0]).position)
        # a value of 1 forces the pagination session
        pages = HelpPaginator(self, self.context, ordered_pages, per_page=1)

        # swap the get_page implementation to work with our nested pages.
        pages.get_page = pages.get_bot_page
        pages.total = total

        await pages.paginate()

    async def send_cog_help(self, cog):
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        pages = HelpPaginator(self, self.context, entries)
        pages.title = f"{cog.qualified_name} Commands"
        pages.description = cog.description

        await pages.paginate()

    def common_command_formatting(self, page_or_embed, command):
        page_or_embed.title = self.get_command_signature(command)
        if command.description:
            page_or_embed.description = f"{command.description}\n\n{command.help}"
        else:
            page_or_embed.description = command.help or "No help found..."

    async def send_command_help(self, command):
        # No pagination necessary for a single command.
        embed = discord.Embed(color=discord.Color.blue())
        self.common_command_formatting(embed, command)
        embed.set_thumbnail(url=config.logo)
        embed.set_footer(text="Designed by WCL Tech Team", icon_url=config.logo)
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)
        pages = HelpPaginator(self, self.context, entries)
        self.common_command_formatting(pages, group)

        await pages.paginate()


class General(commands.Cog):
    """General Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = PaginatedHelpCommand()
        bot.help_command.cog = self
        self.position = 5

    def cog_unload(self):
        self.bot.help_command = self.old_help_command

    @commands.command()
    async def ping(self, ctx):
        """Returns Bots Latency"""
        latency = int(self.bot.latency * 1000)
        embed = discord.Embed(
            title="Bot Latency",
            description=f"Pong! \U0001f3d3",
            colour=config.embed_color,
        )
        msg1 = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        new_embed = discord.Embed(
            title="Bot Latency",
            description=f"Pong! \U0001f3d3 Websocket Latency: {latency}ms",
            color=config.embed_color,
        )
        await msg1.edit(embed=new_embed)

    @commands.command()
    async def uptime(self, ctx):
        """Shows Bot Uptime"""
        embed = discord.Embed(
            title="Uptime", description=f"{self.bot.uptime}", color=config.embed_color
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
