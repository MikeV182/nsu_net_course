import json
import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
LOGIN = config["login"]
PASSWORD = config["password"]

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def login():
    driver.get("https://novosibirsk.hh.ru/account/login")
    time.sleep(3)
    
    email_input = driver.find_element(By.NAME, "username")
    email_input.send_keys(LOGIN)
    email_input.send_keys(Keys.RETURN)
    
    time.sleep(2)  # Ожидание загрузки пароля
    
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Даем время на авторизацию

# Функция парсинга одной страницы
def parse_page():
    vacancies = []
    cards = driver.find_elements(By.CLASS_NAME, "vacancy-serp-item")
    for card in cards:
        try:
            title = card.find_element(By.CLASS_NAME, "serp-item__title").text
            company = card.find_element(By.CLASS_NAME, "vacancy-serp-item__meta-info-company").text
            salary = card.find_element(By.CLASS_NAME, "bloko-header-section-3").text if card.find_elements(By.CLASS_NAME, "bloko-header-section-3") else "Не указана"
            link = card.find_element(By.CLASS_NAME, "serp-item__title").get_attribute("href")
            experience = card.find_element(By.CLASS_NAME, "vacancy-serp-item__meta-info").text
            schedule = card.find_element(By.CLASS_NAME, "bloko-text").text
            
            vacancies.append([title, company, salary, link, experience, schedule])
        except Exception as e:
            print("Ошибка при парсинге карточки:", e)
    return vacancies

# Функция пагинации
def parse_vacancies():
    url = "https://novosibirsk.hh.ru/search/vacancy?text=Python"
    driver.get(url)
    time.sleep(3)
    
    all_vacancies = []
    page = 1
    while True:
        print(f"Парсим страницу {page}...")
        vacancies = parse_page()
        all_vacancies.extend(vacancies)
        
        try:
            next_button = driver.find_element(By.CLASS_NAME, "bloko-button[data-qa='pager-next']")
            next_button.click()
            time.sleep(5)
            page += 1
        except:
            print("Достигнута последняя страница.")
            break
    
    return all_vacancies

# Функция сохранения в CSV
def save_to_csv(vacancies, filename="vacancies.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Название вакансии", "Компания", "Зарплата", "Ссылка", "Опыт работы", "График работы"])
        writer.writerows(vacancies)
    print(f"Данные сохранены в {filename}")

# Основной процесс
login()
vacancies = parse_vacancies()
save_to_csv(vacancies)

driver.quit()
