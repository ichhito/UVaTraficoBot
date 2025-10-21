from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    CallbackQueryHandler, ContextTypes, filters
)
import config
key = config.get_key()

# ==== VISTAS / MENÚ ====
def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🗺️ Ver incidentes", callback_data="menu:check")],
        [InlineKeyboardButton("📝 Reportar incidente", callback_data="menu:report")],
        [InlineKeyboardButton("🔔 Suscripciones", callback_data="menu:subs")],
        [InlineKeyboardButton("❓ Ayuda", callback_data="menu:help")],
        [InlineKeyboardButton("ℹ️ Sobre el bot", callback_data="menu:about")]
    ])
def check_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏱️ Ver recientes", callback_data="menu:checkRecent")],
        [InlineKeyboardButton("🗺️ Ver cercanos", callback_data="menu:checkClose")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="menu:root")]
    ])

# ==== HANDLERS ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /start o volver al menú
    if update.message:
        await update.message.reply_text(
            "Elige una opción:",
            reply_markup=main_menu_keyboard()
        )
    else:
        # por si llega desde callback y queremos 'refrescar' el mensaje
        await update.callback_query.edit_message_text(
            "Elige una opción:",
            reply_markup=main_menu_keyboard()
        )

async def on_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enruta por callback_data del menú."""
    query = update.callback_query
    await query.answer()  # ack rápido para UX

    data = query.data  # p.ej. "menu:nearby"
    if data == "menu:check":
        # Aquí luego pedirás ubicación y listarás posts cercanos
        await query.edit_message_text(
            "Elige una opción: \n",
            reply_markup=check_menu_keyboard()
        )

    elif data == "menu:report":
        # Aquí puedes iniciar un "wizard" de reporte
        await query.edit_message_text(
            "📝 Vamos a reportar un incidente.\n"
            "1) Envíame la ubicación.\n"
            "2) Luego te pediré el tipo (retención/accidente/obra...).",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Volver", callback_data="menu:root")]
            ])
        )

    elif data == "menu:subs":
        await query.edit_message_text(
            "🔔 Suscripciones: podrás seguir una zona/vía y horario.\n"
            "Próximo paso: elegir zona o vía.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Volver", callback_data="menu:root")]
            ])
        )

    elif data == "menu:help":
        await query.edit_message_text(
            "❓ Ayuda\n\n"
            "• 🗺️ Ver cercanos: busca incidentes cerca de ti.\n"
            "• 📝 Reportar: crea un nuevo aviso con tu ubicación.\n"
            "• 🔔 Suscripciones: recibe alertas por zona/vía.\n\n"
            "Comandos: /start para volver al menú.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Volver", callback_data="menu:root")]
            ])
        )
    elif data == "menu:about":
        await query.edit_message_text(
            "ℹ️ Sobre el bot\n\n"
            "UVaTráfico Bot v1\\.0\n"
            "Desarrollado por Ichiro Hitomi\n"
            "[Github](https://github.com/ichhito/UVaTraficoBot)",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Volver", callback_data="menu:root")]
            ])
        )
    elif data == "menu:checkRecent":
        # Mostrar incidentes ordenados por fecha
        #PLACEHOLDER: En el caso real se sacaran los datos con una base de datos o algo asi
        await query.edit_message_text(
            "🕑 Incidentes recientes:\n"
            "1) Accidente en A-62 km 120\n"
            "2) Retención en Pº Zorrilla km 5\n"
            "3) Obras en Calle Real\n\n"
            "Selecciona una opción para más detalles.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Volver", callback_data="menu:check")]
            ])
        )

    elif data == "menu:checkClose":
        # Mostrar incidentes cercanos a la ubicación del usuario
        #PLACEHOLDER: En el caso real se sacaran los datos con una base de datos o algo asi
        await query.edit_message_text(
            "📍 Incidentes cercanos a tu ubicación:\n"
            "1) Retención en Calle Mayor (200m)\n"
            "2) Obras en Av. de la Constitución (500m)\n\n"
            "Selecciona una opción para más detalles.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Volver", callback_data="menu:check")]
            ])
        )


    elif data == "menu:root":
        # Volver al menú principal
        await start(update, context)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Responde con el mismo texto (lo mantengo como pediste)
    text = update.message.text
    await update.message.reply_text(text)

# (Opcional) Recibir ubicaciones ya desde ahora
async def on_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loc = update.message.location
    await update.message.reply_text(
        f"📍 Ubicación recibida: {loc.latitude:.5f}, {loc.longitude:.5f}\n"
        "Pronto te mostraré incidentes cercanos aquí."
    )

# ==== ARRANQUE ====
async def _setup_commands(app):
    # Menú de comandos del cliente (barra /)
    cmds = [
        BotCommand("start", "Abrir menú"),
        BotCommand("help", "Ayuda"),
    ]
    await app.bot.set_my_commands(cmds)

def main():
    app = ApplicationBuilder().token(key).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))

    # Menú (callbacks)
    app.add_handler(CallbackQueryHandler(on_menu_click, pattern=r"^menu:"))

    # Ubicaciones (si las envían desde el clip)
    app.add_handler(MessageHandler(filters.LOCATION, on_location))

    # Echo para cualquier texto que no sea comando
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Configura comandos visibles en el cliente
    app.post_init = _setup_commands

    print("🤖 Bot en marcha. Pulsa Ctrl+C para detenerlo.")
    app.run_polling()

if __name__ == "__main__":
    main()
