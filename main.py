import discord
from brain_db import MemoriaMoon
from allama_api import OllamaBrain
import os
from dotenv import load_dotenv
from personalidade import LunaPersonality
import user_db
import textos
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

memoria = MemoriaMoon()
ia = OllamaBrain(model_name="llama3.1:8B")
moon = LunaPersonality()
user_db.inicializar()

@client.event
async def on_ready():
    print(f'IA pronta e operante como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if client.user not in message.mentions:
        return
    
    id_user = message.author.id
    nick_user = message.author.display_name

    user_db.inserirUsuario(id_user,nick_user)

    tuplaUsuario = user_db.buscarUsuario(id_user)

    if tuplaUsuario[3] == None and tuplaUsuario[4] >= 10:
        asyncio.create_task(gerar_e_salvar_apelido(message.channel, id_user, nick_user))

    system_prompt = moon.formatar_prompt_sistema(id_user, nick_user)

    lembrancas = memoria.recuperar(message.content, id_user)
    print(f"Lembranças: {lembrancas}")

    exemplosDeFala = textos.exemplos()
    
    regras = textos.regras()





    if lembrancas:
        texto_contexto = "\n".join(lembrancas)
        contexto_formatado = f"Aqui estão algumas lembranças de conversas passadas: {texto_contexto}"
    else:
        contexto_formatado = "Não tens memórias anteriores sobre este assunto com este utilizador."

    prompt_final = f"""

                    {system_prompt} 

                    ### REGRAS CRÍTICAS (LEIA ANTES DE RESPONDER):
                    {regras}

                    ### EXEMPLOS DE COMPORTAMENTO:
                    {exemplosDeFala}

                    ### HISTÓRICO DA CONVERSA (Contexto):
                    {contexto_formatado}

                    ### ÚLTIMA MENSAGEM RECEBIDA:
                    fala de {nick_user}: {message.content}

                    ### LEMBRE-SE: Você é a Moon. Máximo 2 frases Se passar disso, você desliga. Use kaomoji.
                    
                    Moon:
                """

    print(f"{nick_user} disse: {message.content}")
    
    async with message.channel.typing():
        resposta = await ia.comunicar(prompt_final)
        await message.channel.send(resposta)

    memoria.guardar(f"Usuário disse: {message.content}. Você respondeu: {resposta}", id_user)

async def gerar_e_salvar_apelido(channel, id_user, nick_user):
    loop = asyncio.get_event_loop()
    
    prompt_apelido = f"Crie um apelido curto, fofo e levemente irritante para {nick_user}. Responda APENAS o apelido, nada mais."

    apelido = await loop.run_in_executor(executor, ia.comunicar_sincrono, prompt_apelido)
    
    apelido_limpo = apelido.strip().replace(".", "").replace('"', '')
    
    user_db.atualizarApelido(id_user, apelido_limpo)
    await channel.send(f"*(Moon olha para você pensativa)*... Cansei de falar seu nome. Agora vou te chamar de {apelido_limpo}! ٩(◕‿◕)۶")

client.run(TOKEN)

