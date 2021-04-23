import discord
from discord.ext.commands import Bot
from discord.ext import commands
import os
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

  
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
               
@bot.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=discord.Color.red()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)

  await ctx.send(embed=embed)
  
  
@bot.command()
async def clear(ctx, amount=None):
    if amount is None:
        await ctx.channel.purge(limit=5)
    elif amount == "all":
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=int(amount))

@bot.command()
async def ban(ctx, member : discord.Member, reason=None):
    if reason == None:
        await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
    else:
        messageok = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.send(messageok)
        await member.ban(reason=reason)

@bot.command(alisases=['ub'])
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name,member_disc):

            await ctx.guild.unban(user)
            await ctx.send(member_name +"has been unbanned!")
            return

    await ctx.send(member+" was not found")
        
@bot.command()
async def kick(ctx, user: discord.Member, *, reason):
  await user.kick(reason=reason)
  
@bot.command()
async def userinfo(ctx, member: discord.Member):

    await ctx.send(f'User name: {member.name}, id: {member.id}')

    with requests.get(member.avatar_url_as(format='png')) as r:
        img_data = r.content
    with open(f'{member.name}.png', 'wb') as f:
        f.write(img_data)

@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)



#Fun commands
@bot.command()
async def rps(ctx, user_choice):
    rpsGame = ['rock', 'paper', 'scissors']
    if user_choice.lower() in rpsGame:
        await ctx.send(f'Choice: `{user_choice}`\nBot Choice: `{random.choice(rpsGame)} you lost`')
    elif user_choice.lower() not in rpsGame:
        await ctx.send('**Error** This command only works with rock, paper, or scissors.')


@bot.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses =['As I see it, yes.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                'Don’t count on it.',
                'It is certain.',
                'It is decidedly so.',
                'Most likely.',
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Outlook good.',
                'Reply hazy, try again.',
                'Signs point to yes.',
                'Very doubtful.',
                'Without a doubt.',
                'Yes.',
                'Yes – definitely.',
                'You may rely on it.']
    responce = random.choice(responses)
    await ctx.send(f'Question: {question}\nAnswer: {responce}')



@bot.command()
async def say(ctx, *, question):
    await ctx.message.delete()
    await ctx.send(f'{question}')   
                                                                                 
@bot.event
async def on_ready():
    activity = discord.Game(name="Play ! for help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready!")

bot.run(os.environ["Disc_Token"])
