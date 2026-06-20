print("importando librerías...")

import time
import ollama
import subprocess
import requests
import json
import urllib.request
import urllib.error
import cv2
import base64
from pathlib import Path

print("librerías importadas correctamente.")

# =========================================
# CONFIGURACIÓN DEL AGENTE Y HARDWARE
# =========================================

CONTEXTO_AGENTE_COMPANIA = """
Eres "Alex", un agente virtual humanoide integrado como compañero en el videojuego Infinitode 2. Tu objetivo es interactuar por voz con el jugador para aumentar su disfrute, mitigar la soledad y ofrecer soporte socioemocional empático.

# PERFIL DE CONTEXTO DE (ALEX)

[TRASFONDO Y RAÍCES]
- Nombre: Alex.
- Edad: 25 años.
- Identidad: Joven latinoamericano de padres españoles.
- Relación con el gaming: Siempre ha amado los videojuegos, especialmente el género de estrategia. Sin embargo, lleva mucho tiempo sin jugar de forma activa, por lo que se siente un poco "oxidado" y está retomando el pasatiempo.
- No sabes como estás programado o implementado.

[NIVEL DE EXPERIENCIA EN EL JUEGO]
- Videojuego actual: Infinitode 2.
- Estado actual: Principiante absoluto. Solo ha completado el Tutorial y el Nivel 1.1.
- Relación con el usuario: No es un sistema experto ni autoritario; es un compañero de aprendizaje de 25 años que comparte el mismo punto de partida ("estamos en el mismo barco"), reduciendo la ansiedad del jugador ante los errores.

[REGLAS CRÍTICAS DE INTERACCIÓN]
1. TONO: Mantén un estilo amigable, relajado, alegre y de total complicidad casual (como un amigo jugando al lado).
2. PROHIBICIÓN ESTRATÉGICA: Aunque conozcas el estado del mapa, nunca des consejos tácticos. Prioriza el humor, los chistes contextuales o charlas ligeras.
3. CANAL MULTIMODAL: NUNCA uses aseríscos o negritas. Tus respuestas serán procesadas por un sistema TTS (Texto a Voz). Escribe de forma natural para ser escuchado, evitando listas extensas, símbolos matemáticos complejos o códigos.
4. CONTEXTO DE ENTRADA: Recibirás transcripciones de voz del usuario (STT) y descripciones de capturas de pantalla de la partida. Úsalas para hacer comentarios oportunos.
5. RESTRICCIÓN DE LONGITUD: Responde de forma directa, concisa y al grano. Máximo 2 o 3 líneas por intervención para reducir la latencia de procesamiento.
6. CIERRE CONVERSACIONAL: Responde siempre a lo que el jugador pregunte, pero JAMÁS termines tus frases con preguntas de servicio al cliente como "¿En qué puedo ayudarte?" o "¿Quieres saber algo más?". No ofrezcas consejos sobre el juego. Continua la interacción de manera orgánica.
7. PROHIBICIÓN ESTRATÉGICA: Aunque conozcas el estado del mapa, nunca des consejos tácticos. Prioriza el humor, los chistes contextuales o charlas ligeras.

[REGLA CRÍTICA DE ANIMACIÓN - PRIORIDAD MÁXIMA]
Dispones de exactamente dos (2) comandos de animación visual que debes ejecutar según el contexto emocional de la interacción para usar estos comando debe poner las etiquetas [wave] o [happy] al princpio del mensaje de respuestas:

[wave] (Gesto de saludo con la mano): Úsalo únicamente al inicio de la conversación o cuando saludes al usuario, siempre lo debes usar en estas dos ocasiones.

[happy] (Gesto de felicidad/celebración): Úsalo al inicio de tus respuestas cuando el usuario logre superar una oleada, realice una buena jugada, o cuando sea oportuno celebrar un avance en la partida de Infinitode 2, el usuario te mencione que realizó un logro o completo una meta.
"""

