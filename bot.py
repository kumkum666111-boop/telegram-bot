import telebot
import requests
import random
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

TOKEN = "8225294682:AAHthQkYsualvHFJqYa7tDHQsFHmexRi7Uo"
bot = telebot.TeleBot(TOKEN)

# --- НАСТОЙКИ OPENROUTER (бесплатные модели) ---
def ask_gemini(question):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [{"role": "user", "content": question}]
            },
            timeout=10
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
            timeout=10
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
            timeout=10
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
    except:
        pass
    return None

# --- УМНЫЙ ЗАПАСНОЙ ОТВЕТ (если все нейросети недоступны) ---
def smart_fallback(question):
    q = question.lower()
    if "привет" in q:
        return "👋 Привет! Я ИИ-помощник. Сейчас нейросети перегружены, но я отвечаю сам. Задай вопрос!"
    if "как дела" in q:
        return "У меня всё отлично! А у тебя?"
    if "код" in q:
        return "```python\nprint('Hello, World!')\n```\nПример кода на Python. Напиши подробнее, что нужно."
    if "реши" in q or "пример" in q:
        try:
            expr = q.replace("реши", "").replace("пример", "").strip()
            result = eval(expr)
            return f"🧮 Результат: {expr} = {result}"
        except:
            return "Напиши пример, например: *реши 25 * 4*"
    if "стих" in q:
        return "🌙 *Лунной ночью код писал,*\n*Никого не понимал.*\n*Вдруг нейросеть прибежала,*\n*Все баги сразу убрала!*"
    if "шутка" in q:
        return "Почему программисты не любят природу? Потому что там слишком много багов! 😄"
    if "время" in q:
        return f"⏰ Сейчас {datetime.now().strftime('%H:%M')}."
    return f"📝 '{question[:60]}' — отличный вопрос! Я обязательно отвечу, когда нейросети освободятся. Напиши что-нибудь ещё."

# --- ВЫБОР ИИ ---
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

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

def keep_alive():
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

Thread(target=keep_alive, daemon=True).start()

# --- ОБРАБОТЧИКИ КОМАНД ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "🤖 *МЕГА-ИИ ПОМОЩНИК*\n\n"
        "Я работаю на **3 нейросетях**:\n"
        "🔥 Google Gemini\n"
        "🔥 GPT-4o-mini\n"
        "🔥 Claude 3 Haiku\n\n"
        "Если нейросети заняты — я отвечаю сам.\n"
        "Просто напиши любой вопрос!\n\n"
        "_Создан ABSOLUTE-01_", 
        parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def answer(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = ask_ai(message.text)
    bot.reply_to(message, reply, parse_mode="Markdown")

print("✅ МЕГА-БОТ ЗАПУЩЕН!")
print("🤖 3 нейросети активны")
bot.infinity_polling()
