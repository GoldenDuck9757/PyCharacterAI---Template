import discord
from discord.ext import commands
import asyncio
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError

# Configurações
DISCORD_TOKEN = "SEU_DISCORD_BOT_TOKEN"
CHARACTER_AI_TOKEN = "SEU_CHARACTER_AI_TOKEN"
CHARACTER_ID = "SEU_CHARACTER_ID"

# Inicializa o cliente do Discord
intents = discord.Intents.default()
intents.messages = True  # Permite capturar mensagens
intents.message_content = True  # Permite acessar o conteúdo das mensagens
bot = commands.Bot(command_prefix="!", intents=intents)

# Inicializa o cliente do Character.AI
character_client = None
character_chat = None


@bot.event
async def on_ready():
    global character_client, character_chat

    # Configura o cliente do Character.AI
    character_client = await get_client(token=CHARACTER_AI_TOKEN)
    me = await character_client.account.fetch_me()
    print(f"Authenticated as @{me.username}")

    # Cria um novo chat
    character_chat, greeting_message = await character_client.chat.create_chat(CHARACTER_ID)
    print(f"Chat iniciado com: {greeting_message.get_primary_candidate().text}")

    print(f"Bot conectado como {bot.user}!")


@bot.event
async def on_message(message):
    global character_chat

    # Evita responder a si mesmo
    if message.author == bot.user:
        return

    # Verifica se o bot foi mencionado
    if bot.user.mentioned_in(message):
        try:
            # Obtém a mensagem do usuário
            user_message = message.clean_content.replace(f"@{bot.user.name}", "").strip()

            # Envia a mensagem ao Character.AI
            answer = await character_client.chat.send_message(
                CHARACTER_ID,
                character_chat.chat_id,
                user_message
            )

            # Obtém o texto da resposta
            response_text = answer.get_primary_candidate().text

            # Envia a resposta como reply
            await message.reply(response_text)
        except SessionClosedError:
            await message.reply("A sessão foi encerrada. Por favor, reinicie o bot.")
        except Exception as e:
            print(f"Erro: {e}")
            await message.reply("Ocorreu um erro ao processar sua mensagem. Tente novamente.")


@bot.event
async def on_disconnect():
    global character_client

    # Fecha a sessão do Character.AI ao desconectar
    if character_client:
        await character_client.close_session()
        print("Sessão do Character.AI encerrada.")


# Inicia o bot do Discord
bot.run(DISCORD_TOKEN)
