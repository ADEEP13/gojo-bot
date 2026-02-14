import discord
from discord.ext import commands, tasks
import os
import psutil
import subprocess
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

previous_users = set()


# =========================
# EMBED CREATOR
# =========================
def create_embed(title, description, color=discord.Color.purple()):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.datetime.now()
    )

    if bot.user and bot.user.avatar:
        embed.set_thumbnail(url=bot.user.avatar.url)

    embed.set_footer(text="Gojo Server Guardian")
    return embed


# =========================
# OWNER CHECK
# =========================
def is_owner(user_id):
    return user_id == OWNER_ID


# =========================
# BOT READY EVENT
# =========================
@bot.event
async def on_ready():
    print(f"Gojo is ONLINE as {bot.user}")
    login_monitor.start()


# =========================
# LOGIN MONITOR
# =========================
@tasks.loop(seconds=10)
async def login_monitor():
    global previous_users

    result = subprocess.getoutput("who")
    current_users = set(result.splitlines())

    new_users = current_users - previous_users

    if new_users:
        channel = bot.get_channel(ALERT_CHANNEL_ID)

        if channel:
            for user in new_users:
                embed = create_embed(
                    "🔐 Login Detected",
                    f"User logged in:\n```{user}```",
                    discord.Color.green()
                )
                await channel.send(embed=embed)

    previous_users = current_users


# =========================
# COMMAND: STATUS
# =========================
@bot.command()
async def status(ctx):

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())

    embed = create_embed(
        "📊 Server Status",
        f"""
CPU Usage: {cpu}%
RAM Usage: {ram}%
Disk Usage: {disk}%
Uptime: {str(uptime).split('.')[0]}
        """,
        discord.Color.blue()
    )

    await ctx.send(embed=embed)


# =========================
# COMMAND: INFO
# =========================
@bot.command()
async def info(ctx):

    embed = create_embed(
        "🧠 Gojo Information",
        f"""
Bot Name: Gojo
Owner ID: {OWNER_ID}
Python Version: {os.sys.version.split()[0]}
Server: Online
        """,
        discord.Color.gold()
    )

    await ctx.send(embed=embed)


# =========================
# COMMAND: HELP
# =========================
@bot.command()
async def helpgojo(ctx):

    embed = create_embed(
        "📖 Gojo Commands",
        """
!status → Server status  
!info → Bot info  
!restart → Restart server (Owner only)  
!shutdown → Shutdown server (Owner only)  
!run <command> → Run Linux command (Owner only)  
        """,
        discord.Color.orange()
    )

    await ctx.send(embed=embed)


# =========================
# COMMAND: RESTART
# =========================
@bot.command()
async def restart(ctx):

    if not is_owner(ctx.author.id):
        await ctx.send(embed=create_embed("❌ Access Denied", "Owner only"))
        return

    await ctx.send(embed=create_embed("⚠ Restarting Server", "Please wait..."))

    os.system("sudo reboot")


# =========================
# COMMAND: SHUTDOWN
# =========================
@bot.command()
async def shutdown(ctx):

    if not is_owner(ctx.author.id):
        await ctx.send(embed=create_embed("❌ Access Denied", "Owner only"))
        return

    await ctx.send(embed=create_embed("⚠ Shutting down Server", "Powering off..."))

    os.system("sudo poweroff")


# =========================
# COMMAND: RUN LINUX COMMAND
# =========================
@bot.command()
async def run(ctx, *, command):

    if not is_owner(ctx.author.id):
        await ctx.send(embed=create_embed("❌ Access Denied", "Owner only"))
        return

    result = subprocess.getoutput(command)

    embed = create_embed(
        "💻 Command Output",
        f"```{result[:1900]}```",
        discord.Color.green()
    )

    await ctx.send(embed=embed)


# =========================
# START BOT
# =========================
bot.run(TOKEN)
