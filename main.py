print("Загружаю библиотеки")
import httpx

from datetime import datetime
import aiohttp
from aiohttp import BasicAuth
import traceback
import os
import sys
import random
import platform
import termcolor
from cfonts import render
from pyfiglet import Figlet
from datetime import datetime, timezone
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import asyncio
import re
import time
import logging
from telethon import TelegramClient, events, functions, types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest, UpdateStatusRequest
from telethon.tl.types import UserStatusOffline, UserStatusOnline
import hashlib
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import (
    InputPeerUser, InputPeerChannel,
    InputReportReasonSpam, InputReportReasonPornography, InputReportReasonViolence,
    InputReportReasonChildAbuse, InputReportReasonCopyright, InputReportReasonFake,
    InputReportReasonGeoIrrelevant, InputReportReasonOther
)
from bs4 import BeautifulSoup
from io import BytesIO
import shutil
from pathlib import Path
from uuid import uuid4
import configparser
from yt_dlp import YoutubeDL
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
from art import text2art
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                           InlineKeyboardMarkup, InlineKeyboardButton)

# ==================== ЗАГРУЗКА КОНФИГУРАЦИИ ====================
def load_config():
    config = {}
    try:
        with open('config.txt', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key.strip()] = value.strip().strip('"\'')
    except FileNotFoundError:
        print("Файл конфигурации не найден!")
        sys.exit(1)
    return config

config = load_config()
api_id = int(config.get('api_id', 0))
api_hash = config.get('api_hash', '')
phone_number = config.get('phone_number', '')
session_name = config.get('session_name', 'session')
BOT_USERNAME = config.get('BOT_USERNAME', '')
STAT_BOT_USERNAME = config.get('STAT_BOT_USERNAME', '')
ai_model = config.get('ai_model', '')
ENABLE_FR_AI = str(config.get('ENABLE_FR_AI', False)).lower() == "true"

client = TelegramClient(session_name, api_id, api_hash)


# ==================== КЛАСС ПРОВЕРКИ ЛИЦЕНЗИЙ ====================
import hashlib
import platform
import aiohttp
import asyncio
from datetime import datetime, timezone

class LicenseChecker:
    def __init__(self):
        self.license_url = "https://fenst4r.life/.netlify/functions/check"
        # другие нужные атрибуты, например
        self.colors = {
            'error': "\033[91m",
            'success': "\033[92m",
            'warning': "\033[93m",
            'info': "\033[94m",
            'reset': "\033[0m"
        }
        self.license_confirmed = False
        self._auto_check_task = None




    def get_hwid(self) -> str:
        sys_info = platform.uname()
        hwid_str = f"{sys_info.system}-{sys_info.node}-{sys_info.release}-{sys_info.machine}"
        return hashlib.sha256(hwid_str.encode()).hexdigest()

    async def check_license(self, user_id: int) -> bool:
        return True

    def print_error(self, message): print(f"{self.colors['error']}{message}{self.colors['reset']}")
    def print_success(self, message): print(f"{self.colors['success']}{message}{self.colors['reset']}")
    def print_warning(self, message): print(f"{self.colors['warning']}{message}{self.colors['reset']}")

    async def _auto_check_loop(self, user_id: int, interval_sec: int = 300):
        while True:
            await self.check_license(user_id)
            await asyncio.sleep(interval_sec)

    def start_auto_check(self, user_id: int, interval_sec: int = 300):
        if self._auto_check_task is None or self._auto_check_task.done():
            self._auto_check_task = asyncio.create_task(self._auto_check_loop(user_id, interval_sec))

# ==================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ====================
OWNER_USER_ID = None
last_vip_status = None
last_notified_expiry = None
KEY = b'0123456789abcdef0123456789abcdef'  # 32 bytes
IV = b'abcdef9876543210'  # 16 bytes
PROTECTED_USER_ID = 7404596587
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
pending_dox_requests = {}
auto_sms_targets = {}
muted_users = set()
bite_targets = {}
pending_downloads = {}
active_floods = {}

# ==================== ДЕКОРАТОРЫ ДОСТУПА ====================
def vip_only(func):
    async def wrapper(event):
        try:
            is_vip = await license_checker.is_vip(event.sender_id)
            expiry = await license_checker.get_vip_expiry(event.sender_id)
            
            if not is_vip:
                await event.respond(
                    f"🚫 Требуется VIP-статус\n"
                    f"Ваш статус: неактивен\n"
                    f"Окончание: {expiry}\n\n"
                    f"Купить VIP: @error_kill"
                )
                return
                
            return await func(event)
            
        except Exception as e:
            await event.respond(f"⚠️ Ошибка проверки VIP: {str(e)}")
    return wrapper

