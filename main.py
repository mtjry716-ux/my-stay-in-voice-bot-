import discord
import asyncio
import os

TOKEN = os.environ.get("DISCORD_TOKEN") 
try:
    TARGET_VOICE_CHANNEL_ID = int(os.environ.get("VOICE_ID"))
except (ValueError, TypeError):
    print("خطأ فادح: لم يتم العثور على VOICE_ID أو أنه ليس رقماً صحيحاً.")
    exit()

if not TOKEN:
    print("خطأ فادح: لم يتم العثور على DISCORD_TOKEN.")
    exit()

class SelfBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_channel_id = TARGET_VOICE_CHANNEL_ID
        self.voice_client = None

    async def on_ready(self):
        print(f'تم تسجيل الدخول بنجاح كـ {self.user}')
        await self.join_voice_channel()

    async def join_voice_channel(self):
        while True:
            try:
                channel = self.get_channel(self.target_channel_id)
                if not isinstance(channel, discord.VoiceChannel):
                    print(f"خطأ: الـ ID لا يعود لروم صوتي.")
                    await asyncio.sleep(60)
                    continue

                if self.voice_client and self.voice_client.is_connected():
                    print(f"الحساب متصل بالفعل بـ: {self.voice_client.channel.name}")
                else:
                    print(f"جاري محاولة الانضمام إلى: {channel.name}")
                    self.voice_client = await channel.connect(reconnect=True, timeout=60)
                    print(f"تم الانضمام بنجاح.")
                
                await asyncio.sleep(300) # تحقق كل 5 دقائق

            except asyncio.CancelledError:
                print("تم إيقاف البوت.")
                break
            except Exception as e:
                print(f"حدث خطأ: {e}. جاري محاولة إعادة الاتصال بعد 30 ثانية...")
                if self.voice_client:
                    await self.voice_client.disconnect(force=True)
                    self.voice_client = None
                await asyncio.sleep(30)

intents = discord.Intents.default()
bot = SelfBot(intents=intents)

try:
    bot.run(TOKEN, bot=False) 
except Exception as e:
    print(f"فشل تشغيل البوت. تأكد من أن التوكن صحيح. الخطأ: {e}")
