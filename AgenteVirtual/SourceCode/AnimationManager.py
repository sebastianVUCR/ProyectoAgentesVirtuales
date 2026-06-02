import asyncio
import websockets

HOST = "127.0.0.1"
PORT = 8999

cliente_conectado = None

async def manejar_cliente(websocket):
    global cliente_conectado

    cliente_conectado = websocket
    print("✅ Unity conectado")

    try:
        await websocket.wait_closed()
    finally:
        print("❌ Unity desconectado")
        cliente_conectado = None

async def consola():
    global cliente_conectado

    while True:
        mensaje = await asyncio.to_thread(
            input,
            "\nEscriba una instrucción (Talk, Idle): "
        )

        if cliente_conectado is None:
            print("⚠ No hay ningún cliente conectado.")
            continue

        try:
            await cliente_conectado.send(mensaje)
            print(f"📤 Enviado: {mensaje}")
        except Exception as e:
            print(f"Error enviando mensaje: {e}")

async def main():
    servidor = await websockets.serve(
        manejar_cliente,
        HOST,
        PORT
    )

    print(f"🚀 Servidor iniciado en ws://{HOST}:{PORT}")

    await asyncio.gather(
        consola(),
        servidor.wait_closed()
    )

if __name__ == "__main__":
    asyncio.run(main())