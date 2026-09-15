import os
import telebot
from telebot import types
from flask import Flask

# Ваш проверенный токен
BOT_TOKEN = "8617201086:AAFQqfmLrzcSBmKj-rwPb9eGgCo2qt7ok1U"
bot = telebot.TeleBot(BOT_TOKEN)

# Ваша точная ссылка на мини-приложение в GitHub Pages
WEB_APP_URL = "https://github.io"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем кнопку для открытия мини-приложения
    web_app = types.WebAppInfo(WEB_APP_URL)
    btn = types.KeyboardButton(text="Открыть приложение 🚀", web_app=web_app)
    markup.add(btn)
    
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! Нажми на кнопку ниже, чтобы запустить мини-приложение:", 
        reply_markup=markup
    )

# Этот блок нужен, чтобы бесплатный хостинг Render думал, что это сайт, и не отключал бота
app = Flask(__name__)
@app.route('/')
def home():
    return "Бот запущен!"

if __name__ == '__main__':
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

