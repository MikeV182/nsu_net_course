import time

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from database import SessionLocal, Vacancy


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())


def parse_vacancies(url):
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(3)

    vacancies = []
    cards = driver.find_elements(By.CLASS_NAME, "magritte-redesign")

    for card in cards:
        try:
            title = card.find_element(
                By.CSS_SELECTOR, "span[data-qa='serp-item__title-text']"
            ).text
            company = card.find_element(
                By.CSS_SELECTOR, "span[data-qa='vacancy-serp__vacancy-employer-text']"
            ).text
            salary = (
                card.find_element(
                    By.CSS_SELECTOR,
                    "span[class*='magritte-text_typography-label-1-regular']",
                ).text
                if card.find_elements(
                    By.CSS_SELECTOR,
                    "span[class*='magritte-text_typography-label-1-regular']",
                )
                else "Не указана"
            )
            link = card.find_element(
                By.CSS_SELECTOR, "a[data-qa='serp-item__title']"
            ).get_attribute("href")
            experience = card.find_element(
                By.CSS_SELECTOR,
                "span[data-qa^='vacancy-serp__vacancy-work-experience']",
            ).text

            vacancies.append(
                {
                    "title": title,
                    "company": company,
                    "salary": salary,
                    "link": link,
                    "experience": experience,
                }
            )
        except Exception:
            continue

    driver.quit()
    return vacancies


@app.get("/parse")
def parse(url: str = Query(...), db: Session = Depends(get_db)):
    vacancies = parse_vacancies(url)

    for vacancy in vacancies:
        db.add(Vacancy(**vacancy))
    db.commit()

    return {"status": "success", "parsed": len(vacancies)}


@app.get("/vacancies")
def get_vacancies(db: Session = Depends(get_db)):
    return db.query(Vacancy).all()
