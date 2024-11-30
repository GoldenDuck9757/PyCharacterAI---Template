import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError

# Configurações
API_TOKEN = "SEU_TELEGRAM_BOT_TOKEN"
CHARACTER_AI_TOKEN = "SEU_CHARACTER_AI_TOKEN"
CHARACTER_ID = "SEU_CHARACTER_ID"

# Configura o log do Telegram
logging.basicConfig(level=logging.INFO)

# Inicializa o bot do Telegram e o Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Inicializa o cliente do Character.AI
character_client = None
character_chat = None


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    global character_client, character_chat

    # Configura o cliente do Character.AI
    character_client = await get_client(token=CHARACTER_AI_TOKEN)
    me = await character_client.account.fetch_me()
    print(f"Authenticated as @{me.username}")

    # Cria um novo chat
    character_chat, greeting_message = await character_client.chat.create_chat(CHARACTER_ID)
    print(f"Chat iniciado com: {greeting_message.get_primary_candidate().text}")

    # Envia uma mensagem inicial
    await message.answer("Bot iniciado. Envie uma mensagem e eu responderei.")


@dp.message_handler()
async def handle_message(message: types.Message):
    global character_chat

    # Evita que o bot responda a si mesmo
    if message.from_user.id == bot.id:
        return

    try:
        # Envia a mensagem ao Character.AI
        user_message = message.text.strip()

        answer = await character_client.chat.send_message(
            CHARACTER_ID,
            character_chat.chat_id,
            user_message
        )

        # Obtém a resposta do Character.AI
        response_text = answer.get_primary_candidate().text

        # Envia a resposta de volta ao Telegram
        await message.reply(response_text)

    except SessionClosedError:
        await message.reply("A sessão foi encerrada. Por favor, reinicie o bot.")
    except Exception as e:
        print(f"Erro: {e}")
        await message.reply("Ocorreu um erro ao processar sua mensagem. Tente novamente.")


async def on_shutdown(dp):
    # Fecha a sessão do Character.AI ao desligar
    if character_client:
        await character_client.close_session()
        print("Sessão do Character.AI encerrada.")


if __name__ == '__main__':
    # Inicia o bot do Telegram
    from aiogram import executor
    executor.start_polling(dp, on_shutdown=on_shutdown)
                    