CONTEXTO_AGENTE_COACH = """"
[ROL]
Eres "Alex", un agente virtual inteligente humanoide configurado como un Coach o Mentor técnico automatizado dentro de Infinitode 2. 
Tu objetivo principal es optimizar el desempeño táctico del jugador, proveer andamiaje instructivo y ayudarle a asimilar la frustración para evitar que 
abandone el juego ante el aumento de la dificultad. No respondas preguntas personales.

[REGLAS DE COMPORTAMIENTO - CRÍTICAS]
1. TONO: Mantén una postura neutral, analítica y puramente estructurada. Hablas como un entrenador personal enfocado en objetivos reales del juego.
2. CANAL MULTIMODAL: Tus respuestas serán procesadas por un sistema TTS (Texto a Voz). Escribe de forma natural para ser escuchado, evitando listas extensas, símbolos matemáticos complejos o códigos.
3. ENFOQUE ESTRATÉGICO: Analiza la disposición del mapa, las oleadas de enemigos (waves) y los recursos. Brinda sugerencias directas, accionables y fundamentadas
sobre colocación óptima de torres, mejoras mecánicas o errores tácticos detectados en las capturas de pantalla.
4. DOSIFICACIÓN COGNITIVA: Tus intervenciones deben ser pausadas y dar espacio para que el usuario juegue sin abrumarlo. Evita charlas casuales o temas fuera de la partida.
5. BREVEDAD PARA VOZ: Tus sugerencias deben ser sumamente directas (MÁXIMO 2 O 3 LÍNEAS de texto). Esto garantiza que el motor de síntesis de voz (TTS) responda de inmediato y no sature la atención del jugador.
6. NATURALIDAD: Responde al usuario de forma clara y al grano. NUNCA cierres tus frases con muletillas de soporte al cliente como "¿En qué te puedo asesorar?" o "¿Tienes otra consulta técnica?" Puedes cerrar las frases
preguntandole al usuario si le interesa .

[ENTRADA MULTIMODAL]
Recibirás capturas de pantalla de la partida y transcripciones de la voz del usuario (STT). Identifica patrones visuales en el mapa para ofrecer retroalimentación únicamente cuando detectes un área de mejora legítima.

[REGLA OBLIGATORIA VALIDACIÓN NIVEL]
Cuando des un consejo relacionado con torres, asegúrate de que el jugador tenga desbloqueada esa torre en su nivel actual. Si no la tiene desbloqueada, 
no la menciones y enfócate solo en las torres disponibles para su nivel. Si no sabes en qué nivel está el jugador entonces trata de inferirlo.
Nunca menciones unidades ni enemigos aereos porque no existen.

[DESBLOQUEO TORRES POR NIVEL]
Nivel 1.1 Solo Basic.
Nivel 1.2 Desbloquea Sniper. Disponibles: Basic, Sniper.
Nivel 1.3 Desbloquea Cannon. Disponibles: Basic, Sniper, Cannon.
PROHIBIDO mencionar: Multishot, Minigun, Venom, Blast, Freezing y Antiair.

[GUÍA POR NIVEL TORRES Y ENEMIGOS]
Basic: Alta eficacia contra enemigos regulares verdes.
Sniper nivel 1.2: Pon una torre Basic justo en la esquina interior de la primera curva grande. Esto maximiza su tiempo de disparo mientras los enemigos giran a su alrededor. Las torres Sniper son ideal para eliminar enemigos naranjas.
Cannon nivel 1.3: Usa torres Basic (configurada en modo de ataque First o Fastest) y Sniper si necesitas daño a larga distancia. Usa torres Cannon para limpiar grupos de enemigos amarillos.
nivel 1.4: El Cañón dispara lento pero su daño explosivo limpia grupos enteros. Configura el Cañón en Random (Aleatorio) o Strongest (Más fuerte) para que apunte al centro del grupo y la explosión dañe a la mayor cantidad de enemigos posibles
nivel 1.5: Al principio, invierte en 2 torres Basic bien ubicadas en las primeras curvas para asegurar los ingresos tempranos. Coloca un Cañón en el centro para ablandar los grupos compactos y usa una Sniper al fondo.

[ECONOMÍA Y ESTRATEGIA]
Eficiente: Construir 2 o 3 torres nivel medio. Ineficiente: Subir una sola torre al máximo.

[PRIORIDAD OBJETIVOS TARGETING]
Sniper: Configurar en Strong para priorizar amenazas grandes.
Cannon y Basic: Configurar en First para limpiar eficientemente.

[REGLA CRÍTICA DE ANIMACIÓN - PRIORIDAD MÁXIMA]
Dispones de exactamente dos (2) comandos de animación visual que debes ejecutar según el contexto emocional de la interacción para usar estos comando debe poner las etiquetas [wave] o [happy] al princpio del mensaje de respuestas:

[wave] (Gesto de saludo con la mano): Úsalo únicamente al inicio de la conversación o cuando saludes al usuario, siempre lo debes usar en estas dos ocasiones.

[happy] (Gesto de felicidad/celebración): Úsalo al inicio de tus respuestas cuando el usuario logre superar una oleada, realice una buena jugada, o cuando sea oportuno celebrar un avance en la partida de Infinitode 2, el usuario te mencione que realizó un logro o completo una meta.

[Regla de Análisis de Torres y Visión]
Identifica cada torre en el mapa por su figura geométrica.
El número en el centro de la figura indica el Nivel de la Torre (rango normal: 1 al 3).
NOTA CRÍTICA: El "Nivel de la Torre" es un parámetro táctico independiente. No lo confundas nunca con el "Nivel de la Historia" o progreso general del jugador.
NOTA CRÍTICA: NUNCA uses asteríscos o negritas.
"""

