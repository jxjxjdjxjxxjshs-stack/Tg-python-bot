import os
import sys
import io
import telebot
from telebot import types
from flask import Flask

BOT_TOKEN = "8617201086:AAFQqfmLrzcSBmKj-rwPb9eGgCo2qt7ok1U"
bot = telebot.TeleBot(BOT_TOKEN)

WEB_APP_URL = "https://github.io"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = types.WebAppInfo(WEB_APP_URL)
    btn = types.KeyboardButton(text="Открыть консоль кода 🚀", web_app=web_app)
    markup.add(btn)
    
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! Открой консоль, напиши код, и я запущу его на сервере.", 
        reply_markup=markup
    )

# Ловим данные, которые пользователь отправил из мини-приложения кнопкой "Запустить код"
@bot.message_handler(content_types=['web_app_data'])
def answer(message):
    user_code = message.web_app_data.data
    
    bot.send_message(message.chat.id, "Выполняю твой код... ⏳")
    
    # Безопасный перехват текста, который выведет функция print() в коде пользователя
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        # ЗАПУСК КУСКА КОДА, КОТОРЫЙ НАПИСАЛ ПОЛЬЗОВАТЕЛЬ
        exec(user_code)
        sys.stdout = old_stdout
        result = redirected_output.getvalue()
        
        if not result:
            result = "Код выполнился успешно, но ничего не вывел (используй print(), чтобы увидеть текст)."
            
    except Exception as e:
        sys.stdout = old_stdout
        result = f"❌ Ошибка в коде:\n{str(e)}"
    
    # Отправляем результат обратно в чат
    bot.send_message(message.chat.id, f"📝 Результат выполнения:\n\n```\n{result}\n```", parse_mode="Markdown")


app = Flask(__name__)
@app.route('/')
def home():
    return "Бот запущен!"

if __name__ == '__main__':
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
