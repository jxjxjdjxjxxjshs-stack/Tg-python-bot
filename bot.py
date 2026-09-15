import os
import telebot
from telebot import types
from flask import Flask

BOT_TOKEN = "8617201086:AAFQqfmLrzcSBmKj-rwPb9eGgCo2qt7ok1U"
bot = telebot.TeleBot(BOT_TOKEN)

# Новая версия v=85 для сброса кэша
WEB_APP_URL = "https://jxjxjdjxjxxjshs-stack.github.io/Tg-python-bot/index.html?v=85
"

@bot.message_handler(commands=['start'])
def start(message):
    inline_markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(WEB_APP_URL)
    inline_btn = types.InlineKeyboardButton(text="Открыть консоль кода 💻", web_app=web_app)
    inline_markup.add(inline_btn)
    
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! Открой консоль ниже, пиши и запускай Python прямо в приложении.", 
        reply_markup=inline_markup
    )

app = Flask(__name__)
@app.route('/')
def home():
    return "Сервер работает!"

if __name__ == '__main__':
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
