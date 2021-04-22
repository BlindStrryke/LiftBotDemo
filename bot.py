import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='!', help_command=None)   
bot.remove_command('help')

@bot.command()
async def help(ctx, args=None):
    help_embed = discord.Embed(title="My Bot's Help!")
    command_names_list = [x.name for x in bot.commands]

    # If there are no arguments, just list the commands:
    if not args:
        help_embed.add_field(
            name="List of supported commands soon coming soon! more commands :",
            value="\n".join([str(i+1)+". "+x.name for i,x in enumerate(bot.commands)]),
            inline=False
        )
        help_embed.add_field(
            name="Details",
            value="Type `.help <command name>` for more details about each command.",
            inline=False
        )

    # If the argument is a command, get the help text from that command:
    elif args in command_names_list:
        help_embed.add_field(
            name=args,
            value=bot.get_command(args).help
        )

    # If someone is just trolling:
    else:
        help_embed.add_field(
            name="Nope.",
            value="Don't think I got that command, boss!"
        )

    await ctx.send(embed=help_embed)
