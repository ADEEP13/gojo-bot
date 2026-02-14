import discord
from discord.ext import commands
import os
import platform
import psutil
import socket
import time

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

start_time = time.time()

@bot.event
async def on_ready():
    print(f"Gojo is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Gojo is awake.")

@bot.command()
async def status(ctx):
    await ctx.send("Server is ONLINE")

@bot.command()
async def cpu(ctx):
    await ctx.send(f"CPU Usage: {psutil.cpu_percent()}%")

@bot.command()
async def ram(ctx):
    ram = psutil.virtual_memory()
    await ctx.send(f"RAM Usage: {ram.percent}%")

@bot.command()
async def uptime(ctx):
    uptime_seconds = int(time.time() - start_time)
    await ctx.send(f"Uptime: {uptime_seconds} seconds")

@bot.command()
async def ip(ctx):
    ip = socket.gethostbyname(socket.gethostname())
    await ctx.send(f"Server IP: {ip}")

bot.run(TOKEN)
