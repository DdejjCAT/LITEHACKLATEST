# ==================== ИНИЦИАЛИЗАЦИЯ БОТА ====================
license_checker = LicenseChecker(client)
vip_checker = VipChecker(client)

async def init_bot():
    # Крашнемся внутри verify_captcha при ошибке, сюда попадём только если капча пройдена
    await verify_captcha()

    # Запуск клиента
    await client.start(phone=phone_number)
    me = await client.get_me()
    if me is None:
        print("❌ Не удалось получить информацию о пользователе")
        sys.exit(1)

    global OWNER_USER_ID
    OWNER_USER_ID = me.id

    # Лог админа
    if OWNER_USER_ID == PROTECTED_USER_ID:
        print(f"🔐 Пользователь — владелец и администратор (PROTECTED_USER_ID).")

    # Запуск мониторинга лицензии в фоне
    asyncio.create_task(monitor_license())

    # ==================== Проверка лицензии через участие в канале ====================
    is_licensed = await license_checker.is_member(OWNER_USER_ID)
    if not is_licensed:
        print("❌ Лицензия не подтверждена, скрипт остановлен.")
        await client.disconnect()
        sys.exit(1)
    else:
        print("✅ Лицензия подтверждена через канал!")

    # ==================== Проверка VIP через участие в канале ====================
    is_vip = await vip_checker.is_member(OWNER_USER_ID)
    if is_vip:
        print("💎 VIP активен")
    else:
        print("⚠️ У владельца нет VIP. Некоторые команды будут недоступны.")


# ==================== Фоновый мониторинг лицензии ====================
async def monitor_license():
    last_license_status = True

    while True:
        await asyncio.sleep(60)  # Проверять каждую минуту
        current_status = await license_checker.is_member(OWNER_USER_ID)

        if current_status != last_license_status:
            last_license_status = current_status
            if not current_status:
                print("❌ Лицензия аннулирована! Скрипт завершает работу.")
                await client.disconnect()
                os._exit(0)
