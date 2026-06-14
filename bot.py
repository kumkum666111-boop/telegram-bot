import telebot
import requests

TOKEN = "8832647487:AAFrqCsBhp-1_MR3supC8Wci-aQruuOpKTY"
bot = telebot.TeleBot(TOKEN)

def ask_ai(question):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer sk-or-v1-2e9d8f7c6b5a4d3c2b1a0e9f8d7c6b5a4d3c2b1a0e9f8d7c6b5a4d3c2b1a0e"
            },
            json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [{"role": "user", "content": question}]
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "⚠️ ИИ временно недоступен. Попробуй через минуту."
    except Exception as e:
        return f"⚠️ Ошибка: {str(e)[:100]}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 *ИИ-помощник на базе Google Gemini*\n\nЗадавай любые вопросы!", parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def answer(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = ask_ai(message.text)
    bot.reply_to(message, reply)

print("✅ Бот с ИИ запущен!")
bot.infinity_polling()
