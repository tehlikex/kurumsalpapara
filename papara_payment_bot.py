import logging
import time
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from papara_api import get_account_balance, create_payment, check_payment
from database import init_db, get_balance, update_balance, add_payment, update_payment_status, get_payment
from config import PAPARA_API_KEY

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Yapılandırma bilgileri
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'

# Veritabanını başlatma
init_db()

# Ödeme bilgilerini saklamak için basit bir yapı
user_payments = {}

# Benzersiz açıklama oluşturma
def generate_unique_description(user_id):
    return f"payment_{user_id}_{int(time.time())}"

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Hoş geldiniz {user.mention_markdown_v2()}\! Papara ile ödeme yapmak için /pay komutunu kullanabilirsiniz\.',
    )

# /pay komutu
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    description = generate_unique_description(user.id)
    user_payments[user.id] = {'description': description}

    await update.message.reply_text(
        'Lütfen yatırmak istediğiniz tutarı girin (örneğin: 100):',
        reply_markup=ReplyKeyboardRemove()
    )

# /amount komutu
async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id in user_payments:
        try:
            amount = float(update.message.text)
            user_payments[user.id]['amount'] = amount

            # Veritabanına ödeme ekleme
            add_payment(user.id, user_payments[user.id]['description'], amount)

            keyboard = [['QR Kod', 'POS', 'Uygulama']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                'Lütfen ödeme yönteminizi seçin:',
                reply_markup=reply_markup
            )
        except ValueError:
            await update.message.reply_text('Geçersiz tutar. Lütfen doğru bir miktar girin (örneğin: 100).')
    else:
        await update.message.reply_text('Ödeme açıklamanız bulunamadı. Lütfen önce /pay komutunu kullanarak ödeme yapın.')

# /payment komutu
async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id in user_payments and 'amount' in user_payments[user.id]:
        amount = user_payments[user.id]['amount']
        description = user_payments[user.id]['description']
        payment_method = update.message.text

        payment_data = create_payment(description, amount)
        if payment_data:
            if payment_method == 'QR Kod':
                qr_url = payment_data['qrUrl']
                await update.message.reply_text(f'Ödemenizi tamamlamak için QR kodu tarayın: {qr_url}')
            elif payment_method == 'POS':
                pos_url = payment_data['posUrl']
                await update.message.reply_text(f'Ödemenizi tamamlamak için POS bağlantısını kullanın: {pos_url}')
            elif payment_method == 'Uygulama':
                mobile_url = payment_data['mobileUrl']
                await update.message.reply_text(f'Ödemenizi tamamlamak için Papara uygulamasını kullanın: {mobile_url}')
            else:
                await update.message.reply_text('Geçersiz ödeme yöntemi. Lütfen QR Kod, POS veya Uygulama seçin.')
        else:
            await update.message.reply_text('Ödeme oluşturulamadı. Lütfen tekrar deneyin.')
    else:
        await update.message.reply_text('Ödeme açıklamanız veya miktarınız bulunamadı. Lütfen önce /pay komutunu kullanarak ödeme yapın.')

# /confirm komutu
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id in user_payments:
        description = user_payments[user.id]['description']
        await update.message.reply_text('Ödemenizi kontrol ediyoruz, lütfen bekleyin...')

        if check_payment(description):
            await update.message.reply_text('Ödemeniz başarıyla alındı! Teşekkür ederiz.')

            # Ödeme durumunu ve kullanıcı bakiyesini güncelle
            update_payment_status(description, 'completed')
            payment_info = get_payment(description)
            update_balance(user.id, payment_info[2])  # payment_info[2] = amount
            del user_payments[user.id]
        else:
            await update.message.reply_text('Henüz ödeme alınmadı. Lütfen tekrar kontrol edin.')
    else:
        await update.message.reply_text('Ödeme açıklamanız bulunamadı. Lütfen önce /pay komutunu kullanarak ödeme yapın.')

# /balance komutu
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    balance = get_balance(user.id)
    if balance is not None:
        await update.message.reply_text(f'Bakiyeniz: {balance} TL')
    else:
        await update.message.reply_text('Bakiyeniz bulunmamaktadır.')

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Komut işleyicileri
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pay", pay))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, amount))
    application.add_handler(CommandHandler("payment", payment))
    application.add_handler(CommandHandler("confirm", confirm))
    application.add_handler(CommandHandler("balance", balance))

    # Botu başlatma
    application.run_polling()

if __name__ == '__main__':
    main()
