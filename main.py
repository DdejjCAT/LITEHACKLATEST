def self_update_main_py():
    import requests, hashlib, os, sys

    url = "https://raw.githubusercontent.com/DdejjCAT/LITEHACKLATEST/main/main.py"
    local_path = "main.py"
    temp_path = "main.py.new"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        remote_code = response.content
        remote_hash = hashlib.sha256(remote_code).hexdigest()
    except Exception as e:
        print(f"[❌] Не удалось проверить обновление main.py: {e}")
        return False

    if os.path.exists(local_path):
        try:
            with open(local_path, "rb") as f:
                local_code = f.read()
            local_hash = hashlib.sha256(local_code).hexdigest()
            if remote_hash == local_hash:
                return False  # Обновления нет
        except Exception as e:
            print(f"[⚠️] Ошибка проверки текущей версии main.py: {e}")

    # Записываем новый файл во временный
    try:
        with open(temp_path, "wb") as f:
            f.write(remote_code)
    except Exception as e:
        print(f"[❌] Ошибка записи обновления main.py: {e}")
        return False

    # Заменяем файл
    try:
        os.replace(temp_path, local_path)
        print("[🔁] main.py обновлён, перезапуск...")
        # Перезапускаем процесс с новым файлом
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"[❌] Ошибка при перезапуске после обновления: {e}")
        return False
