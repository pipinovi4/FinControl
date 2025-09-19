"""Entry‑point for FinRadarOffice bot."""
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from handlers.form import start, handle, cancel, FORM
from config import TELEGRAM_TOKEN

app = Application.builder().token("8141477114:AAHnyYuamVB0qQ8FodClq20LHbtkJkUN_mY").build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={FORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle)]},
    fallbacks=[CommandHandler("cancel", cancel)],
)
app.add_handler(conv)
print("FinBot is running… (Ctrl‑C to stop)")
app.run_polling()