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
# options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def login():
    driver.get("https://novosibirsk.hh.ru/account/login")
    time.sleep(3)
    
    login_button = driver.find_element(
        By.XPATH,
        '/html/body/div[5]/div/div[1]/div[4]/div/div/div/div[1]/div/div/div/div \
        /div/div/div/div/div/form/div/div[3]/button[1]')
    login_button.click()
    time.sleep(2)

    email_label = driver.find_element(
        By.XPATH,
        '/html/body/div[5]/div/div[1]/div[4]/div/div/div/div[1]/div/div/div/div \
        /div/div/div/div/div/form/div/div/div[2]/label[2]')
    email_label.click()
    time.sleep(2)

    email_input = driver.find_element(By.NAME, "username")
    email_input.send_keys(LOGIN)
    
    login_with_password = driver.find_element(
        By.XPATH,
        '/html/body/div[5]/div/div[1]/div[4]/div/div/div/div[1]/div/div/div/div \
        /div/div/div/div/div/form/div/div/div[6]/button[2]')
    login_with_password.click()
    time.sleep(2)
    
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(PASSWORD)
    
    enter_button = driver.find_element(
        By.XPATH,
        '/html/body/div[5]/div/div[1]/div[4]/div/div/div/div[1]/div/div/div/div \
        /div/div/div/div/div/form/div/div/div[5]/button[1]')
    enter_button.click()

    time.sleep(5)

def parse_page():
    vacancies = []
    cards = driver.find_elements(By.CLASS_NAME, "magritte-redesign")
    for card in cards:
        title = card.find_element(
            By.CSS_SELECTOR, 
            "span[data-qa='serp-item__title-text']").text
        company = card.find_element(
            By.CSS_SELECTOR, 
            "span[data-qa='vacancy-serp__vacancy-employer-text']").text
        salary = card.find_element(
            By.CSS_SELECTOR, 
            "span[class*='magritte-text_typography-label-1-regular___pi3R-_3-0-27']").text \
            if card.find_elements(
                By.CSS_SELECTOR, 
                "span[class*='magritte-text_typography-label-1-regular___pi3R-_3-0-27']") \
            else "Не указана"
        link = card.find_element(
            By.CSS_SELECTOR, 
            "a[data-qa='serp-item__title']").get_attribute("href")
        experience = card.find_element(
            By.CSS_SELECTOR, 
            "span[data-qa^='vacancy-serp__vacancy-work-experience']").text
            
        vacancies.append([title, company, salary, link, experience])
    return vacancies

def parse_vacancies():
    url = "https://novosibirsk.hh.ru/search/vacancy?text=PHP+junior"
    driver.get(url)
    time.sleep(3)
    
    all_vacancies = []
    page = 1
    while True:
        try:
            print(f"Парсим страницу {page}...")
            vacancies = parse_page()
            all_vacancies.extend(vacancies)
        
            driver.get(url + f"&page={page}")
            time.sleep(5)
            page += 1
        except Exception as e:
            print("Достигнута последняя страница или произошла ошибка:", e)
            break
    
    return all_vacancies

def save_to_csv(vacancies, filename="vacancies.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Название вакансии", 
            "Компания", 
            "Зарплата", 
            "Ссылка", 
            "Опыт работы"])
        writer.writerows(vacancies)
    print(f"Данные сохранены в {filename}")

login()
vacancies = parse_vacancies()
save_to_csv(vacancies)

driver.quit()
