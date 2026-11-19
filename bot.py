from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Бот работает!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
import discord
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ВСТАВЬ СЮДА ID КАНАЛА ДЛЯ СВОДОК
ALERT_CHANNEL_ID = 1573082047289761813

# База городов и направлений
CITIES = ["Днепр", "Кривой Рог", "Киев", "Харьков", "Запорожье", "Полтаву", "Чернигов", "Сумы", "Павлоград", "Одессу"]
ORIGINS = ["Брянска", "Крыма", "Курска", "Воронежа", "Таганрога", "Приморско-Ахтарска", "Белгорода"]
DIRECTIONS = ["с севера", "с юга", "с востока", "с северо-востока", "с юго-востока", "с моря"]

async def send_embed(channel, title, text, color, ping=False):
    embed = discord.Embed(title=title, description=text, color=color)
    await channel.send(content="@here" if ping else "", embed=embed)

async def generate_random_event(channel):
    # БПЛА выпадают чаще всего, плюс реактивные, баллистика и крылатые
    attack_type = random.choice([
        "uav_mass", "uav_mass", "uav_single", "jet_uav", "jet_uav", "ballistic", "cruise_missile"
    ])
    city = random.choice(CITIES)
    direction = random.choice(DIRECTIONS)
    origin = random.choice(ORIGINS)

    # 1. МАССОВЫЕ ПУСКИ БПЛА (ШАХЕДЫ)
    if attack_type == "uav_mass":
        groups = random.randint(3, 10)
        await send_embed(channel, "🛸 ПУСКИ БПЛА", f"📡 Фиксируются массовые пуски шахедов из района **{origin}** (~{groups} групп).", 0xffa500, ping=True)
        
        await asyncio.sleep(random.randint(30, 70))
        await send_embed(channel, "🛸 ДВИЖЕНИЕ ЦЕЛЕЙ", f"⚠️ **Группы БПЛА на {city} {direction}!**", 0xffa500)
        
        await asyncio.sleep(random.randint(25, 50))
        await send_embed(channel, "🎯 ЗАХОД НА ЦЕЛЬ", f"🚨 **Шахеды на {city} — на удар!!** Всем в укрытия, работает ПВО!", 0xff4500)
        
        await asyncio.sleep(random.randint(20, 40))
        outcome = random.choice(["clean", "partial", "hit"])
        if outcome == "clean":
            await send_embed(channel, "🟢 ЧИСТО", f"✅ **Всё сбито! По {city} — чисто!**", 0x2ecc71)
        elif outcome == "partial":
            await send_embed(channel, "🟠 СБИТИЕ / ПРИЛЕТ", f"⚠️ Часть целей сбита ПВО, но есть **прилет в районе г. {city}**! Далее — чисто.", 0xe67e22)
        else:
            await send_embed(channel, "🔴 ПРИЛЕТ", f"💥 **Прилет в {city}!** Слышен мощный взрыв. По остальным целям — чисто.", 0xff0000)

    # 2. ОДИНОЧНЫЙ БПЛА
    elif attack_type == "uav_single":
        await send_embed(channel, "🛸 БПЛА", f"📡 БПЛА на **{city}** {direction}.", 0xffa500, ping=True)
        
        await asyncio.sleep(random.randint(20, 45))
        if random.random() < 0.65: # 65% шанс что собьют
            await send_embed(channel, "🟢 ЧИСТО", f"✅ **Сбит! По {city} — чисто.**", 0x2ecc71)
        else:
            await send_embed(channel, "🎯 НА УДАР", f"🚨 **БПЛА заходит на удар по {city}!**", 0xff4500)
            await asyncio.sleep(random.randint(8, 15))
            await send_embed(channel, "🔴 ПРИЛЕТ", f"💥 **Прилет в г. {city}!**", 0xff0000)

    # 3. РЕАКТИВНЫЙ БПЛА
    elif attack_type == "jet_uav":
        await send_embed(channel, "🔥 РЕАКТИВНЫЙ БПЛА", f"🚨 **Реактивный БПЛА {direction} в сторону {city}!** Очень быстро!", 0xff4500, ping=True)
        
        await asyncio.sleep(random.randint(12, 25))
        await send_embed(channel, "🎯 НА УДАР", f"⚡ **Реактивный БПЛА на {city} — НА УДАР!!**", 0xff0000)
        
        await asyncio.sleep(random.randint(10, 18))
        if random.random() < 0.55:
            await send_embed(channel, "🟢 ЧИСТО", f"✅ **Сбит на подлете! По {city} — чисто!**", 0x2ecc71)
        else:
            await send_embed(channel, "🔴 ПРИЛЕТ", f"💥 **Прилет реактивного БПЛА в г. {city}!**", 0xff0000)

    # 4. БАЛЛИСТИКА
    elif attack_type == "ballistic":
        await send_embed(channel, "🚀 БАЛЛИСТИКА", f"🚨 **Угроза баллистики с {origin}!**", 0xff0000, ping=True)
        
        await asyncio.sleep(random.randint(8, 18))
        if random.random() < 0.3: # 30% шанс что пуск был ложный / фальш-цель
            await send_embed(channel, "🟢 ЧИСТО", f"✅ **Локационно чисто!** Отбой баллистики.", 0x2ecc71)
        else:
            await send_embed(channel, "⚡ НА УДАР", f"🚀 **Выход баллистики! Ракета на {city} — НА УДАР!!**", 0xff0000)
            await asyncio.sleep(random.randint(10, 20))
            if random.random() < 0.4:
                await send_embed(channel, "🟢 ЧИСТО", f"✅ **Перехвачена ПВО! По {city} — чисто!**", 0x2ecc71)
            else:
                await send_embed(channel, "🔴 ПРИЛЕТ", f"💥 **Прилет баллистики в {city}!** Отбой угрозы.", 0xff0000)

    # 5. КРЫЛАТЫЕ РАКЕТЫ
    elif attack_type == "cruise_missile":
        await send_embed(channel, "✈️ ПУСКИ РАКЕТ", f"✈️ Пуски крылатых ракет из района **{origin}**.", 0xdc143c, ping=True)
        
        await asyncio.sleep(random.randint(25, 50))
        await send_embed(channel, "🎯 НА УДАР", f"🚨 **Крылатая ракета на {city} {direction} — НА УДАР!!**", 0xff0000)
        
        await asyncio.sleep(random.randint(15, 30))
        if random.random() < 0.7:
            await send_embed(channel, "🟢 ЧИСТО", f"✅ **Ракета сбита! По {city} — чисто!**", 0x2ecc71)
        else:
            await send_embed(channel, "🔴 ПРИЛЕТ", f"💥 **Прилет ракеты в г. {city}!**", 0xff0000)

async def random_loop():
    await bot.wait_until_ready()
    channel = bot.get_channel(ALERT_CHANNEL_ID)
    if not channel:
        print("❌ Канал не найден! Проверь ALERT_CHANNEL_ID.")
        return

    while not bot.is_closed():
        # Абсолютно случайное время между тревогами (от 5 до 60 минут)
        wait_seconds = random.randint(300, 3600)
        print(f"⏳ Следующая тревога через {wait_seconds // 60} мин. {wait_seconds % 60} сек.")
        await asyncio.sleep(wait_seconds)
        
        await generate_random_event(channel)

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} в сети! Мониторинг активен.")
    bot.loop.create_task(random_loop())

# Команда !тревога — запустить случайную атаку прямо сейчас
@bot.command(name="тревога")
@commands.has_permissions(administrator=True)
async def force_random(ctx):
    await ctx.message.delete()
    await generate_random_event(ctx.channel)

import os
bot.run(os.getenv("MTU3MzA1NDY2MjM2NDUwMDEyMA.GYakwW.rXlm7q1UI-hby6SViCdUUXsFi9X3QL9wUcBeUg"))
