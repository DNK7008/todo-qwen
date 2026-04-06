from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from sqlalchemy.orm import Session
from models import init_db, User, Task, Role, TaskStatus, get_db, SessionLocal
from datetime import datetime

# States for conversation
SELECT_USER, CREATE_TASK_TITLE, CREATE_TASK_DESCRIPTION, SET_PRIORITY = range(4)

# Bot token - replace with your actual token
BOT_TOKEN = "8644348317:AAHhc-wLShYOs9gn4HQ-3awk2b1dZasOXkQ"

# Admin user IDs who can set roles (add your Telegram ID here)
ADMIN_IDS = [734548409]

def get_user_by_telegram_id(db: Session, telegram_id: str) -> User:
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def create_or_update_user(db: Session, telegram_id: str, username: str, full_name: str) -> User:
    user = get_user_by_telegram_id(db, telegram_id)
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
            role=Role.SUBORDINATE
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    db = SessionLocal()
    try:
        user = create_or_update_user(
            db, 
            str(update.effective_user.id),
            update.effective_user.username,
            update.effective_user.full_name
        )
        
        role_names = {
            Role.CHIEF: "👑 Начальник",
            Role.MANAGER: "👨‍💼 Руководитель",
            Role.SUBORDINATE: "👤 Подчиненный"
        }
        
        welcome_text = f"""
Привет, {user.full_name or user.username}!

Твоя роль: {role_names[user.role]}

Доступные команды:
/tasks - Мои задачи
/create - Создать задачу
/my_created - Созданные мной задачи
/help - Помощь
        """
        
        if user.role in [Role.CHIEF, Role.MANAGER]:
            welcome_text += "\n/set_role - Назначить роль пользователю"
        
        keyboard = [
            [InlineKeyboardButton("📋 Мои задачи", callback_data="my_tasks")],
            [InlineKeyboardButton("➕ Создать задачу", callback_data="create_task")],
        ]
        
        if user.role in [Role.CHIEF, Role.MANAGER]:
            keyboard.append([InlineKeyboardButton("📝 Созданные мной", callback_data="my_created")])
            keyboard.append([InlineKeyboardButton("⚙️ Назначить роль", callback_data="set_role")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    finally:
        db.close()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help information"""
    help_text = """
📌 *Система управления задачами*

*Роли:*
👑 Начальник - может всё
👨‍💼 Руководитель - может создавать задачи подчиненным
👤 Подчиненный - выполняет задачи

*Команды:*
/start - Запустить бота
/tasks - Показать мои задачи
/create - Создать новую задачу
/my_created - Задачи созданные мной
/set_role - Назначить роль (для начальников и руководителей)
/help - Эта справка

*Статусы задач:*
⏳ Ожидает
🔄 В работе
✅ Выполнено
🔒 Закрыто
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def show_my_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show tasks assigned to current user"""
    db = SessionLocal()
    try:
        user = get_user_by_telegram_id(db, str(update.effective_user.id))
        tasks = db.query(Task).filter(Task.assignee_id == user.id).order_by(Task.created_at.desc()).limit(10).all()
        
        if not tasks:
            await update.message.reply_text("У вас нет задач 🎉")
            return
        
        status_emojis = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.CLOSED: "🔒"
        }
        
        priority_names = {1: "Низкий", 2: "Средний", 3: "Высокий"}
        
        for task in tasks:
            text = f"""
{status_emojis[task.status]} *Задача #{task.id}*
*Название:* {task.title}
*Описание:* {task.description or 'Нет описания'}
*Приоритет:* {priority_names.get(task.priority, 'Нормальный')}
*Создана:* {task.created_at.strftime('%d.%m.%Y %H:%M')}
            """
            
            keyboard = []
            if task.status == TaskStatus.PENDING:
                keyboard.append([InlineKeyboardButton("▶️ В работу", callback_data=f"start_{task.id}")])
            elif task.status == TaskStatus.IN_PROGRESS:
                keyboard.append([InlineKeyboardButton("✅ Выполнить", callback_data=f"complete_{task.id}")])
            
            if keyboard:
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)
            else:
                await update.message.reply_text(text, parse_mode='Markdown')
    finally:
        db.close()

async def my_created_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show tasks created by current user"""
    db = SessionLocal()
    try:
        user = get_user_by_telegram_id(db, str(update.effective_user.id))
        
        if user.role == Role.SUBORDINATE:
            await update.message.reply_text("Эта команда доступна только руководителям и начальнику")
            return
        
        tasks = db.query(Task).filter(Task.creator_id == user.id).order_by(Task.created_at.desc()).limit(10).all()
        
        if not tasks:
            await update.message.reply_text("Вы еще не создавали задач")
            return
        
        status_emojis = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.CLOSED: "🔒"
        }
        
        for task in tasks:
            assignee_name = task.assignee.full_name if task.assignee else "Не назначена"
            text = f"""
{status_emojis[task.status]} *Задача #{task.id}*
*Название:* {task.title}
*Исполнитель:* {assignee_name}
*Статус:* {task.status.value}
            """
            await update.message.reply_text(text, parse_mode='Markdown')
    finally:
        db.close()

async def create_task_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start creating a new task"""
    db = SessionLocal()
    try:
        user = get_user_by_telegram_id(db, str(update.effective_user.id))
        
        # Get all subordinates for assignment
        subordinates = db.query(User).filter(User.role == Role.SUBORDINATE).all()
        
        if not subordinates:
            await update.message.reply_text("Нет доступных исполнителей. Сначала добавьте пользователей.")
            return ConversationHandler.END
        
        keyboard = []
        for sub in subordinates:
            keyboard.append([InlineKeyboardButton(sub.full_name or sub.username, callback_data=f"assign_{sub.id}")])
        
        keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="cancel")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Выберите исполнителя для задачи:", reply_markup=reply_markup)
        return SELECT_USER
    finally:
        db.close()

async def select_user_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user selection for task assignment"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "cancel":
        await query.edit_message_text("Создание задачи отменено")
        return ConversationHandler.END
    
    assignee_id = int(query.data.split("_")[1])
    context.user_data['assignee_id'] = assignee_id
    
    await query.edit_message_text("Введите название задачи:")
    return CREATE_TASK_TITLE

async def task_title_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle task title input"""
    context.user_data['title'] = update.message.text
    await update.message.reply_text("Введите описание задачи (или отправьте /skip чтобы пропустить):")
    return CREATE_TASK_DESCRIPTION

async def task_description_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle task description input"""
    if update.message.text == "/skip":
        context.user_data['description'] = None
    else:
        context.user_data['description'] = update.message.text
    
    keyboard = [
        [InlineKeyboardButton("1️⃣ Низкий", callback_data="priority_1")],
        [InlineKeyboardButton("2️⃣ Средний", callback_data="priority_2")],
        [InlineKeyboardButton("3️⃣ Высокий", callback_data="priority_3")],
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Выберите приоритет задачи:", reply_markup=reply_markup)
    return SET_PRIORITY

async def set_priority_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle priority selection and create task"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "cancel":
        await query.edit_message_text("Создание задачи отменено")
        return ConversationHandler.END
    
    priority = int(query.data.split("_")[1])
    context.user_data['priority'] = priority
    
    # Create the task
    db = SessionLocal()
    try:
        creator = get_user_by_telegram_id(db, str(update.effective_user.id))
        
        task = Task(
            title=context.user_data['title'],
            description=context.user_data.get('description'),
            priority=priority,
            creator_id=creator.id,
            assignee_id=context.user_data['assignee_id']
        )
        
        db.add(task)
        db.commit()
        
        await query.edit_message_text(f"✅ Задача создана!\n\nID: #{task.id}\nНазвание: {task.title}")
        
        # Notify assignee if different from creator
        if task.assignee_id != creator.id:
            try:
                assignee = db.query(User).filter(User.id == task.assignee_id).first()
                await context.bot.send_message(
                    chat_id=assignee.telegram_id,
                    text=f"📋 Вам назначена новая задача #{task.id}: {task.title}"
                )
            except Exception as e:
                print(f"Could not notify assignee: {e}")
                
    finally:
        db.close()
    
    return ConversationHandler.END

async def set_role_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start setting role for a user"""
    db = SessionLocal()
    try:
        user = get_user_by_telegram_id(db, str(update.effective_user.id))
        
        if user.role not in [Role.CHIEF, Role.MANAGER]:
            await update.message.reply_text("Эта команда доступна только руководителям и начальнику")
            return ConversationHandler.END
        
        # Get all users except chiefs
        users = db.query(User).filter(User.role != Role.CHIEF).all()
        
        keyboard = []
        for u in users:
            role_emoji = "👨‍💼" if u.role == Role.MANAGER else "👤"
            keyboard.append([InlineKeyboardButton(f"{role_emoji} {u.full_name or u.username}", callback_data=f"user_{u.id}")])
        
        keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="cancel")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Выберите пользователя для изменения роли:", reply_markup=reply_markup)
        return SELECT_USER
    finally:
        db.close()

