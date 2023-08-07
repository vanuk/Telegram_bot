import ccxt
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Ваш API token від BotFather
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Ключі для доступу до API Binance
BINANCE_API_KEY = 'YOUR_BINANCE_API_KEY'
BINANCE_API_SECRET = 'YOUR_BINANCE_API_SECRET'

# Ініціалізація об'єкту біржі Binance
exchange = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_API_SECRET,
})

def get_account_balance():
    balance = exchange.fetch_balance()
    filtered_balance = {currency: amount for currency, amount in balance['total'].items() if amount > 0.0000001}
    return filtered_balance

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привіт! Відправте /balance, щоб отримати баланс валют з Binance.')

def balance(update: Update, context: CallbackContext) -> None:
    account_balance = get_account_balance()
    response = 'Баланс валют з біржі Binance:\n\n'
    for currency, amount in account_balance.items():
        response += f'{currency}: {amount}\n'
    update.message.reply_text(response)

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("balance", balance))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
