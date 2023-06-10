# образ на основе которого создаём контейнер
FROM python:3.10-alpine
COPY . /Drip_Chip
# рабочая директория внутри проекта
WORKDIR /Drip_Chip
# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# устанавливаем зависимости
RUN pip install --upgrade pip
RUN python -m venv venv
RUN pip install -r requirements.txt
RUN apk --update --no-cache add curl
# копируем содержимое текущей папки в контейнер
ENTRYPOINT ["/Drip_Chip/entrypoint.sh"]