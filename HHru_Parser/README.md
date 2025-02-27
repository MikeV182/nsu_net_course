## How to launch?

```
uvicorn WebParser:app --reload
```

- Запрос GET 127.0.0.1:8000/parse?url=https://novosibirsk.hh.ru/search/vacancy?text=Python запустит парсер.
- Запрос GET 127.0.0.1:8000/vacancies вернет вакансии в JSON.