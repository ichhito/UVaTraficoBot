from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import config
key = config.get_key()
# 💡 Sustituye esto por tu API key real
print(key) #Prueba

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Responde con el mismo mensaje que recibió
    text = update.message.text
    await update.message.reply_text(text)

def main():
    # Crea la aplicación
    app = ApplicationBuilder().token(key).build()

    # Añade el handler que responderá a todos los mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot en marcha. Pulsa Ctrl+C para detenerlo.")
    app.run_polling()

if __name__ == "__main__":
    main()
