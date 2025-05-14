import os
import discord
from discord import app_commands
from wakeonlan import send_magic_packet
from dotenv import load_dotenv

load_dotenv()
# 環境変数読み込み
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEVICES = {
        "desktop": "9C:6B:00:51:D0:9F"
}

class WolBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user}')

bot = WolBot()

@bot.tree.command(name="wol", description="Wake-on-LANでデバイスを起動")
@app_commands.describe(device="起動するデバイス名")
async def wol_command(interaction: discord.Interaction, device: str):
    # デバイス確認
    if (mac := DEVICES.get(device.lower())) is None:
        return await interaction.response.send_message(
            f"無効なデバイス名です\n有効: {', '.join(DEVICES.keys())}",
            ephemeral=True
        )

    # WoL送信
    try:
        send_magic_packet(mac)
        await interaction.response.send_message(f"⚡ {device} を起動中...")
    except Exception as e:
        await interaction.response.send_message(f"❌ エラー: {str(e)}")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

