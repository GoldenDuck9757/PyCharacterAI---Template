import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError, CreateError

# Configurações
API_TOKEN = "SEU_TELEGRAM_BOT_TOKEN"
CHARACTER_AI_TOKEN = "SEU_CHARACTER_AI_TOKEN"
CHARACTER_ID = "SEU_CHARACTER_ID"  # Verifique se esse ID está correto

# Configura o log do Telegram (Reduzindo a verbosidade)
logging.basicConfig(level=logging.WARNING)  # Mostra apenas warnings e erros

# Inicializa o bot do Telegram
bot = Bot(token=API_TOKEN)

# Inicializa o cliente do Character.AI
character_client = None
character_chat = None

# Inicializa o Dispatcher
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def create_chat():
    global character_client, character_chat

    try:
        # Configura o cliente do Character.AI
        character_client = await get_client(token=CHARACTER_AI_TOKEN)
        me = await character_client.account.fetch_me()
        print(f"Authenticated as @{me.username}")

        # Verifica se há um chat existente e tenta criá-lo
        if character_chat is None:
            try:
                # Cria um novo chat com o personagem, verificando se o CHARACTER_ID é válido
                character_chat, greeting_message = await character_client.chat.create_chat(CHARACTER_ID)
                print(f"Chat iniciado com: {greeting_message.get_primary_candidate().text}")
            except CreateError as e:
                print(f"Erro ao criar o chat: {str(e)}")
                return "Erro ao criar o chat. Verifique o ID do personagem."

    except Exception as e:
        print(f"Erro na inicialização do bot: {str(e)}")
        return "Erro ao inicializar o cliente do Character.AI."

    return "Chat criado com sucesso!"

# Função para lidar com as mensagens recebidas
async def handle_message(message: types.Message):
    global character_chat

    # Evita que o bot responda a si mesmo
    if message.from_user.id == bot.id:
        return

    # Ignora o comando "/start" e outras mensagens sem conteúdo relevante
    if message.text.strip().lower() == "/start":
        return

    try:
        # Envia a mensagem ao Character.AI
        user_message = message.text.strip()

        # Envia a mensagem ao Character.AI, buscando a resposta
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

# Função que é executada quando o bot é desligado
async def on_shutdown(dp):
    # Fecha a sessão do Character.AI ao desligar
    if character_client:
        await character_client.close_session()
        print("Sessão do Character.AI encerrada.")

# Função principal que inicia o bot e cria o chat
async def main():
    result = await create_chat()
    print(result)  # Exibe o status da criação do chat

    # Registra o handler de mensagens
    dp.message()(handle_message)

    # Inicia o bot com um loop mais eficiente
    await dp.start_polling(bot, on_shutdown=on_shutdown)

if __name__ == '__main__':
    # Chama a função principal
    asyncio.run(main())