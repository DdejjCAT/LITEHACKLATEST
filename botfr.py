import os
import sys
import subprocess
import platform
import hashlib
import requests
import shutil
import io
import zipfile
from prompt_toolkit.shortcuts import (
    radiolist_dialog, message_dialog, yes_no_dialog, input_dialog
)
from prompt_toolkit.styles import Style

COMMANDS_FILE = "commands.json"
OPTIONS_FILE = "config.txt"
MAIN_PY = "main.py"

REQUIREMENTS = [
    "telethon", "aiohttp", "termcolor", "cfonts", "pyfiglet",
    "cryptography", "yt_dlp", "Pillow", "numpy", "beautifulsoup4",
    "aiogram", "colored", "pystyle", "selenium", "art", "text2art",
    "transformers", "llama-cpp-python", "torch", "tensorflow", "requests"
]

style = Style.from_dict({
    "dialog":             "bg:#2a0050 #dcdcdc",
    "dialog frame-label": "bg:#1c1c1c #b28ddb bold",
    "button":             "bg:#1c1c1c #b28ddb",
    "button-arrow":       "bg:#1c1c1c #b28ddb",
    "button focused":     "bg:#5a00a0 #000000 bold",
    "radiolist":          "#dcdcdc",
    "radiolist focused":  "bg:#5a00a0 #000000",
    "text-area":          "bg:#1c1c1c #dcdcdc",
    "dialog.body":        "bg:#2a0050 #dcdcdc",
})

def save_default_commands():
    if not os.path.exists(COMMANDS_FILE):
        data = {
            "fr!edit": {"enabled": True, "whitelist": []},
            "fr!del": {"enabled": True, "whitelist": []},
            "fr!flood": {"enabled": True, "whitelist": []}
        }
        with open(COMMANDS_FILE, "w") as f:
            import json
            json.dump(data, f, indent=2)

def create_default_options():
    if not os.path.exists(OPTIONS_FILE):
        with open(OPTIONS_FILE, "w") as f:
            f.write("""\
phone_number = 
api_id = 
api_hash = 
session_name = 
BOT_USERNAME = 
STAT_BOT_USERNAME = 
ai_model = 
ENABLE_FR_AI = 
""")

def install_requirements():
    for lib in REQUIREMENTS:
        subprocess.call([sys.executable, "-m", "pip", "install", lib, "--break-system-packages"])

