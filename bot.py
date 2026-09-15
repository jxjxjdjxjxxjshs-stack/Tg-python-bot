import os
import sys
import io
import telebot
from telebot import types
from flask import Flask

# Токен вашего бота
BOT_TOKEN = "8617201086:AAFQqfmLrzcSBmKj-rwPb9eGgCo2qt7ok1U"
bot = telebot.TeleBot(BOT_TOKEN)

# Ваша абсолютно правильная ссылка без пробелов и сбросом кэша
WEB_APP_URL = "https://jxjxjdjxjxxjshs-stack.github.io/Tg-python-bot/?v=15"

@bot.message_handler(commands=['start'])
def start(message):
    # Создаем инлайн-кнопку прямо в сообщении (с неё отправка данных ВСЕГДА работает)
    inline_markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(WEB_APP_URL)
    inline_btn = types.InlineKeyboardButton(text="Открыть консоль кода 💻", web_app=web_app)
    inline_markup.add(inline_btn)
    
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! Открой консоль по синей кнопке ниже, напиши код, и я запущу его на сервере.", 
        reply_markup=inline_markup
    )

# Ловим код, который пользователь отправил кнопкой из мини-приложения
@bot.message_handler(content_types=['web_app_data'])
def answer(message):
    user_code = message.web_app_data.data
    bot.send_message(message.chat.id, "Выполняю твой код... ⏳")
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        # Авто-исправление заглавной буквы Print (на случай автозамены в телефоне)
        fixed_code = user_code.replace("Print", "print")
        
        # Запуск кода на сервере
        exec(fixed_code)
        
        sys.stdout = old_stdout
        result = redirected_output.getvalue()
        if not result:
            result = "Код выполнился успешно, но ничего не вывел. Используй print(), чтобы увидеть текст."
    except Exception as e:
        sys.stdout = old_stdout
        result = f"❌ Ошибка в коде:\n{str(e)}"
    
    bot.send_message(message.chat.id, f"📝 Результат выполнения:\n\n```\n{result}\n```", parse_mode="Markdown")

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

if __name__ == '__main__':
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
