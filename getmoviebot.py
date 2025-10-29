from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Bot
import datetime

# --- Apna details yahan likho ---
BOT_TOKEN = "8396399839:AAESTEWYLg-EoOS5euts7mBH90UONPJTcIw"  # apna bot token
CHANNEL_ID = 1002810828742  # apne private channel ka ID (minus ke sath)
VERIFY_LINK = "https://link-center.net/1394248/EOdn0r07wI7u"

verified_users = {}

# --- Start command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome to MovieBot!\nType /verify to unlock movies for 24 hours."
    )

# --- Verify command ---
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Please verify here 👇\n{VERIFY_LINK}\n\nThen type /done ✅"
    )

# --- Done command ---
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    verified_users[user_id] = datetime.datetime.now()
    await update.message.reply_text("✅ Verification complete! Use /movie <name>")

# --- Movie search command ---
async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.datetime.now()

    if user_id not in verified_users:
        await update.message.reply_text("❌ Please verify first using /verify")
        return

    if (now - verified_users[user_id]).total_seconds() > 86400:
        await update.message.reply_text("⏰ Verification expired! Do /verify again.")
        return

    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("🎥 Example: /movie Animal")
        return

    await update.message.reply_text(f"🔍 Searching '{query}'...")

    bot = Bot(token=BOT_TOKEN)
    try:
        # Channel se 100 recent messages nikal lo
        async for msg in bot.get_chat_history(CHANNEL_ID, limit=100):
            if msg.text and query.lower() in msg.text.lower():
                await update.message.reply_text(f"🎬 Found: \n{msg.text}")
                return

        await update.message.reply_text("😔 Sorry, no results found for that movie.")
    except Exception as e:
        await update.message.reply_text(f"⚠ Error: {e}")

# --- Run the bot ---
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("verify", verify))
app.add_handler(CommandHandler("done", done))
app.add_handler(CommandHandler("movie", movie))

print("🤖 Bot is running...")
app.run_polling()