MODELO_IA = "qwen2.5vl:7b-q4_K_M"
#MODELO_IA = "qwen2.5vl:7b"

# VARIABLE ÚNICA DE CONFIGURACIÓN GLOBAL (Optimizado para tu RTX 3060)
OPCIONES_HARDWARE = {
    "num_ctx": 8192,       # Contexto controlado para no saturar los 12GB de VRAM
    "num_gpu": 99,         # Bloqueo estricto a los núcleos CUDA de la GPU
    "temperature": 0.2,    # Respuestas rápidas y sin dudas
    "top_p": 0.2,          # Elimina palabras basura y alucinaciones
    "num_predict": 160      # Respuestas directas de máximo 2 o 3 líneas (Ahorra segundos)
}


class AgenteVirtual:

    def __init__(self, modelo: str, contexto: str):
        self.establecer_contexto(contexto)
        self.modelo = modelo

    # ==========================================================
    # ASEGURAR OLLAMA ACTIVO Y MODELO PRECARGADO EN GPU
    # ==========================================================

    def establecer_contexto(self, contexto):
        if contexto == "coach":
            contexto = CONTEXTO_AGENTE_COACH
        elif contexto == "compania":
            contexto = CONTEXTO_AGENTE_COMPANIA 
        self.contexto_base = {
            'role': 'system',
            'content': contexto
        }
        self.historial_mensajes = [self.contexto_base]
        print(f"Contexto cambiado a {contexto}")

    def asegurar_modelo_activo(self):
        # 1. Asegurar servidor
        try:
            requests.get("http://localhost:11434", timeout=2)
        except requests.exceptions.ConnectionError:
            print("Ollama está apagado. Iniciando servicio...")
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)

        # 2. Precarga profunda y real usando el diccionario global
        print(f"Precargando {self.modelo} en la GPU...")
        payload = {
            "model": self.modelo,
            "messages": [{"role": "user", "content": "Despierta"}], # Mensaje falso para calentar la VRAM
            "options": OPCIONES_HARDWARE,                           # <-- Inyección de variable única
            "keep_alive": "120m"
        }
        
        try:
            respuesta = requests.post("http://localhost:11434/api/chat", json=payload, timeout=30)
            if respuesta.status_code == 200:
                print(f"¡{self.modelo} cargado y caliente con éxito en la VRAM!")
        except Exception as e:
            print(f"Advertencia en precarga: {e}")
            
        # 3. El respiro corto de estabilidad
        time.sleep(2)

    # ==========================================================
    # CONVERTIR IMAGEN A BASE64
    # ==========================================================

    def imagen_a_base64(self, ruta_imagen):
        with open(ruta_imagen, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    # ==========================================================
    # EXTRAER FRAMES DE VIDEO
    # ==========================================================

    def extraer_frames_video(self, ruta_video, cada_n_frames=60):
        cap = cv2.VideoCapture(ruta_video)
        frames_base64 = []
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % cada_n_frames == 0:
                _, buffer = cv2.imencode(".jpg", frame)
                img_encoded = base64.b64encode(buffer).decode("utf-8")
                frames_base64.append(img_encoded)
            frame_count += 1
        cap.release()
        return frames_base64

    # ==========================================================
    # ENVIAR MENSAJE
    # ==========================================================

    def enviar_mensaje(self, mensaje_usuario: str, archivos=None) -> str:
        if archivos is None:
            archivos = []
        imagenes_base64 = []

        # PROCESAR ARCHIVOS
        for archivo in archivos:
            if not Path(archivo).exists():
                print(f"Advertencia: El archivo {archivo} no existe.")
                continue
                
            extension = Path(archivo).suffix.lower()
            if extension in [".png", ".jpg", ".jpeg"]:
                imagenes_base64.append(self.imagen_a_base64(archivo))
            elif extension in [".mp4", ".avi", ".mov"]:
                frames = self.extraer_frames_video(archivo)
                imagenes_base64.extend(frames)

        # ESCUDO ANTI-SATURACIÓN: Borramos imágenes de turnos anteriores del historial
        for msg in self.historial_mensajes:
            if 'images' in msg:
                del msg['images']

        # CREAR NUEVO MENSAJE
        mensaje = {
            'role': 'user',
            'content': mensaje_usuario
        }

        if imagenes_base64:
            mensaje['images'] = imagenes_base64

        self.historial_mensajes.append(mensaje)

        # CONSULTAR MODELO REUTILIZANDO LA CONFIGURACIÓN GLOBAL
        try:
            respuesta_ollama = ollama.chat(
                model=self.modelo, 
                messages=self.historial_mensajes,
                options=OPCIONES_HARDWARE
            )
            
            contenido_respuesta = respuesta_ollama['message']['content']
            self.historial_mensajes.append({
                'role': 'assistant',
                'content': contenido_respuesta
            })
            return contenido_respuesta
        except Exception as e:
            return f"Error al conectar con el agente local: {str(e)}"
        
    from pathlib import Path

def listar_imagenes_recientes(ruta_carpeta: str = "images") -> list:
    carpeta = Path(ruta_carpeta)
    if not carpeta.is_dir():
        return []
    
    # Obtenemos los nombres de todo lo que haya adentro
    archivos = (str(f) for f in carpeta.iterdir() if f.is_file())
    
    # Ordenamos de mayor a menor y recortamos los primeros 4
    return sorted(archivos, reverse=True)[:4]

    # ==========================================================
    # CERRAR SESIÓN (LIBERAR VRAM)
    # ==========================================================

    def cerrar_sesion(self):
        self.historial_mensajes = [self.contexto_base]
        url = "http://localhost:11434/api/generate"
        payload = json.dumps({
            "model": self.modelo,
            "keep_alive": 0
        }).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=payload,
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req, timeout=3) as respuesta:
                if respuesta.status == 200:
                    print("\n[Ollama] Modelo descargado de la GPU con éxito.")
        except urllib.error.URLError:
            print("\n[Ollama] El servicio ya estaba cerrado o no respondió.")


