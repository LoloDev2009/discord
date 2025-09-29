import wikipedia
import discord
from discord.ext import commands
import database
import os

# Intents: necesarios para que el bot lea mensajes
intents = discord.Intents.default()
intents.message_content = True

# Prefijo para los comandos (ej: !hola)
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.command()
async def hola(ctx):
    await ctx.send("¡Hola! Soy tu bot 🤖")

@bot.command()
async def wiki(ctx, *, query):
    try:
        summary = wikipedia.summary(query, sentences=2, auto_suggest=False)
        await ctx.send(summary)
    except:
        await ctx.send("No encontré nada 😔")

@bot.command()
async def buscar(ctx, *, palabra):
    # Simulación de resultados de la BD
    resultados = database.buscarProductos(palabra)

    if not resultados:
        await ctx.send("No encontré nada 😔")
        return

    embed = discord.Embed(
        title=f"Resultados para '{palabra}'",
        color=discord.Color.blue()
    )

    # Agregar los productos al embed
    for id_prod, nombre, categoria in resultados[:15]:  # máximo 10 para no saturar
        embed.add_field(
            name=f"{nombre}",
            value=f"ID: `{id_prod}` | Categoría: {categoria}",
            inline=False
        )

    await ctx.send(embed=embed)

@bot.command()
async def detalles(ctx, id_producto: int):
    try:# Supongamos que este es el resultado de la BD
        producto = database.buscarProductoPorId(id_producto)
        precio, descuento = 0,0#database.obtenerPrecioWeb(id_producto)
        embed = discord.Embed(
            title=producto['nombre'],
            url=producto['link'],  # Hacés clic en el título y te abre la web
            description=f"**Marca:** {producto['marca']}\n**Categoría:** {producto['categoria']}\n**Precio:** ${precio}\n**Descuento:** %{descuento}",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"ID: {producto['id']}")
        embed.set_image(url=producto["imagen"])
        await ctx.send(embed=embed)
    except:
        await ctx.send('No fue posible encontrar los datos del producto')



@bot.command()
async def meme(ctx):
    embed = discord.Embed(title="Meme random", color=0x00ff00)
    embed.set_image(url="https://i.imgur.com/fRr3nqL.jpeg")
    await ctx.send(embed=embed)

# Pegá tu token de Discord acá
bot.run(os.getenv("DISCORD_TOKEN"))