async def skip_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Skip description input"""
    return await task_description_received(update, context)

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel current conversation"""
    await update.message.reply_text("Операция отменена")
    return ConversationHandler.END

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button callbacks for task actions"""
    query = update.callback_query
    await query.answer()
    
    db = SessionLocal()
    try:
        if query.data.startswith("start_"):
            task_id = int(query.data.split("_")[1])
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = TaskStatus.IN_PROGRESS
                db.commit()
                await query.edit_message_text(f"✅ Задача #{task.id} переведена в статус 'В работе'")
                
        elif query.data.startswith("complete_"):
            task_id = int(query.data.split("_")[1])
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.utcnow()
                db.commit()
                await query.edit_message_text(f"🎉 Задача #{task.id} выполнена!")
                
    finally:
        db.close()

def main():
    """Main function to run the bot"""
    # Initialize database
    init_db()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tasks", show_my_tasks))
    application.add_handler(CommandHandler("my_created", my_created_tasks))
    
    # Create task conversation handler
    create_task_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(create_task_start, pattern="^create_task$")],
        states={
            SELECT_USER: [CallbackQueryHandler(select_user_callback)],
            CREATE_TASK_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_title_received)],
            CREATE_TASK_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_description_received),
                CommandHandler("skip", skip_description)
            ],
            SET_PRIORITY: [CallbackQueryHandler(set_priority_callback)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )
    application.add_handler(create_task_conv)
    
    # General button callback handler
    application.add_handler(CallbackQueryHandler(button_callback, pattern="^(start_|complete_)"))
    
    # Run the bot
    print("Bot is starting...")
    # For Python 3.14+ compatibility, we need to handle the event loop explicitly
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