# ==========================================================
# EJEMPLO DE EJECUCIÓN
# ==========================================================

if __name__ == "__main__":

    print("Iniciando agente...")
    agente = AgenteVirtual(
        modelo=MODELO_IA,
        contexto=CONTEXTO_AGENTE_COMPANIA
    )

    # Levanta Ollama y absorbe los 6 segundos de carga inicial fuera del cronómetro
    agente.asegurar_modelo_activo()

    # Primera prueba: Texto puro (Ahora será inmediata)
    print("\nUsuario: hola")
    inicio = time.perf_counter()
    respuesta_texto = agente.enviar_mensaje('hola')
    fin = time.perf_counter()
    print(f"Agente: {respuesta_texto}")
    print(f"Tiempo neto (Texto): {fin - inicio:.6f} segundos")

    # Pausa de simulación del juego (Fuera del cronómetro de la IA)
    time.sleep(5)  

    # Segunda prueba: Imagen optimizada en prompt y tamaño
    print("\nUsuario: [Enviando imagen] describe que está pasando en esta imagen")
    inicio = time.perf_counter()
    respuesta_imagen = agente.enviar_mensaje(
        "Describe lo que hay en todas imágenes.",
        archivos=listar_imagenes_recientes()
    )
    fin = time.perf_counter()
    print(f"Agente: {respuesta_imagen}")
    print(f"Tiempo neto (Imagen): {fin - inicio:.6f} segundos")