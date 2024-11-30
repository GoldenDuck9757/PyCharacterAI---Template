
Este repositório contém exemplos básicos de bots que se integram ao **Character.AI**, usando a biblioteca **PyCharacterAI**. Com esses códigos, você pode criar bots personalizados no Discord e no Telegram que se comunicam com um personagem do **Character.AI**.

🔗 **PyCharacterAI**: [GitHub Repositório PyCharacterAI](https://github.com/Xtr4F/PyCharacterAI)

---

## 💡 Funcionalidade

Esses bots utilizam a API do **Character.AI** para enviar mensagens para o personagem selecionado e obter respostas de volta. Você pode usar os exemplos como base para seus próprios bots em plataformas como Discord ou Telegram.

### 🔍 Como Funciona:
1. O bot captura as mensagens dos usuários na plataforma de escolha (Discord ou Telegram).
2. Quando o bot é mencionado ou recebe uma mensagem, ele envia essa mensagem para o Character.AI usando a **API PyCharacterAI**.
3. O **Character.AI** gera uma resposta com base no comportamento do personagem configurado.
4. O bot responde ao usuário com a mensagem gerada pelo **Character.AI**.

---

## ⚙️ Como Usar

### 1. **Configuração do Bot no Discord** 🎮

Este código cria um bot básico do **Discord** que interage com um personagem do **Character.AI**. Para rodar o bot, siga os seguintes passos:

#### 📝 Requisitos:
- Python 3.8 ou superior
- Instalar as dependências:
    ```bash
    pip install discord PyCharacterAI
    ```

#### 📄 Código Base do Bot para Discord:
```python
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
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Inicializa o cliente do Character.AI
character_client = None
character_chat = None

@bot.event
async def on_ready():
    global character_client, character_chat
    character_client = await get_client(token=CHARACTER_AI_TOKEN)
    me = await character_client.account.fetch_me()
    print(f"Authenticated as @{me.username}")
    character_chat, greeting_message = await character_client.chat.create_chat(CHARACTER_ID)
    print(f"Chat iniciado com: {greeting_message.get_primary_candidate().text}")
    print(f"Bot conectado como {bot.user}!")

@bot.event
async def on_message(message):
    global character_chat
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        try:
            user_message = message.clean_content.replace(f"@{bot.user.name}", "").strip()
            answer = await character_client.chat.send_message(CHARACTER_ID, character_chat.chat_id, user_message)
            response_text = answer.get_primary_candidate().text
            await message.reply(response_text)
        except SessionClosedError:
            await message.reply("A sessão foi encerrada. Por favor, reinicie o bot.")
        except Exception as e:
            print(f"Erro: {e}")
            await message.reply("Ocorreu um erro ao processar sua mensagem. Tente novamente.")

@bot.event
async def on_disconnect():
    global character_client
    if character_client:
        await character_client.close_session()
        print("Sessão do Character.AI encerrada.")

bot.run(DISCORD_TOKEN)

Substitua os seguintes valores:

SEU_DISCORD_BOT_TOKEN: O token do seu bot no Discord.

SEU_CHARACTER_AI_TOKEN: O token da sua conta do Character.AI.

SEU_CHARACTER_ID: O ID do personagem com o qual deseja interagir.



---

2. Configuração do Bot no Telegram 📱

Este código cria um bot básico do Telegram que interage com um personagem do Character.AI. O funcionamento é similar ao do bot do Discord.

📝 Requisitos:

Python 3.8 ou superior

Instalar as dependências:

pip install aiogram PyCharacterAI


📄 Código Base do Bot para Telegram:

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
    character_client = await get_client(token=CHARACTER_AI_TOKEN)
    me = await character_client.account.fetch_me()
    print(f"Authenticated as @{me.username}")
    character_chat, greeting_message = await character_client.chat.create_chat(CHARACTER_ID)
    print(f"Chat iniciado com: {greeting_message.get_primary_candidate().text}")
    await message.answer("Bot iniciado. Envie uma mensagem e eu responderei.")

@dp.message_handler()
async def handle_message(message: types.Message):
    global character_chat
    if message.from_user.id == bot.id:
        return
    try:
        user_message = message.text.strip()
        answer = await character_client.chat.send_message(CHARACTER_ID, character_chat.chat_id, user_message)
        response_text = answer.get_primary_candidate().text
        await message.reply(response_text)
    except SessionClosedError:
        await message.reply("A sessão foi encerrada. Por favor, reinicie o bot.")
    except Exception as e:
        print(f"Erro: {e}")
        await message.reply("Ocorreu um erro ao processar sua mensagem. Tente novamente.")

async def on_shutdown(dp):
    if character_client:
        await character_client.close_session()
        print("Sessão do Character.AI encerrada.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_shutdown=on_shutdown)

Substitua os seguintes valores:

SEU_TELEGRAM_BOT_TOKEN: O token do seu bot no Telegram.

SEU_CHARACTER_AI_TOKEN: O token da sua conta do Character.AI.

SEU_CHARACTER_ID: O ID do personagem com o qual deseja interagir.



---

🛠️ Como Contribuir

Sinta-se à vontade para contribuir para este projeto! Se você tiver melhorias, correções de bugs ou novas funcionalidades, abra um Pull Request. Certifique-se de seguir as melhores práticas de desenvolvimento e escrever testes quando necessário.


---

📜 Licença

Este projeto está licenciado sob a MIT License - consulte o arquivo LICENSE para mais detalhes.


---
