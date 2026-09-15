import os
import sys
import io
import telebot
from telebot import types
from flask import Flask, request, jsonify, send_from_directory

BOT_TOKEN = "8617201086:AAFQqfmLrzcSBmKj-rwPb9eGgCo2qt7ok1U"
bot = telebot.TeleBot(BOT_TOKEN)

# Новая версия для сброса кэша Telegram
WEB_APP_URL = "https://jxjxjdjxjxxjshs-stack.github.io/Tg-python-bot/index.html?v=60
"

@bot.message_handler(commands=['start'])
def start(message):
    inline_markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(WEB_APP_URL)
    inline_btn = types.InlineKeyboardButton(text="Открыть консоль кода 💻", web_app=web_app)
    inline_markup.add(inline_btn)
    
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! Открой консоль, пиши код, и результат появится прямо внутри приложения.", 
        reply_markup=inline_markup
    )

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

# ОБРАБОТЧИК: Выполняет код и сразу отдает ответ обратно в мини-приложение
@app.route('/api/run', methods=['POST'])
def run_code():
    data = request.json or {}
    user_code = data.get('code', '')
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        # Исправляем автоматическую заглавную букву Print от клавиатуры телефона
        fixed_code = user_code.replace("Print", "print")
        exec(fixed_code, {})
        sys.stdout = old_stdout
        result = redirected_output.getvalue()
        if not result:
            result = "Код успешно выполнен, но ничего не вывел (используйте print())."
    except Exception as e:
        sys.stdout = old_stdout
        result = f"❌ Ошибка в коде:\n{str(e)}"
        
    return jsonify({"output": result})

if __name__ == '__main__':
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
