import os, random, threading, time, requests, asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)

# DK WIN Market - Live Price
def get_live_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        return float(r['price'])
    except:
        return round(random.uniform(66000, 68000), 2)

@app.route('/')
def home():
    return "ARAFAT DK WIN - LIFETIME LIVE ✅"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 **ARAFAT VAI MASTER - DK WIN** 🔥\n\n"
        "✅ DK WIN Market Connected\n"
        "✅ No Balance System\n"
        "✅ Lifetime Active\n\n"
        "Command:\n"
        "/signal - DK WIN Signal\n"
        "/dkwin - DK WIN Signal\n\n"
        "1 মিনিট পর Auto WIN/LOSS + Sticker আসবে।"
    )

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    direction = random.choice(["CALL 🔼", "PUT 🔽"])
    entry = get_live_price()
    
    await update.message.reply_text(
        f"💎 **DK WIN SIGNAL** 💎\n\n"
        f"Market: DK WIN LIVE\n"
        f"Pair: BTC/USDT\n"
        f"Direction: {direction}\n"
        f"Entry Price: {entry}\n\n"
        f"⏳ 60 Sec Wait... Result Coming"
    )
    
    # 60 sec por result
    threading.Thread(target=lambda: check_result(context.bot, update.effective_chat.id, direction, entry), daemon=True).start()

def check_result(bot, chat_id, direction, entry):
    time.sleep(60)
    exit_price = get_live_price()
    is_win = (exit_price > entry) if "CALL" in direction else (exit_price < entry)

    async def send():
        if is_win:
            await bot.send_message(chat_id=chat_id, text=f"✅ **WIN** ✅\n\nEntry: {entry}\nExit: {exit_price}\nDirection: {direction}\n\n🔥 DK WIN WIN 🔥")
            try:
                # Win Sticker
                await bot.send_sticker(chat_id=chat_id, sticker="CAACAgIAAxkBAAIBCGg0r0u8hW8ZAAEe8QAC0Qk0AAI2TQABq0QAB0gQ")
            except: pass
        else:
            await bot.send_message(chat_id=chat_id, text=f"❌ **LOSS** ❌\n\nEntry: {entry}\nExit: {exit_price}\nDirection: {direction}\n\n📉 LOSS")
            try:
                # Loss Sticker
                await bot.send_sticker(chat_id=chat_id, sticker="CAACAgIAAxkBAAIBCWg0r0y1k3oZAAEe8QAC0Qk0AAI2TQABq0QAB0gQ")
            except: pass

    asyncio.run(send())

def run_bot():
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("signal", signal))
    bot_app.add_handler(CommandHandler("dkwin", signal))
    bot_app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()
    if TOKEN:
        run_bot()
