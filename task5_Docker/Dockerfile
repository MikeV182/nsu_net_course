# https://fastapi.tiangolo.com/deployment/docker/#create-the-fastapi-code

# Используем официальный Python образ
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файл зависимостей
COPY ./requirements.txt /code/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Копируем все исходники
COPY ./app /code/app

# Команда для запуска FastAPI через Uvicorn на порту 11111
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "11111"]
