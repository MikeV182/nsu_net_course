from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal, Url


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/add-url")
def parse(url: str = Query(...), db: Session = Depends(get_db)):
    db.add(Url(**{"url" : url}))
    db.commit()

    return {"status": "success", "added": url}


@app.get("/urls")
def get_vacancies(db: Session = Depends(get_db)):
    return db.query(Url).all()
