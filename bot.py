import os
import ccxt
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ====== LOAD SECRETS FROM ENVIRONMENT ======
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
EXCHANGE = os.getenv("EXCHANGE", "binance")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# ====== CONNECT TO EXCHANGE ======
exchange = getattr(ccxt, EXCHANGE)({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "enableRateLimit": True,
})

# ====== TELEGRAM COMMANDS ======

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 MemeCoinBot online!\n\n"
        "Commands:\n"
        "/price <symbol>   → e.g. /price PEPE/USDT\n"
        "/buy <symbol> <amount>\n"
        "/sell <symbol> <amount>"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /price PEPE/USDT")
        return
    symbol = context.args[0].upper()
    try:
        ticker = exchange.fetch_ticker(symbol)
        await update.message.reply_text(f"{symbol} price: {ticker['last']:.8f} USDT")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /buy PEPE/USDT 10")
        return
    symbol = context.args[0].upper()
    amount = float(context.args[1])
    try:
        exchange.create_market_buy_order(symbol, amount)
        await update.message.reply_text(f"✅ Bought {amount} {symbol}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /sell PEPE/USDT 10")
        return
    symbol = context.args[0].upper()
    amount = float(context.args[1])
    try:
        exchange.create_market_sell_order(symbol, amount)
        await update.message.reply_text(f"✅ Sold {amount} {symbol}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ====== RUN BOT ======
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("sell", sell))
    print("MemeCoinBot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
