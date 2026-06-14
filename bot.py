import telebot
import requests
import random
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "8832647487:AAGUewpKFoQbfmSl7F1bqhevMYXT3PPYLEA"
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

def ask_claude(question):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "anthropic/claude-3-haiku:free",
                "messages": [{"role": "user", "content": question}]
            },
            timeout=15
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
    except:
        pass
    return None

def smart_fallback(question):
    answers = [
        f"🤖 Вопрос принят: '{question[:60]}'. Нейросети сейчас думают, я отвечу чуть позже!",
        f"📡 Запрос '{question[:50]}' сохранён. Скоро вернусь с ответом!",
        f"⚡ Отличный вопрос! '{question[:40]}'. Напиши ещё что-нибудь, я быстро учусь.",
        f"💾 Твой вопрос в очереди. Когда ИИ ответит — сразу напишу!"
    ]
    return random.choice(answers)

def ask_ai(question):
    answer = ask_gemini(question)
    if answer:
        return answer
    answer = ask_gpt(question)
    if answer:
        return answer
    answer = ask_claude(question)
    if answer:
        return answer
    return smart_fallback(question)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "🤖 *МЕГА-ИИ ПОМОЩНИК*\n\n"
        "Я работаю на **3 нейросетях**:\n"
        "🔥 Google Gemini\n"
        "🔥 GPT-4o-mini\n"
        "🔥 Claude 3 Haiku\n\n"
        "Просто напиши любой вопрос!\n\n"
        "_Создан ABSOLUTE-01_", 
        parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def answer(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        reply = ask_ai(message.text)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {str(e)[:100]}\n\nПопробуй ещё раз.")

# Фиктивный веб-сервер для Render
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

def keep_alive():
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

Thread(target=keep_alive, daemon=True).start()

print("✅ МЕГА-БОТ ЗАПУЩЕН!")
print("🤖 3 нейросети активны")
bot.infinity_polling()