def toggle_command_access():
    save_default_commands()
    import json
    with open(COMMANDS_FILE, "r") as f:
        data = json.load(f)

    cmd = input_dialog(title="Команда", text="Введите команду (например, fr!edit):", style=style).run()
    if not cmd:
        return
    if cmd not in data:
        data[cmd] = {"enabled": True, "whitelist": []}

    current = data[cmd]["enabled"]
    enable = yes_no_dialog(
        title="Доступ",
        text=f"Команда '{cmd}' сейчас {'ВКЛ' if current else 'ВЫКЛ'}. Включить?",
        style=style
    ).run()

    data[cmd]["enabled"] = enable
    with open(COMMANDS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    message_dialog(title="Готово", text=f"Команда '{cmd}' обновлена.", style=style).run()

def configure_access():
    save_default_commands()
    import json
    with open(COMMANDS_FILE, "r") as f:
        data = json.load(f)

    cmd = input_dialog(title="Команда", text="Введите команду:", style=style).run()
    if not cmd or cmd not in data:
        message_dialog(title="Ошибка", text="Команда не найдена.", style=style).run()
        return

    uid = input_dialog(title="ID пользователя", text="Введите ID (число):", style=style).run()
    if uid and uid.isdigit():
        uid = int(uid)
        if uid not in data[cmd]["whitelist"]:
            data[cmd]["whitelist"].append(uid)
            with open(COMMANDS_FILE, "w") as f:
                import json
                json.dump(data, f, indent=2)
            message_dialog(title="Готово", text=f"ID {uid} добавлен в whitelist команды '{cmd}'.", style=style).run()

def install_():
    import requests, zipfile, io, os, shutil

    repo_zip_url = "https://github.com/DdejjCAT/LITEHACKADDONS/archive/refs/heads/main.zip"
    local_addons_dir = "addons"

    try:
        resp = requests.get(repo_zip_url)
        resp.raise_for_status()
        zip_bytes = io.BytesIO(resp.content)

        with zipfile.ZipFile(zip_bytes) as z:
            # Очистка папки addons
            if os.path.exists(local_addons_dir):
                shutil.rmtree(local_addons_dir)
            os.makedirs(local_addons_dir, exist_ok=True)

            for file in z.namelist():
                # Файлы в корне архива addons ветки, без вложенных папок
                # Пример: LITEHACKLATEST-addons/ivi.py
                parts = file.split('/')
                if len(parts) == 2 and parts[0] == "LITEHACKLATEST-addons" and file.endswith(".py"):
                    filename = parts[1]
                    target_path = os.path.join(local_addons_dir, filename)
                    with z.open(file) as source, open(target_path, "wb") as target:
                        shutil.copyfileobj(source, target)

        message_dialog(title="✅ Аддоны", text="Аддоны успешно установлены из ветки addons!", style=style).run()
    except Exception as e:
        message_dialog(title="❌ Ошибка", text=f"Не удалось установить аддоны:\n{e}", style=style).run()

def show_online_readme():
    url = "https://raw.githubusercontent.com/DdejjCAT/LITEHACKLATEST/main/README.md"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        readme_text = response.text.strip()

        if not readme_text:
            raise ValueError("README пуст")

        # Ограничим длину на всякий случай
        max_length = 5000
        if len(readme_text) > max_length:
            readme_text = readme_text[:max_length] + "\n\n... (обрезано)"

        message_dialog(title="📘 README с GitHub", text=readme_text, style=style).run()

    except Exception as e:
        message_dialog(title="❌ Ошибка", text=f"Не удалось загрузить README.md:\n{e}", style=style).run()


def self_update_launcher():
    import requests, hashlib, sys, os
    from pathlib import Path

    url = "https://raw.githubusercontent.com/DdejjCAT/LITEHACKLATEST/main/botfr.py"
    launcher_path = Path(__file__)
    temp_path = launcher_path.with_suffix(".new")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        remote_code = response.content
        remote_hash = hashlib.sha256(remote_code).hexdigest()
    except Exception as e:
        print(f"[❌] Не удалось получить обновление лаунчера:\n{e}")
        return

    try:
        with open(launcher_path, "rb") as f:
            local_code = f.read()
        local_hash = hashlib.sha256(local_code).hexdigest()

        if remote_hash == local_hash:
            return  # Нет обновлений
    except Exception as e:
        print(f"[⚠️] Ошибка при проверке лаунчера:\n{e}")
        # Продолжаем обновление на всякий случай

    # Сохраняем новый файл во временный
    try:
        with open(temp_path, "wb") as f:
            f.write(remote_code)
    except Exception as e:
        print(f"[❌] Ошибка при сохранении обновления:\n{e}")
        return

    print("[🔁] Обновление лаунчера...")

    try:
        os.replace(temp_path, launcher_path)  # Безопасная замена
        print("[✅] Лаунчер обновлён, перезапуск...")
        os.execv(sys.executable, [sys.executable] + sys.argv)  # Перезапуск
    except Exception as e:
        print(f"[❌] Ошибка при перезапуске лаунчера:\n{e}")


def download_main_py():
    url = "https://raw.githubusercontent.com/DdejjCAT/LITEHACKLATEST/main/main.py"

    try:
        response = requests.get(url)
        response.raise_for_status()
        remote_data = response.content
        remote_hash = hashlib.sha256(remote_data).hexdigest()
    except Exception as e:
        message_dialog(title="❌ Ошибка", text=f"Ошибка при получении скрипта:\n{e}", style=style).run()
        return False

    # Проверяем существующий файл
    if os.path.exists(MAIN_PY):
        try:
            with open(MAIN_PY, "rb") as f:
                local_data = f.read()
            local_hash = hashlib.sha256(local_data).hexdigest()

            # Если файл не изменился — ничего не делаем
            if local_hash == remote_hash:
                return True
        except Exception as e:
            message_dialog(title="⚠️ Ошибка чтения", text=f"Не удалось проверить скрипт:\n{e}", style=style).run()

    # Обновляем main.py
    try:
        with open(MAIN_PY, "wb") as f:
            f.write(remote_data)
        message_dialog(title="📥 Обновление", text="Файл скрипта был обновлён с GitHub!", style=style).run()
        return True
    except Exception as e:
        message_dialog(title="❌ Ошибка", text=f"Не удалось записать скрипт:\n{e}", style=style).run()
        return False

def run_in_new_terminal():
    python_exe = sys.executable
    script_path = os.path.abspath(MAIN_PY)
    system = platform.system()

    try:
        if system == "Windows":
            subprocess.Popen(['start', 'cmd', '/k', python_exe, script_path], shell=True)
        elif system == "Linux":
            if shutil.which("gnome-terminal"):
                subprocess.Popen(["gnome-terminal", "--", python_exe, script_path])
            elif shutil.which("xterm"):
                subprocess.Popen(["xterm", "-e", python_exe, script_path])
            else:
                message_dialog(title="⚠️ Внимание", text="Терминал не найден, скрипт запущен без терминала. Ввод кода может быть недоступен.", style=style).run()
                subprocess.Popen([python_exe, script_path])
        elif system == "Darwin":
            apple_script = f'''
            tell application "Terminal"
                do script "{python_exe} '{script_path}'"
                activate
            end tell
            '''
            subprocess.Popen(["osascript", "-e", apple_script])
        else:
            message_dialog(title="⚠️ Внимание", text=f"Неизвестная ОС {system}, запускаю без терминала.", style=style).run()
            subprocess.Popen([python_exe, script_path])
        return True
    except Exception as e:
        message_dialog(title="❌ Ошибка", text=f"Ошибка при запуске скрипта:\n{e}", style=style).run()
        return False

def download_and_run_main():
    if not download_main_py():
        return False
    return run_in_new_terminal()

def check_options_file():
    if not os.path.exists(OPTIONS_FILE):
        create_default_options()
        return False

    lines = []
    with open(OPTIONS_FILE, "r") as f:
        lines = f.readlines()

    empty_fields = []
    for line in lines:
        line = line.strip()
        if "=" in line:
            key, val = map(str.strip, line.split("=", 1))
            if val == "":
                empty_fields.append(key)

    if empty_fields:
        msg = "Пожалуйста, заполните следующие поля в config.txt:\n\n"
        msg += "\n".join(f"- {field}" for field in empty_fields)
        msg += "\n\nПосмотрите инструкцию в меню."
        message_dialog(title="❌ Ошибка настройки", text=msg, style=style).run()
        return False

    return True

def main_menu():
    save_default_commands()
    create_default_options()
    os.makedirs("databases", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("addons", exist_ok=True)

    while True:
        result = radiolist_dialog(
            title="LiteHack Установка и настройка",
            text="Выберите действие:",
            values=[
                ("run", "🚀 Запустить скрипт"),
                ("install", "📥 Установить библиотеки"),
                ("toggle", "⚙️  Вкл/Выкл команды"),
                ("access", "🔐 Доступ по ID"),
                ("addons", "📦 Установить аддоны"),
                ("readme", "📘 Инструкция"),
                ("exit", "❌ Выйти"),
            ],
            style=style,
        ).run()

        if result == "install":
            install_requirements()
            message_dialog(title="✅ Установка", text="Установка завершена!", style=style).run()

        elif result == "toggle":
            toggle_command_access()

        elif result == "access":
            configure_access()

        elif result == "addons":
            install_addons()

        elif result == "readme":
            show_online_readme()

        elif result == "run":
            updated = download_main_py()  # Проверка и обновление
            if not updated:
                message_dialog(title="❌ Ошибка", text="Не удалось обновить скрипт с GitHub.", style=style).run()
                continue

            if check_options_file():
                ok = run_in_new_terminal()
                if ok:
                    message_dialog(title="🚀 Запуск", text="Скрипт запущен!", style=style).run()
                else:
                    message_dialog(title="❌ Ошибка", text="Не удалось запустить скрипт.", style=style).run()


        elif result == "exit" or result is None:
            sys.exit(0)


if __name__ == "__main__":
    self_update_launcher()
    main_menu()
