import random

class AgenteVirtualMock:
    def __init__(self):
        """
        Constructor de la clase. Inicializa las variables base.
        """
        self.contexto = None
        self.modelo_activo = False
        print("[Mock] Agente Virtual inicializado.")

    def establecer_contexto(self, contexto):
        """
        Guarda el contexto asignado para la simulación.
        """
        self.contexto = contexto
        print(f"[Mock] Contexto establecido: {self.contexto}")

    def asegurar_modelo_activos(self):
        """
        Simula la verificación y activación del modelo.
        """
        self.modelo_activo = True
        print("[Mock] Modelo verificado y activo.")

    def enviar_mensaje(self, mensaje_usuario: str, archivos=None) -> str:
        """
        Simula el envío de un mensaje y devuelve una respuesta aleatoria
        basada en un generador de números entre 1 y 3.
        """
        # Aseguramos que el modelo esté listo antes de procesar
        self.asegurar_modelo_activos()
        
        print(f"[Mock] Mensaje recibido del usuario: '{mensaje_usuario}'")
        if archivos:
            print(f"[Mock] Archivos adjuntos procesados: {archivos}")

        # Generador de números aleatorios entre 1 y 3
        numero_aleatorio = random.randint(1, 3)

        # Selección de la respuesta según el número obtenido
        if numero_aleatorio == 1:
            respuesta = "Hoy es un bonito día para jugar Infinitode 2."
        elif numero_aleatorio == 2:
            respuesta = "[wave] ¡Hola! Soy Alex. Muchos gusto en conocerte."
        else:
            respuesta = "[happy] ¡Felicidades! Ese es un gran logro"

        return respuesta