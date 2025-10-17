from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 💡 Sustituye esto por tu API key real
API_KEY = "TU_API_KEY_AQUI"

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Responde con el mismo mensaje que recibió
    text = update.message.text
    await update.message.reply_text(text)

def main():
    # Crea la aplicación
    app = ApplicationBuilder().token(API_KEY).build()

    # Añade el handler que responderá a todos los mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot en marcha. Pulsa Ctrl+C para detenerlo.")
    app.run_polling()

if __name__ == "__main__":
    main()
