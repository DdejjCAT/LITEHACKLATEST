import aiohttp
import json

async def ask_ai(message: str, profile: str = "code", flags: dict = None) -> dict:
    if flags is None:
        flags = {"uncensored": True}

    payload = {
        "model": MODEL_NAME,
        "profile": profile,
        "message": message,
        "flags": flags
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload) as resp:
            if resp.status != 200:
                raise RuntimeError(f"❌ Ошибка API: {resp.status}")
            data = await resp.json()

    if "reply" not in data:
        raise ValueError(f"❌ В ответе от AI отсутствует ключ 'reply': {data}")

    raw_reply = data["reply"]

    # Если список — оборачиваем
    if isinstance(raw_reply, list):
        return {"actions": raw_reply}

    # Если dict — сразу возвращаем
    if isinstance(raw_reply, dict):
        return raw_reply

    # Если строка — пробуем достать JSON
    if isinstance(raw_reply, str):
        raw_reply = raw_reply.strip()
        start = raw_reply.find('{')
        end = raw_reply.rfind('}') + 1
        if start == -1 or end == -1:
            raise ValueError(f"❌ Не удалось найти JSON в ответе: {raw_reply}")
        return json.loads(raw_reply[start:end])

    raise ValueError(f"❌ Неподдерживаемый тип поля 'reply': {type(raw_reply)}")
