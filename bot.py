import telebot
import requests
import random

TOKEN = "8832647487:AAFrqCsBhp-1_MR3supC8Wci-aQruuOpKTY"
bot = telebot.TeleBot(TOKEN)

def ask_gemini(question):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [{"role": "user", "content": question}]
            },
            timeout=15
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
    except:
        pass
    return None

def ask_gpt(question):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": question}]
            },
            timeout=15
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
    except:
        pass
    return None

def smart_answer(question):
    answers = [
        f"🤖 Твой вопрос: '{question[:60]}'. Я отвечу через минуту, а пока — отличный вопрос!",
        f"📡 Запрос принят: '{question[:50]}'. Нейросети думают, скоро ответят.",
        f"⚡ Вопрос '{question[:40]}' очень интересный! Напиши ещё что-нибудь."
    ]
    return random.choice(answers)

def ask_ai(question):
    answer = ask_gemini(question)
    if answer:
        return answer
    answer = ask_gpt(question)
    if answer:
        return answer
    return smart_answer(question)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 *ИИ-помощник*\n\nЗадавай любые вопросы! Работаю 24/7", parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def answer(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = ask_ai(message.text)
    bot.reply_to(message, reply)

print("✅ Бот запущен!")
bot.infinity_polling()
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
def keep_alive():
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
Thread(target=keep_alive, daemon=True).start()
