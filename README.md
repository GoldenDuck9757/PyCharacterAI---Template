# **PyCharacterAI Templates**  

![Banner](https://via.placeholder.com/1000x300?text=PyCharacterAI+Templates)  

Este repositório apresenta **templates otimizados e prontos para uso** que permitem integrar a biblioteca [PyCharacterAI](https://github.com/Xtr4F/PyCharacterAI) com bots no **Discord** e **Telegram**. Esses exemplos foram criados como **bases profissionais**, ampliando as funcionalidades disponíveis no repositório oficial.  

---

## **Sobre o PyCharacterAI**  
O [PyCharacterAI](https://github.com/Xtr4F/PyCharacterAI) é uma biblioteca para integração com o Character.AI através de sua API não oficial. Ela possibilita que você crie interações avançadas com personagens virtuais diretamente em suas plataformas favoritas. Este repositório oferece templates prontos para integrar bots no Discord e Telegram, com configurações práticas e de fácil personalização.  

---

## **Funcionalidades dos Templates**  

### **1. Template para Discord**
- **Descrição**: Cria um bot no Discord que responde quando mencionado diretamente no chat. Ele se conecta ao **Character.AI**, envia mensagens do usuário para o personagem escolhido e retorna as respostas automaticamente.
- **Principais Características**:
  - Respostas automáticas a menções.
  - Gerenciamento de sessão do Character.AI com tratamento de erros.
  - Fácil configuração com suporte a mensagens.
  
> **Código**: O código para o bot do Discord pode ser encontrado diretamente neste repositório. É necessário copiar e colar o template de código que está disponível acima neste arquivo `import discord
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
bot.run(DISCORD_TOKEN)`.  

### **2. Template para Telegram**
- **Descrição**: Cria um bot do Telegram que interage diretamente com o Character.AI, respondendo a todas as mensagens de texto recebidas.
- **Principais Características**:
  - Inicialização com o comando `/start`.
  - Gerenciamento automático de mensagens e respostas.
  - Sistema de fallback para tratar erros na conexão com o Character.AI.
  
> **Código**: O código para o bot do Telegram também está disponível acima neste `README.md`. Copie e cole o template para configurar facilmente o bot.  

---

## **Como Utilizar**

### **Requisitos**  
Antes de começar, certifique-se de ter os seguintes requisitos:
1. **Python 3.8 ou superior**.
2. Instale as dependências necessárias com o seguinte comando:
    ```bash
    pip install discord.py aiogram PyCharacterAI
    ```

3. **Tokens Necessários**:
    - **Discord Bot Token**: Obtenha em [Discord Developer Portal](https://discord.com/developers/applications).
    - **Telegram Bot Token**: Configure com o [BotFather](https://core.telegram.org/bots).
    - **Character.AI Token**: Obtenha seu token e o ID do personagem seguindo as orientações no repositório oficial do [PyCharacterAI](https://github.com/Xtr4F/PyCharacterAI).

### **Passos para Implementação**  
1. **Substitua os Tokens**: No código dos templates, substitua as variáveis `SEU_DISCORD_BOT_TOKEN`, `SEU_TELEGRAM_BOT_TOKEN`, `SEU_CHARACTER_AI_TOKEN`, e `SEU_CHARACTER_ID` com as informações correspondentes.
2. **Personalize conforme necessário**: Sinta-se à vontade para modificar o comportamento dos bots, adicionando comandos personalizados ou ajustando como as mensagens são processadas.

---

## **Licença e Créditos**  
Este projeto é baseado no repositório [PyCharacterAI](https://github.com/Xtr4F/PyCharacterAI), que fornece a API para integração com o Character.AI. O código foi **modificado e aprimorado** para criar templates otimizados para bots no Discord e Telegram.  
Sinta-se à vontade para contribuir ou adaptar os códigos conforme necessário!  

---
