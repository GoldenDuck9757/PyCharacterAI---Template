import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PyCharacterAI import get_client

# Tokens e IDs
TELEGRAM_TOKEN = "TokenTelegram"
CHARACTER_AI_TOKEN = "ChToken"
CHARACTER_ID = "ChId"

# Variáveis globais
character_client = None
chat_id = None

async def initialize_character_ai():
    """Inicializa o cliente do Character AI e cria um novo chat."""
    global character_client, chat_id
    character_client = await get_client(token=CHARACTER_AI_TOKEN)
    chat, _ = await character_client.chat.create_chat(CHARACTER_ID)
    chat_id = chat.chat_id
    print(f"Chat inicializado com ID: {chat_id}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start para inicializar a sessão."""
    global character_client
    if character_client is None:
        await initialize_character_ai()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde às mensagens do usuário."""
    global character_client, chat_id

    if character_client is None:
        await update.message.reply_text("Erro: Use o comando /start para inicializar o bot.")
        return

    user_message = update.message.text
    try:
        # Exibe "escrevendo" na barra de ações do chat
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        # Envia a mensagem ao Character AI e obtém a resposta
        response = await character_client.chat.send_message(CHARACTER_ID, chat_id, user_message)
        reply_text = response.get_primary_candidate().text.strip()

        # Responde diretamente à mensagem do usuário
        await update.message.reply_text(reply_text)
    except Exception as e:
        await update.message.reply_text(f"Erro ao processar a mensagem: {e}")

async def shutdown():
    """Fecha a sessão do cliente ao encerrar o bot."""
    global character_client
    if character_client:
        await character_client.close_session()
        print("Sessão encerrada.")

def main():
    """Função principal para iniciar o bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Configuração dos handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Executa o bot
    application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
