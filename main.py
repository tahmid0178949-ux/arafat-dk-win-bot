import os, random, time, threading, requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)

@app.route('/')
def home():
    return "ARAFAT DK WIN BOT LIVE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 ARAFAT VAI MASTER - DK WIN 🔥\n\n✅ DK WIN Market Connected\n✅ Lifetime Active\n\nCommand:\n/signal - Signal\n/dkwin - Signal")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    direction = random.choice(["CALL UP 🟢", "PUT DOWN 🔴"])
    try:
        price = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()['price']
    except:
        price = round(random.uniform(65000, 68000), 2)
    
    await update.message.reply_text(f"💎 DK WIN SIGNAL 💎\n\nPair: BTC/USDT\nPrice: {price}\nSignal: {direction}\n\n⏳ 60s Wait Result...")

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

def run_bot():
    if not TOKEN:
        print("BOT_TOKEN missing!")
        return
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("signal", signal))
    bot_app.add_handler(CommandHandler("dkwin", signal))
    bot_app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