def owner_only(func):
    async def wrapper(event):
        if not await is_admin(event.sender_id):
            await event.respond("🚫 У вас нет прав на выполнение данной команды.")
            return
        return await func(event)
    return wrapper

async def is_admin(user_id):
    return user_id == OWNER_USER_ID

# ==================== ИНИЦИАЛИЗАЦИЯ БОТА ====================
license_checker = LicenseChecker()

async def init_bot():
    global OWNER_USER_ID
    
    await client.start(phone=phone_number)
    me = await client.get_me()
    OWNER_USER_ID = me.id
    
    asyncio.create_task(monitor_license())

    if not await license_checker.check_license(OWNER_USER_ID):
        print(f"{license_checker.colors['error']}❌ Скрипт остановлен.")
        print(f"Купить лицензию: @error_kill{license_checker.colors['reset']}")
        await client.disconnect()
        exit()

async def monitor_license():
    last_license_status = True

    while True:
        await asyncio.sleep(60)
        current_status = await license_checker.check_license(OWNER_USER_ID)

        if current_status != last_license_status:
            last_license_status = current_status

            if not current_status:
                print("❌ Лицензия аннулирована! Скрипт завершает работу.")
                await client.disconnect()
                os._exit(0)

    checker = LicenseChecker()
    asyncio.run(checker.periodic_check(user_id))
# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================
def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

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
    for text in ['LiteHack', 'V18']:
        output = render(text, colors=['magenta'], align='center')
        print(output)

def show_random_quote():
    quote = get_lol_quote()
    words = quote.split()
    colored_quote = " ".join([termcolor.colored(word, 'magenta') for word in words])
    print(colored_quote + " - Кто-то")
    print()

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

def image_to_ascii(img, width=80):
    img = img.convert("L")
    aspect_ratio = img.height / img.width
    new_height = int(aspect_ratio * width * 0.5)
    img = img.resize((width, new_height))
    pixels = np.array(img)

    ascii_str = ""
    for row in pixels:
        for pixel in row:
            p = int(pixel)
            index = min(p * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)
            ascii_str += ASCII_CHARS[index]
        ascii_str += "\n"
    return ascii_str

