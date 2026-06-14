FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install pyTelegramBotAPI requests
CMD python bot.py
