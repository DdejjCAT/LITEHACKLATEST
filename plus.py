from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Настройки
url = "https://besplatno.com/940722?bid=12637"
email = "frgift@bk.ru"

# Инициализация драйвера
options = webdriver.ChromeOptions()
options.add_argument('--no-proxy-server')  # Отключить прокси
driver = webdriver.Chrome(options=options)

def find_promo_code(driver):
    """Функция для поиска промокода различными способами"""
    # 1. Проверка URL
    current_url = driver.current_url
    if "promocode=" in current_url:
        promo_code = current_url.split("promocode=")[1].split("&")[0]
        return f"{promo_code}"
    
    # 2. Поиск по регулярному выражению в тексте страницы
    page_text = driver.page_source
    promo_pattern = re.compile(r'[A-Z0-9]{8,12}')
    matches = promo_pattern.findall(page_text)
    
    # Фильтрация возможных промокодов (можно добавить дополнительные критерии)
    possible_promos = [m for m in matches if len(m) >= 8]
    if possible_promos:
        return f"{', '.join(set(possible_promos))}"
    
    # 3. Поиск в элементах страницы
    try:
        # Поиск по тексту "промокод" и соседним элементам
        elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ПРОМОКОД', 'промокод'), 'промокод')]")
        for element in elements:
            parent = element.find_element(By.XPATH, "./..")
            siblings = parent.find_elements(By.XPATH, "./*")
            for sibling in siblings:
                text = sibling.text.strip()
                if re.match(r'^[A-Z0-9]{8,12}$', text):
                    return f"{text}"
    except:
        pass
    
    # 4. Поиск в полях ввода
    try:
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for inp in inputs:
            value = inp.get_attribute("value")
            if value and re.match(r'^[A-Z0-9]{8,12}$', value):
                return f"{value}"
    except:
        pass
    
    # 5. Поиск в элементах с определенными классами
    try:
        possible_containers = driver.find_elements(By.CSS_SELECTOR, "div.promo-code, span.promo-code, code, kbd")
        for container in possible_containers:
            text = container.text.strip()
            if re.match(r'^[A-Z0-9]{8,12}$', text):
                return f"{text}"
    except:
        pass
    
    return "Не удалось найти промокод"

try:
    # 1. Открываем страницу с промокодом
    driver.get(url)
    
    # 2. Вводим email
    email_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.sc-TextInput-input")))
    email_field.send_keys(email)
    
    # 3. Нажимаем кнопку получения
    WebDriverWait(driver, 15).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "button.sc-CjmControl").get_attribute("disabled") is None)
    submit_button = driver.find_element(By.CSS_SELECTOR, "button.sc-CjmControl")
    submit_button.click()
    
    # 4. Ждем перехода на страницу Яндекса
    WebDriverWait(driver, 30).until(EC.url_contains("yandex.ru/gift"))
    
    # 5. Даем время для загрузки всех элементов
    time.sleep(5)
    
    # 6. Поиск промокода
    result = find_promo_code(driver)
    print(result)
    
    # Сохраняем скриншот и HTML для отладки
    driver.save_screenshot("result.png")
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

except Exception as e:
    print(f"\nПроизошла ошибка: {str(e)}")
    print(f"\nОбратитесь в тех. поддержку")
finally:
    if 'driver' in locals():
        driver.quit()
