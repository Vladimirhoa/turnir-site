FROM python:3.12-slim

# Устанавливаем переменные окружения, чтобы Python не писал .pyc файлы и не буферизировал вывод
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь код проекта внутрь контейнера
COPY . /app/

# Команда, которая запустит боевой сервер на 8000 порту
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]