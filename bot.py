import os
import sys
import io
import telebot
from telebot import types
from flask import Flask, request, jsonify

# Токен вашего бота
BOT_TOKEN = "8617201086:AAFQqfmLrzcSBmKj-rwPb9eGgCo2qt7ok1U"
bot = telebot.TeleBot(BOT_TOKEN)

# Ссылка на ваше мини-приложение (сбрасываем кэш версией v=9)
WEB_APP_URL = "https://jxjxjdjxjxxjshs-stack.github.io/Tg-python-bot//index.html?v=11"

@bot.message_handler(commands=['start'])
def start(message):
    inline_markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(WEB_APP_URL)
    inline_btn = types.InlineKeyboardButton(text="Открыть консоль кода 💻", web_app=web_app)
    inline_markup.add(inline_btn)
    
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! Открой консоль, напиши код, и я запущу его на сервере.", 
        reply_markup=inline_markup
    )

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот и сервер запущены!"

# ИСПРАВЛЕНО: Теперь метод POST указан абсолютно верно
@app.route('/run-code', methods=['POST'])
def run_code_endpoint():
    try:
        data = request.json
        user_code = data.get('code', '')
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"status": "error", "message": "No user_id"}), 400
            
        bot.send_message(user_id, "Выполняю твой код... ⏳")
        
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        
        try:
            # Исправляем заглавную букву Print, если телефон ввёл её автоматически
            fixed_code = user_code.replace("Print", "print")
            exec(fixed_code)
            sys.stdout = old_stdout
            result = redirected_output.getvalue()
            if not result:
                result = "Код выполнился успешно, но ничего не вывел (используй print())."
        except Exception as e:
            sys.stdout = old_stdout
            result = f"❌ Ошибка в коде:\n{str(e)}"
        
        bot.send_message(user_id, f"📝 Результат выполнения:\n\n```\n{result}\n```", parse_mode="Markdown")
        return jsonify({"status": "success"})
    except Exception as global_e:
        return jsonify({"status": "error", "message": str(global_e)}), 500

if __name__ == '__main__':
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
