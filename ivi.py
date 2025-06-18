from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def find_promo_code(driver):
    # 1. Проверка URL
    current_url = driver.current_url
    
    if "ivi.ru/cert/promo" in current_url:
        if "code=" in current_url:
            return current_url.split('code=')[1].split('&')[0]
    
    # 2. Поиск в DOM
    try:
        promo_element = driver.find_element(By.CSS_SELECTOR, ".promo-code, .promocode, .code")
        if promo_element:
            return promo_element.text.strip()
    except:
        pass
    
    # 3. Поиск по регулярному выражению
    page_text = driver.page_source
    promo_matches = re.findall(r"[A-Z0-9]{8,16}", page_text)
    if promo_matches:
        return promo_matches[0]
    
    return "Промокод не найден"

# Настройки
url = "https://besplatno.com/966995"
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
    
    # Ожидание перехода
    WebDriverWait(driver, 30).until(
        EC.url_contains("ivi.ru/cert/promo")
    )
    
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
