"""Telegram productivity bot."""

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime
import asyncio

TOKEN = "7624456489:AAF-KLXmQq7J1oR05P5CWwchSR4H66aL5Z0"
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Hustletrackos 💸\n\n"
        "This bot was built for those who hustle with intention.\n\n"
        "🔹 Track your hustle\n"
        "🔹 Take focused breaks\n"
        "🔹 Stay productive with music\n\n"
        "Work. Break. Work. Repeat.\n"
        "By Thal"
    )

async def lockin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.datetime.now()

    if user_id not in user_data:
        user_data[user_id] = {}

    if user_data[user_id].get("on_break"):
        break_duration = now - user_data[user_id]["break_start"]
        user_data[user_id]["break_time"] += break_duration
        user_data[user_id]["on_break"] = False
        await update.message.reply_text("🔁 Break ended. Back to work.")
        return

    user_data[user_id] = {
        "start": now,
        "breaks": 0,
        "on_break": False,
        "break_time": datetime.timedelta(),
        "last_active_date": now.date()
    }

    await update.message.reply_text(
        "✅ Locked in!\n"
        "🎷 Time to grind. Enjoy this playlist while working:\n"
        "https://open.spotify.com/playlist/3XI4IJ1DpSnrTBztcjbnBS?"
    )

async def break_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.datetime.now()

    if user_id not in user_data or "start" not in user_data[user_id]:
        await update.message.reply_text("❌ You need to /lockin first.")
        return

    data = user_data[user_id]

    if data["breaks"] >= 3:
        await update.message.reply_text(
            "😤 You're still locked in.\n"
            "You've already taken 3 breaks.\n"
            "If you're this lazy, just /lockout — the timer keeps running."
        )
        return

    if data["on_break"]:
        await update.message.reply_text("❗ You're already on a break.")
        return

    elapsed = now - data["start"] - data["break_time"]
    data["on_break"] = True
    data["breaks"] += 1
    data["break_start"] = now

    await update.message.reply_text(
        f"⏸ Break #{data['breaks']} started.\n"
        f"⏱ Current work time: {str(elapsed).split('.')[0]}\n"
        "🔁 Use /lockin to resume."
    )

async def lockout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.datetime.now()

    if user_id not in user_data or "start" not in user_data[user_id]:
        await update.message.reply_text("❌ You haven't /lockin yet.")
        return

    data = user_data[user_id]

    if data.get("on_break"):
        break_duration = now - data["break_start"]
        data["break_time"] += break_duration

    total_work_time = now - data["start"] - data["break_time"]
    readable_time = str(total_work_time).split('.')[0]

    await update.message.reply_text(
        f"✅ You worked for {readable_time}.\n"
        "🔁 Click /start to reset for your next hustle."
    )

    del user_data[user_id]

async def main():
    print("🤖 Hustletrackos is running...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lockin", lockin))
    app.add_handler(CommandHandler("break", break_command))
    app.add_handler(CommandHandler("lockout", lockout))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())

