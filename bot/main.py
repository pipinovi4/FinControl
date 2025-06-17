"""Entry‑point for FinRadarOffice bot."""
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from handlers.form import start, handle, cancel, FORM
from config import TELEGRAM_TOKEN

app = Application.builder().token(TELEGRAM_TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={FORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle)]},
    fallbacks=[CommandHandler("cancel", cancel)],
)
app.add_handler(conv)
print("FinBot is running… (Ctrl‑C to stop)")
app.run_polling()