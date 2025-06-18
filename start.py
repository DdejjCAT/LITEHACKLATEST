from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def find_promo_code(driver):
    # 1. Проверка URL (приоритетная проверка)
    current_url = driver.current_url
    
    # Если мы на start.ru/code
    if "start.ru/code" in current_url:
        # Проверяем параметр promocode в URL
        if "promocode=" in current_url:
            promo = current_url.split('promocode=')[1].split('&')[0]
            if len(promo) >= 8:  # минимальная длина промокода
                return promo
        
        # Дополнительно ищем в DOM
        try:
            promo_elements = driver.find_elements(By.CSS_SELECTOR, ".promo-code, .promocode, .code, [class*='promo'], [class*='code']")
            for element in promo_elements:
                text = element.text.strip()
                if len(text) >= 8 and text.isupper() and any(c.isdigit() for c in text):
                    return text
        except:
            pass
        
        # Ищем в тексте страницы
        page_text = driver.page_source
        promo_matches = re.findall(r"[A-Z0-9]{8,20}", page_text)
        if promo_matches:
            return max(promo_matches, key=len)  # возвращаем самый длинный код
    
    # 2. Проверка для других URL (ivi.ru и т.д.)
    try:
        # Проверяем URL на наличие промокода
        if "promocode=" in current_url:
            promo = current_url.split('promocode=')[1].split('&')[0]
            if len(promo) >= 8:
                return promo
        
        # Поиск в DOM
        promo_elements = driver.find_elements(By.CSS_SELECTOR, ".promo-code, .promocode, .code, [class*='promo'], [class*='code']")
        for element in promo_elements:
            text = element.text.strip()
            if len(text) >= 8 and text.isupper() and any(c.isdigit() for c in text):
                return text
        
        # Поиск по регулярному выражению
        page_text = driver.page_source
        promo_matches = re.findall(r"[A-Z0-9]{8,20}", page_text)
        if promo_matches:
            return max(promo_matches, key=len)  # возвращаем самый длинный код
    
    except Exception as e:
        print(f"Ошибка при поиске промокода: {e}")
    
    return "Промокод не найден"

# Настройки
url = "https://besplatno.com/971313"
email = "frgift@bk.ru"

# Запуск браузера
driver = webdriver.Chrome()
try:
    driver.get(url)
    
    # Ввод email
    email_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.sc-TextInput-input"))
    )
    email_field.send_keys(email)
    
    # Клик по кнопке
    submit_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sc-CjmControl"))
    )
    submit_button.click()
    
    # Ожидание перехода (либо на start.ru/code, либо на ivi.ru)
    try:
        WebDriverWait(driver, 30).until(
            lambda d: "start.ru/code" in d.current_url or "ivi.ru/cert/promo" in d.current_url
        )
    except:
        print("Не удалось дождаться перехода на целевую страницу")
    
    # Поиск промокода
    promo_code = find_promo_code(driver)
    print(promo_code)
    
    # Для отладки
    driver.save_screenshot("debug.png")
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

except Exception as e:
    print("Ошибка:", e)
finally:
    driver.quit()
