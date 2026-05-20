import discord
from brain_db import MemoriaMoon
from allama_api import OllamaBrain
import os
from dotenv import load_dotenv
from personalidade import LunaPersonality
import user_db
import textos
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
memoria = MemoriaMoon()
ia = OllamaBrain(model_name="qwen2.5:3b")
moon = LunaPersonality()
user_db.inicializar()
ollama_lock = asyncio.Lock()

@client.event
async def on_ready():
    print(f'IA pronta e operante como {client.user}')

@client.event
async def on_message(message):
if message.author == client.user:
    return
if not any(mention.id == client.user.id for mention in message.mentions):
    return

    id_user = message.author.id
    nick_user = message.author.display_name
    user_db.inserirUsuario(id_user, nick_user)
    tuplaUsuario = user_db.buscarUsuario(id_user)

    if tuplaUsuario[3] is None and tuplaUsuario[4] >= 10:
        asyncio.create_task(gerar_e_salvar_apelido(message.channel, id_user, nick_user))

    lembrancas = memoria.recuperar(message.content, id_user)
    print(f"Lembranças: {lembrancas}")

    if lembrancas:
        texto_contexto = "\n".join(lembrancas)
        contexto_formatado = f"Lembranças de conversas passadas: {texto_contexto}"
    else:
        contexto_formatado = "Sem memórias anteriores sobre este assunto."

    system_prompt = f"""
{moon.formatar_prompt_sistema(id_user, nick_user)}

### REGRAS CRÍTICAS:
{textos.regras()}

### EXEMPLOS DE COMPORTAMENTO:
{textos.exemplos()}

### CONTEXTO:
{contexto_formatado}

LEMBRE-SE: Você É a Moon. Não é uma IA. Não é um assistente. Máximo 2 frases. Use kaomoji.
"""

    print(f"{nick_user} disse: {message.content}")
    async with message.channel.typing():
        async with ollama_lock:
            resposta = await ia.comunicar(system_prompt, message.content)

    await message.channel.send(resposta)
    memoria.guardar(f"Usuário disse: {message.content}. Você respondeu: {resposta}", id_user)

async def gerar_e_salvar_apelido(channel, id_user, nick_user):
    prompt_sistema = "Você cria apelidos criativos. Responda APENAS o apelido, nada mais, sem pontuação."
    prompt_user = f"Crie um apelido curto, fofo e levemente irritante para {nick_user}."
    
    async with ollama_lock:
        apelido = await ia.comunicar(prompt_sistema, prompt_user)
    
    apelido_limpo = apelido.strip().replace(".", "").replace('"', '')
    user_db.atualizarApelido(id_user, apelido_limpo)
    await channel.send(f"*(Moon olha para você pensativa)*... Cansei de falar seu nome. Agora vou te chamar de {apelido_limpo}! ٩(◕‿◕)۶")

client.run(TOKEN)