def render_text_to_image(text, font_size=40):
    font = ImageFont.load_default()
    dummy_img = Image.new("L", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    img = Image.new("L", (text_width + 10, text_height + 10), color=255)
    draw = ImageDraw.Draw(img)
    draw.text((5, 5), text, font=font, fill=0)
    return img

async def get_gif_url(query):
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
            return gif_link["src"]
        else:
            return None
    
    except Exception as e:
        logging.error(f"Ошибка при парсинге Giphy: {e}")
        return None

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

# ==================== КОМАНДЫ БОТА ====================
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
                decrypted_text = decrypt_json(encrypted_bytes, KEY, IV)
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

@client.on(events.NewMessage(pattern=r'^fr!ascii (.+)$'))
@owner_only
async def ascii_art_handler(event):
    text = event.pattern_match.group(1)
    
    if re.search('[а-яА-Я]', text):
        await event.respond("Ошибка: русский текст не поддерживается, используйте только латиницу и цифры.")
        return
    
    ascii_text = Figlet().renderText(text)
    response = f"```\n {ascii_text[:1999]}{'...' if len(ascii_text) > 1999 else ''}\n```"
    await event.respond(response, parse_mode='markdown')

@client.on(events.NewMessage(pattern=r'^fr!myvip$'))
async def check_vip_status(event):
    is_vip = await license_checker.is_vip(event.sender_id)
    expiry = await license_checker.get_vip_expiry(event.sender_id)
    
    status = "💎 VIP активен" if is_vip else "🚫 VIP неактивен"
    await event.respond(
        f"{status}\n"
        f"🔢 Ваш ID: `{event.sender_id}`\n"
        f"📅 Окончание: {expiry}\n"
        f"🖥️ HWID: `{license_checker.get_hwid()}`",
        parse_mode='markdown'
    )
    
@client.on(events.NewMessage(pattern=r'^fr!readall$'))
@owner_only
async def read_all_handler(event):
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.unread_count > 0:
            await client.send_read_acknowledge(dialog.entity)
    await event.respond("✅ Все сообщения помечены как прочитанные")

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

@client.on(events.NewMessage(pattern=r'^fr!dox(?: (.*))?'))
@owner_only
async def dox_command(event):
    args = event.pattern_match.group(1)
    
    if not args:
        await event.respond("❌ Укажите информацию для поиска: fr!dox <ник/имя/номер>")
        return
    
    try:
        if args.startswith('@'):
            args = f"t.me/{args[1:]}"
        
        await send_to_bot(client, event, BOT_USERNAME, args)
        
        if event.is_reply:
            replied_msg = await event.get_reply_message()
            await client.forward_messages(BOT_USERNAME, replied_msg)
            
    except Exception as e:
        await event.respond(f"❌ Ошибка: {str(e)}")

@client.on(events.NewMessage(pattern=r'^fr!gif '))
@owner_only
async def gif_command(event):
    query = event.message.text[6:].strip()
    
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

@client.on(events.NewMessage(pattern=r'^fr!snos(?: (.*))?'))
@owner_only
@vip_only
async def snos_handler(event):
    global process

    args = event.pattern_match.group(1)

    if process is None:
        # Определяем путь и проверяем существование файла
        script_path = os.path.join('addons', 'snos.py')
        if not os.path.exists(script_path):
            await event.respond("❌ Файл snos.py не найден в папке addons/")
            logging.error(f"Файл не найден: {script_path}")
            return

        try:
            # Создаем процесс
            process = await asyncio.create_subprocess_exec(
                sys.executable, script_path,  # Используем текущий интерпретатор Python
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(script_path)  # Рабочая директория - где лежит скрипт
            )

            # Создаем сообщение для вывода
            message = await event.respond("🚀 Запускаю сносер...")

            async def handle_output():
                """Обработка вывода подпроцесса"""
                while True:
                    if process.stdout.at_eof():
                        break
                    line = await process.stdout.readline()
                    if line:
                        try:
                            text = line.decode('utf-8').strip()
                        except UnicodeDecodeError:
                            text = line.decode('cp1251', errors='ignore').strip()
                        
                        if text:
                            try:
                                await message.edit(f"```\n{text}\n```")
                            except:
                                # Если не удалось отредактировать, отправляем новое сообщение
                                message = await event.respond(f"```\n{text}\n```")

            async def handle_stderr():
                """Обработка ошибок подпроцесса"""
                while True:
                    if process.stderr.at_eof():
                        break
                    line = await process.stderr.readline()
                    if line:
                        error_text = line.decode('utf-8', errors='ignore').strip()
                        if error_text:
                            logging.error(f"[SNOS ERROR] {error_text}")

            # Запускаем обработчики
            asyncio.create_task(handle_output())
            asyncio.create_task(handle_stderr())

            logging.info("Сносер успешно запущен")
            
        except Exception as e:
            await event.respond(f"❌ Ошибка запуска: {str(e)}")
            logging.exception("Ошибка запуска сносера")
            process = None
            return

    # Если переданы аргументы - отправляем их в процесс
    if args:
        try:
            if process.stdin.is_closing():
                await event.respond("❌ Процесс завершился или недоступен")
                process = None
                return
                
            process.stdin.write(f"{args}\n".encode('utf-8'))
            await process.stdin.drain()
            logging.info(f"Отправлена команда в сносер: {args}")
            
            # Удаляем сообщение с командой
            try:
                await event.delete()
            except Exception as delete_error:
                logging.warning(f"Не удалось удалить сообщение: {delete_error}")
                
        except Exception as e:
            await event.respond(f"❌ Ошибка отправки команды: {str(e)}")
            logging.exception("Ошибка отправки команды в сносер")
@client.on(events.NewMessage(pattern=r'^fr!sn_crash$'))
@owner_only
@vip_only
async def snos_crash_handler(event):
    global process

    if process is None:
        await event.respond("❌ Процесс сноса не запущен.")
        return

    try:
        process.terminate()
        await process.wait()
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

@client.on(events.NewMessage(pattern=r'^fr!video (.+)$'))
@owner_only
async def handle_video_request(event):
    chat_id = event.chat_id
    user_input = event.pattern_match.group(1).strip()

    url = user_input if user_input.startswith('http') else f"ytsearch1:{user_input}"

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

        if info.get('thumbnail'):
            await client.send_file(chat_id, info['thumbnail'])

        caption = (
            f"📹 Название: {info.get('title', 'Без названия')}\n"
            f"👤 Автор: {info.get('uploader', 'Неизвестен')}\n"
            f"⏱ Длительность: {info.get('duration', 0)} сек\n\n"
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
                    f"⏱ Длительность: {info.get('duration', 0)} сек\n"
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

@client.on(events.NewMessage(pattern=r'^fr!music (yt|sc) (.+)$'))
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
    args = event.pattern_match.group(1)
    is_id = event.pattern_match.group(2)

    if not args:
        await event.respond("❌ Укажите username или ID: fr!tg <ник> или fr!tg <ID> id")
        return

    query = args if is_id else args.lstrip('@')

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
        async with client.conversation(STAT_BOT_USERNAME) as conv:
            await conv.send_message(query if is_id else f"@{query}")

            while True:
                try:
                    response = await conv.get_response(timeout=30)
                    if not ("⏳" in response.text or "📊 Статистика" in response.text):
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

@client.on(events.NewMessage(pattern=r'^fr!edit (\d{1,2}) (.+)$'))
async def handler_edit(event):
    try:
        count = int(event.pattern_match.group(1))
        new_text = event.pattern_match.group(2)

        async for msg in client.iter_messages(event.chat_id, from_user='me', limit=count + 1):
            if msg.id != event.id:
                await msg.edit(new_text)
        await event.delete()
    except Exception as e:
        await event.reply(f"Ошибка при редактировании: {e}")

@client.on(events.NewMessage(pattern=r'^fr!del (\d+)$'))
async def handler_delete(event):
    try:
        count = int(event.pattern_match.group(1))
        deleted = 0
        cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        messages_to_delete = []

        async for msg in client.iter_messages(event.chat_id, from_user='me', limit=count * 2):
            if msg.date < cutoff:
                continue
            messages_to_delete.append(msg)
            if len(messages_to_delete) >= count:
                break

        if not messages_to_delete:
            await event.respond("Не найдено подходящих сообщений для удаления.")
            return

        for msg in messages_to_delete:
            try:
                await client.delete_messages(event.chat_id, msg)
                deleted += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                await event.reply(f"Не удалось удалить сообщение {msg.id}: {e}")

        await event.respond(f"Удалено {deleted} сообщений.")
    except Exception as e:
        await event.reply(f"Ошибка при удалении: {e}")

@client.on(events.NewMessage(pattern=r'^fr!autotype$'))
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

@client.on(events.NewMessage(pattern=r'^fr!mute$'))
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

@client.on(events.NewMessage(pattern=r'^fr!report$'))
@owner_only
async def report_user(event):
    if event.is_reply:
        try:
            replied_msg = await event.get_reply_message()
            reason = InputReportReasonSpam()
            
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

@client.on(events.NewMessage(pattern=r'^fr!love$'))
@owner_only
async def send_love(event):
    hearts = ['❤️', '💕', '💖', '💗', '💘', '💝', '💞', '💓']
    message = await event.respond("Создаю анимацию сердечек...")
    
    for _ in range(10):
        heart = random.choice(hearts)
        try:
            await message.edit(heart * 10)
            await asyncio.sleep(0.5)
        except Exception as e:
            logging.error(f"Ошибка в анимации: {e}")
            break

@client.on(events.NewMessage(pattern=r'^fr!roll$'))
async def roll_dice(event):
    result = random.randint(1, 6)
    await event.respond(f"🎲 Результат броска: {result}")

@client.on(events.NewMessage(pattern=r'^fr!help$'))
async def help_handler(event):
    help_text = (
        "**📖 Справка по командам (без пасхалок):**\n\n"

        "**💡 Основные команды:**\n"
        "`fr!ping` — Проверка отклика\n"
        "`fr!id` — Получить свой ID и ID чата\n"
        "`fr!ascii <текст>` — ASCII арт (латиница)\n"
        "`fr!readall` — Прочитать все сообщения\n\n"
        
        "**🎭 Внешность и статус:**\n"
        "`fr!anim 😺 0.3` — Анимация имени и био\n\n"

        "**💬 Утилиты:**\n"
        "`fr!gif <запрос>` — Поиск гифки\n"
        "`fr!dox <инфо>` — DOX запрос через бот\n"
        "`fr!tg <username|id>` — Стата Telegram\n\n"

        "**📦 Видео и музыка:**\n"
        "`fr!video <ссылка или запрос>` — Скачать видео\n"
        "`fr!music yt <название>` — Музыка с YouTube\n"
        "`fr!music sc <название>` — Музыка с SoundCloud\n\n"

        "**💬 Автосообщения и байт:**\n"
        "`fr!автосмс <текст>` — В ответ: включить автосообщение\n"
        "`fr!автосмсстоп` — Отключить автосообщение\n"
        "`fr!байт` — Ответить оскорблением (в ответ)\n"
        "`fr!байтстоп` — Отключить байт\n\n"

        "**🧠 ИИ:**\n"
        "`fr!AI <вопрос>` — Ответ от AI (если включено)\n"
        "`fr!ArtI - Прокомментировать\n\n"

        "**👨‍💻 Dev/admin (для владельца):**\n"
        "`fr!admin` — Настройки админов\n"
        "`fr!edit <N> <текст>` — Изменить N последних сообщений\n"
        "`fr!del <N>` — Удалить N последних сообщений\n"
        "`fradmin!` — Админ-панель (доступ для админов)\n\n"

        "**🛠 Скрипты (addons):**\n"
        "`fr!snos [команда]` — Запуск сноса\n"
        "`fr!sn_crash` — Краш сноса\n"
        "`fr!promostart` — Генерация промо\n"
        "`fr!promoplus` — Генерация промо Яндекс\n\n"

        "🔒 Команды с `@vip_only` работают только при активной VIP-лицензии.\n"
        "👑 Купить лицензию: @error_kill"
    )
    await event.respond(help_text, parse_mode='markdown')

@client.on(events.NewMessage(pattern=r'^fr!data(?:\s+(\S+))?(?:\s+(.+))?'))
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
        if '..' in filename or '/' in filename or '\\' in filename:
            await event.respond("❌ Недопустимое имя файла")
            return

    keyword = keyword.upper()
    found = False
    results = []

    base_dir = os.path.join(os.path.dirname(__file__), 'databases')

    if filename == 'all':
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
                continue

    else:
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
        "Версия: RELEASE 18\n\n"
        "Создатель/Программист: @error_kill\n"
        "Помощник/Программист: RonZ\n"
        "Тестер: @roskomnadzor333, @SWLGTEAM все кого мучал в лс в чатах командами)\n"
        "Фразы: @error_kill, @tous111, Открытые источники.\n\n"
        "[fenst4r 2025]\n\n"
        "Для полной работоспособности боту нужен VPN. Я использую @S1GyMAVPNBOT"
    )
    await event.respond(info_message)
    
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

import requests
import json
from telethon import events



import json
import requests
from telethon import events, functions



BACKUP_FILE = 'backup_profile.json'

def save_backup_profile(profile):
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

def load_backup_profile():
    if not os.path.exists(BACKUP_FILE):
        return None
    with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

profiles = {
    "code": (
        'Ты — NEIROST4R, помощник для управления Telegram через юзербота, который возвращает только JSON с действиями: '
        'edit_message (message_id, text), send_message (text), reply (message_id, text), delete_message (message_id), '
        'pin_message (message_id), unpin_message (message_id), update_bio (text), update_username (username), '
        'update_name (first_name, last_name), send_photo (file, caption), change_chat_title (title). '
        'Всегда возвращай валидный JSON {"actions":[...]}, без текста и пояснений. Используй профиль "code" для ответа.'
    )
}

API_URL = "https://fenst4r.life/api/ai"
MODEL_NAME = "openai/gpt-4.1"


async def ask_ai(message: str, profile: str = "code") -> dict:
    import subprocess

    json_data = json.dumps({
        "model": MODEL_NAME,
        "profile": profile,
        "message": message
    }, ensure_ascii=False)
    
    print(f"Отправляем нейросети: {json_data}")

    cmd = [
        "curl",
        "-s",
        "-X", "POST",
        API_URL,
        "-H", "Content-Type: application/json",
        "-d", json_data
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"Ошибка curl: {stderr.decode().strip()}")

    raw_response = stdout.decode('utf-8')

    # --- Отладочный вывод ---
    print(f"DEBUG raw_response: {raw_response}")
    
    raw_response = raw_response.replace("'", '"')
    
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON от AI: {e}\nОтвет: {raw_response}")

    if "reply" in data:
        raw_reply = data["reply"].strip()
    elif "choices" in data:
        raw_reply = data["choices"][0]["message"]["content"].strip()
    else:
        raise ValueError(f"В ответе от AI нет ключей 'reply' или 'choices'. Ответ: {raw_response}")

    start = raw_reply.find('{')
    end = raw_reply.rfind('}') + 1
    if start == -1 or end == -1:
        raise ValueError(f"Ответ AI не содержит валидный JSON: {raw_reply}")

    clean_json_str = raw_reply[start:end]

    try:
        actions_json = json.loads(clean_json_str)
        return actions_json
    except json.JSONDecodeError:
        raise ValueError(f"Ответ AI не является валидным JSON после очистки: {clean_json_str}")



async def get_user_profile(client, user_id):
    full = await client(functions.users.GetFullUserRequest(user_id))
    user = full.user if hasattr(full, 'user') else None
    bio = getattr(full, "about", "") or ""  # Получаем био
    profile = {
        "username": getattr(user, "username", "") if user else "",
        "first_name": getattr(user, "first_name", "") if user else "",
        "last_name": getattr(user, "last_name", "") if user else "",
        "bio": bio,
    }
    return profile


async def get_chat_history(client, chat_id, limit=20):
    messages = []
    async for msg in client.iter_messages(chat_id, limit=limit):
        sender = await msg.get_sender()
        sender_name = sender.first_name if sender else "Unknown"
        text = msg.text or "<медиа/стикер/другое>"
        messages.append(f"{sender_name}: {text}")
    messages.reverse()
    return "\n".join(messages)


import json
import logging

# Настроим логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




import json
import logging
from telethon import events, functions

# Логирование
logging.basicConfig(level=logging.DEBUG)


# Путь к логам
LOG_FILE = 'change_logs.txt'
BACKUP_FILE = 'backup_profile.json'

# Логирование изменений
def log_change(action_type, details):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{action_type}: {details}\n")

def clear_log():
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("")  # Очистка файла

# Сохранение и загрузка профиля
def save_backup_profile(profile):
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

def load_backup_profile():
    if not os.path.exists(BACKUP_FILE):
        return None
    with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Константы для API
MODEL_NAME = "jamba-large"  # Название модели
API_URL = "https://fenst4r.life/api/ai_v2"  # URL для API

# Обработка запроса к нейросети
async def ask_ai(message: str, profile: str = "code") -> dict:
    import subprocess

    json_data = json.dumps({
        "model": MODEL_NAME,
        "profile": profile,
        "message": message
    }, ensure_ascii=False)

    cmd = [
        "curl",
        "-s",
        "-X", "POST",
        API_URL,
        "-H", "Content-Type: application/json",
        "-d", json_data
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"Ошибка curl: {stderr.decode().strip()}")

    raw_response = stdout.decode('utf-8')
    print(f"DEBUG raw_response: {raw_response}")

    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON от AI: {e}\nОтвет: {raw_response}")

    if "reply" in data:
        raw_reply = data["reply"].strip()
    elif "choices" in data:
        raw_reply = data["choices"][0]["message"]["content"].strip()
    else:
        raise ValueError(f"В ответе от AI нет ключей 'reply' или 'choices'. Ответ: {raw_response}")

    # Попробуем очистить строку и вернуть валидный JSON
    start = raw_reply.find('{')
    end = raw_reply.rfind('}') + 1
    if start == -1 or end == -1:
        raise ValueError(f"Ответ AI не содержит валидный JSON: {raw_reply}")

    clean_json_str = raw_reply[start:end]

    try:
        actions_json = json.loads(clean_json_str)
        return actions_json
    except json.JSONDecodeError:
        raise ValueError(f"Ответ AI не является валидным JSON после очистки: {clean_json_str}")

async def execute_actions(event, actions):
    results = []  # Инициализация списка результатов
    logging.debug(f"DEBUG actions: {json.dumps(actions, ensure_ascii=False, indent=2)}")  # Логируем входные данные

    def log_and_add_result(action_type, result, message):
        log_change(action_type, message)
    
    def check_params(action_type, required_params, params):
        for param in required_params:
            if param not in params:
                results.append(f"⚠️ Не указан параметр '{param}' для действия {action_type}.")
                logging.warning(f"Не указан параметр '{param}' для действия {action_type}.")
                return False
        return True

    for action in actions.get("actions", []):
        if not isinstance(action, dict) or len(action) != 1:
            results.append(f"⚠️ Некорректный формат действия: {action}")
            logging.warning(f"Некорректный формат действия: {action}")
            continue
        
        action_type = list(action.keys())[0]
        params = action[action_type]

        try:
            if action_type == "send_message":
                if not check_params(action_type, ["text"], params):
                    continue
                sent = await event.client.send_message(event.chat_id, params["text"])

            elif action_type == "reply":
                if not check_params(action_type, ["message_id", "text"], params):
                    continue
                await event.client.send_message(event.chat_id, params["text"], reply_to=params["message_id"])

            elif action_type == "edit_message":
                if not check_params(action_type, ["message_id", "text"], params):
                    continue
                await event.client.edit_message(event.chat_id, params["message_id"], params["text"])

            elif action_type == "delete_message":
                if not check_params(action_type, ["message_id"], params):
                    continue
                await event.client.delete_messages(event.chat_id, params["message_id"])

            elif action_type == "send_file":
                if not check_params(action_type, ["file"], params):
                    continue
                await event.client.send_file(event.chat_id, params["file"])

            elif action_type == "kick_user":
                if not check_params(action_type, ["user_id"], params):
                    continue
                await event.client.kick_participant(event.chat_id, params["user_id"])

            elif action_type == "unban_user":
                if not check_params(action_type, ["user_id"], params):
                    continue
                await event.client.unban_participant(event.chat_id, params["user_id"])

            elif action_type == "pin_message":
                if not check_params(action_type, ["message_id"], params):
                    continue
                await event.client.pin_message(event.chat_id, params["message_id"])

            elif action_type == "unpin_message":
                if not check_params(action_type, ["message_id"], params):
                    continue
                await event.client.unpin_message(event.chat_id, params["message_id"])

            elif action_type == "add_participant":
                if not check_params(action_type, ["user_id"], params):
                    continue
                await event.client.add_participant(event.chat_id, params["user_id"])

            elif action_type == "block_user":
                if not check_params(action_type, ["user_id"], params):
                    continue
                await event.client.block_user(params["user_id"])

            elif action_type == "unblock_user":
                if not check_params(action_type, ["user_id"], params):
                    continue
                await event.client.unblock_user(params["user_id"])

            elif action_type == "get_chat_info":
                chat_info = await event.client.get_entity(event.chat_id)
                results.append(f"📝 Информация о чате: {chat_info.title} (ID: {chat_info.id})")

            elif action_type == "get_user_info":
                if not check_params(action_type, ["user_id"], params):
                    continue
                user_info = await event.client.get_entity(params["user_id"])
                results.append(f"📝 Информация о пользователе: {user_info.username} (ID: {user_info.id})")

            elif action_type == "get_messages":
                if not check_params(action_type, ["limit"], params):
                    continue
                messages = await event.client.get_messages(event.chat_id, limit=params["limit"])
                for msg in messages:
                    results.append(f"📩 Сообщение: {msg.text} (ID: {msg.id})")

            elif action_type == "send_poll":
                if not check_params(action_type, ["question", "options"], params):
                    continue
                poll = await event.client.send_poll(event.chat_id, params["question"], params["options"], is_anonymous=True)
                results.append(f"🗳️ Опрос отправлен: {poll.id}")

            elif action_type == "delete_chat":
                await event.client.delete_chat(event.chat_id)

            elif action_type == "set_title":
                if not check_params(action_type, ["title"], params):
                    continue
                await event.client.edit_chat(event.chat_id, title=params["title"])

            elif action_type == "add_admin":
                if not check_params(action_type, ["user_id"], params):
                    continue
                await event.client.edit_admin(event.chat_id, params["user_id"], is_admin=True)

            elif action_type == "remove_admin":
                if not check_params(action_type, ["user_id"], params):
                    continue
                await event.client.edit_admin(event.chat_id, params["user_id"], is_admin=False)

            elif action_type == "send_sticker":
                if not check_params(action_type, ["sticker"], params):
                    continue
                await event.client.send_sticker(event.chat_id, params["sticker"])

            elif action_type == "forward_message":
                if not check_params(action_type, ["message_id", "to_chat"], params):
                    continue
                await event.client.forward_messages(params["to_chat"], event.chat_id, params["message_id"])

            elif action_type == "edit_username":
                if not check_params(action_type, ["username"], params):
                    continue
                await event.client.edit_profile(username=params["username"])

            else:
                results.append(f"⚠️ Неизвестное действие: {action_type}")
                logging.warning(f"Неизвестное действие: {action_type}")

        except Exception as exc:
            logging.error(f"Ошибка при выполнении действия {action_type}: {exc}")
            results.append(f"❌ Ошибка выполнения действия {action_type}: {exc}")

    if results:
        await event.reply("\n".join(results))  # Отправляем ответ с результатами


# Пример хендлера для команды fr!AI
@client.on(events.NewMessage(pattern=r'^fr!AI(?: (.+))?$'))
async def fr_ai_handler(event):
    user_message = event.pattern_match.group(1) or "Привет, что сделать?"
    
    # Заменяем реальные переводы строк на символы \n для передачи в нейросеть
    user_message = user_message.replace('\n', '\\n')

    # Получаем актуальный профиль пользователя
    profile = await get_user_profile(event.client, event.sender_id)

    # Собираем информацию для контекста: имя, фамилию, био
    user_bio = profile["bio"]
    user_first_name = profile["first_name"]
    user_last_name = profile["last_name"]
    user_username = profile["username"]

    # История чатов (по желанию можно добавлять в контекст)
    history_text = await get_chat_history(event.client, event.chat_id)

    # Формируем контекст для нейросети
    context = f"История изменений профиля: {load_backup_profile()}\nЗапрос от пользователя: {user_message}\nДанные пользователя: Имя: {user_first_name} Фамилия: {user_last_name} Био: {user_bio} Юзернейм: {user_username}"

    try:
        actions = await ask_ai(context)  # Отправляем запрос с контекстом
        await execute_actions(event, actions)  # Выполняем действия на основе ответа
    except Exception as e:
        await event.reply(f"❌ Ошибка запроса к AI: {e}")
        return

# Функция для получения последних сообщений
async def get_chat_history(client, chat_id, limit=5):
    messages = await client.get_messages(chat_id, limit=limit)
    return "\n".join([msg.text for msg in messages])

# Обработчик команды fr!AI
@client.on(events.NewMessage(pattern=r'^fr!ArtI(?: (.+))?$'))
async def fr_ai_handler(event):
    user_message = event.pattern_match.group(1) or "Что сделать?"

    # Получаем последние 5 сообщений чата
    history_text = await get_chat_history(event.client, event.chat_id, limit=5)

    # Формируем контекст для нейросети
    context = f"История сообщений:\n{history_text}\nЗапрос от пользователя: {user_message}"

    try:
        actions = await ask_ai(context)  # Отправляем запрос с контекстом
        await execute_actions(event, actions)  # Выполняем действия на основе ответа
    except Exception as e:
        await event.reply(f"❌ Ошибка запроса к AI: {e}")
        return
        
# Функция для получения профиля пользователя
async def get_user_profile(client, user_id):
    full = await client(functions.users.GetFullUserRequest(user_id))

    # Получаем данные о пользователе
    user = full.users[0] if full.users else None
    bio = getattr(user, "about", "") or "Био не указано"
    first_name = getattr(user, "first_name", "Имя не указано")
    last_name = getattr(user, "last_name", "Фамилия не указана")
    username = getattr(user, "username", "Юзернейм не указан")

    # Собираем информацию в строку
    user_info = f"Имя: {first_name} {last_name}\nЮзернейм: {username}\nБио: {bio}"

    logging.debug(f"User Info: {user_info}")

    # Возвращаем профиль в виде словаря
    profile = {
        "bio": bio,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "user_info": user_info  # Собранная строка
    }
    return profile





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

@client.on(events.NewMessage(pattern=r'^fr!license$'))
async def license(event):
    license_message = (
        f"✅ Лицензия верифицирована FENST4R на сервере.\n"
        f"Для перепроверки напишите @error_kill.\n"
        f"ID юзера-хоста для проверки: `{OWNER_USER_ID}`"
    )
    await event.respond(license_message)

# ==================== ЗАПУСК БОТА ====================
async def main():
    try:
        clear_screen()
        print_ascii_titles()
        print(termcolor.colored("ʟɪᴛᴇʜᴀᴄᴋ ʙʏ @error_kill", "magenta", attrs=["bold"]))
        show_random_quote()

        print(termcolor.colored("Загрузка параметров по умолчанию...", "magenta", attrs=["bold"]))
        print(termcolor.colored("Загрузка юзербота...", "magenta", attrs=["bold"]))
        print("")

        await init_bot()
        print(f"\n{license_checker.colors['success']}✅ Бот успешно запущен")
        print(f"ID аккаунта: {OWNER_USER_ID}{license_checker.colors['reset']}\n")

        # Первая проверка лицензии при старте
        is_valid = await license_checker.check_license(OWNER_USER_ID)
        if not is_valid:
            print("❌ Лицензия не подтверждена. Выход...")
            return

        # Регулярная проверка лицензии раз в 5 минут
        while True:
            await asyncio.sleep(300)  # 300 секунд = 5 минут
            is_valid = await license_checker.check_license(OWNER_USER_ID)
            if not is_valid:
                print("❌ Лицензия перестала быть действительной. Останавливаю бота.")
                # Здесь можно добавить код остановки или выхода
                return

    except Exception as e:
        print(f"⚠️ Ошибка в главном цикле: {e}")


if __name__ == '__main__':
    client.loop.run_until_complete(main())
