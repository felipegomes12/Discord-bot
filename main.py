import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

queues = {}
repeat_song = {}
repeat_queue = {}

YDL_OPTIONS = {'format': 'bestaudio', 'quiet': True}
FFMPEG_OPTIONS = {'options': '-vn'}

def get_queue(guild_id):
    if guild_id not in queues:
        queues[guild_id] = []
    return queues[guild_id]

async def play_next(ctx):
    guild_id = ctx.guild.id
    queue = get_queue(guild_id)
    vc = ctx.voice_client

    if repeat_song.get(guild_id):
       
        queue.insert(0, queue[0])
    elif repeat_queue.get(guild_id) and len(queue) == 0:
       
        queue[:] = repeat_queue[guild_id].copy()

    if len(queue) > 0:
        url, title = queue.pop(0)
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']

        vc.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS),
                after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        await ctx.send(f"🎶 Tocando agora: **{title}**")
    else:
        await ctx.send("✅ Fila finalizada!")

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send("Você precisa estar em um canal de voz!")
        return

    voice_channel = ctx.author.voice.channel
    vc = ctx.voice_client
    if vc is None:
        vc = await voice_channel.connect()

    if "youtube.com" in search or "youtu.be" in search:
        url = search
    else:
        await ctx.send("🔍 Pesquisando...")
        with yt_dlp.YoutubeDL({'format': 'bestaudio', 'quiet': True, 'noplaylist': True}) as ydl:
            info = ydl.extract_info(f"ytsearch5:{search}", download=False)['entries']

        results = [f"{i+1}. {v['title']}" for i, v in enumerate(info)]
        msg = await ctx.send("Escolha uma opção:\n" + "\n".join(results))

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit() and 1 <= int(m.content) <= len(info)

        try:
            reply = await bot.wait_for('message', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo esgotado.")
            return

        choice = int(reply.content) - 1
        url = info[choice]['webpage_url']

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'Desconhecido')

    queue = get_queue(ctx.guild.id)
    queue.append((url, title))

    await ctx.send(f"🎵 Adicionado à fila: **{title}**")

    if not ctx.voice_client.is_playing():
        await play_next(ctx)

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭ Pulando música atual...")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        queues[ctx.guild.id] = []
        await ctx.send("🛑 Bot desconectado e fila limpa!")

@bot.command()
async def clear(ctx):
    queues[ctx.guild.id] = []
    await ctx.send("🧹 Fila de músicas limpa!")

@bot.command()
async def repeat(ctx, mode: str = None):
    guild_id = ctx.guild.id
    if mode == "song":
        repeat_song[guild_id] = not repeat_song.get(guild_id, False)
        await ctx.send(f"🔁 Repetir música: {'ativado' if repeat_song[guild_id] else 'desativado'}")
    elif mode == "queue":
        repeat_queue[guild_id] = get_queue(guild_id).copy()
        await ctx.send("🔂 Repetição da playlist ativada.")
    else:
        await ctx.send("Use `!repeat song` ou `!repeat queue`")

@bot.command()
async def rickroll(ctx):
    await play(ctx, search="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
load_dotenv() 
TOKEN = os.getenv("DISCORD_TOKEN")

print(TOKEN)  
bot.run(TOKEN)
