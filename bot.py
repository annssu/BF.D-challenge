import discord
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)

WATCH_CHANNEL_ID = 1480785301487091823
TODO_CHANNEL_ID = 1482922299647725792
TODO_EMOJI = "✅"

@client.event
async def on_ready():
    print(f"봇 실행 중: {client.user}")

@client.event
async def on_raw_reaction_add(payload):
    # ✅ 이모지인지 확인
    if str(payload.emoji) != TODO_EMOJI:
        return

    # 감시 채널인지 확인
    if payload.channel_id != WATCH_CHANNEL_ID:
        return

    # 메시지 가져오기
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # 이미 투두에 추가된 메시지인지 확인 (중복 방지)
    todo_channel = client.get_channel(TODO_CHANNEL_ID)

    # 투두 채널에 전송
    author = message.author.display_name
    content = message.content
    message_url = message.jump_url

    embed = discord.Embed(
        description=content,
        color=0x57F287
    )
    embed.set_author(name=author, icon_url=message.author.display_avatar.url)
    embed.add_field(name="원본 메시지", value=f"[바로가기]({message_url})", inline=False)

    await todo_channel.send("✅ 새 투두 항목", embed=embed)

client.run(os.environ["DISCORD_TOKEN"])
