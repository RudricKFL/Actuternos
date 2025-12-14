import discord
import asyncio
import requests
import os

# Datos del bot desde variables de entorno
TOKEN = os.environ["TOKEN"]
CANAL_ID = int(os.environ["CANAL_ID"])
SERVER_IP = os.environ["SERVER_IP"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)

estado_anterior = None

async def comprobar_estado():
    global estado_anterior
    await client.wait_until_ready()

    canal = client.get_channel(CANAL_ID)

    try:
        # Comprobación inicial nada más arrancar
        respuesta = requests.get(
            f"https://api.mcsrvstat.us/2/{SERVER_IP}",
            timeout=10
        ).json()

        estado_anterior = respuesta.get("online", False)

        if estado_anterior:
            await canal.send("@everyone Estado actual del servidor: **ONLINE** ✅")
        else:
            await canal.send("@everyone Estado actual del servidor: **OFFLINE** ❌")

    except Exception as e:
        print("Error en comprobación inicial:", e)

    # Bucle continuo para detectar cambios de estado
    while not client.is_closed():
        try:
            respuesta = requests.get(
                f"https://api.mcsrvstat.us/2/{SERVER_IP}",
                timeout=10
            ).json()

            estado_actual = respuesta.get("online", False)

            if estado_actual != estado_anterior:
                if estado_actual:
                    await canal.send("@everyone El servidor está **ONLINE** ✅")
                else:
                    await canal.send("@everyone El servidor está **OFFLINE** ❌")

                estado_anterior = estado_actual

        except Exception as e:
            print("Error comprobando estado:", e)

        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")
    client.loop.create_task(comprobar_estado())

client.run(TOKEN)
