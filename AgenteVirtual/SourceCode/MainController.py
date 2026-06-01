import json
import time
import queue
import threading
import os

# IMPORTACIONES DE MIS MÓDULOS
from QwenIntegration import AgenteVirtual, MODELO_IA, CONTEXTO_AGENTE_COMPANIA, listar_imagenes_recientes
from FasterWhisperIntegration import WhisperSTTContinuo
from TTS.PiperIntegration import ReproductorTTS
from dataCollector import generate_data

class ControladorJuegoIA:
    def __init__(self):
        print("🚀 Inicializando el sistema integrado de IA...")
        
        # 1. Crear la cola que usará el STT para enviarnos los textos detectados
        self.cola_transcripciones = queue.Queue()
        self.ejecutando = True
        self.modo = self.leer_configuracion(etiqueta="modo")

        # 2. Inicializar los componentes pasándole la cola al STT
        self.tts = ReproductorTTS()
        
        self.agente_llm = AgenteVirtual(
            modelo=MODELO_IA,
            contexto=self.modo
        )
        
        # Pasamos self.cola_transcripciones al inicializador
        self.stt = WhisperSTTContinuo(
            model_size="small", 
            device="cpu", 
            compute_type="int8",
            cola_salida_texto=self.cola_transcripciones 
        )

        self.default_prompt = "Describe lo que hay en todas imágenes."

    def bucle_interaccion_principal(self):
        """Maneja el flujo lógico de eventos."""
        print("\n🤖 El Agente Alex está escuchando... (Presiona Ctrl+C para salir)")
        
        while self.ejecutando:
            try:
                # Esperar a que el STT deposite una transcripción
                texto_usuario = self.cola_transcripciones.get(timeout=0.5)
            except queue.Empty:
                continue
            
            # Interrumpir a Alex si el usuario vuelve a hablar
            self.tts.detener()
            
            print(f"🧠 Consultando a Qwen ({MODELO_IA})...")
            inicio_ia = time.perf_counter()
            texto_usuario =  "El usuario te estadiciendo lo siguiente, si es una pregunta respóndele: " + texto_usuario
            respuesta_ia = self.agente_llm.enviar_mensaje(texto_usuario, archivos=listar_imagenes_recientes())
            
            fin_ia = time.perf_counter()
            print(f"🤖 Alex: {respuesta_ia} [Tiempo: {fin_ia - inicio_ia:.2f}s]")
            
            # Enviar a Piper TTS
            self.tts.reproducir_texto(respuesta_ia)       
            self.cola_transcripciones.task_done()

    def iniciar_sistema(self):
        # 1. Precargar el LLM en la VRAM
        self.agente_llm.asegurar_modelo_activo()
        
        # 2. Lanzar los hilos del STT directamente
        t_grabar = threading.Thread(target=self.stt._hilo_grabacion, args=(0.013, 1.5))
        t_procesar = threading.Thread(target=self.stt._hilo_procesamiento, args=("es",))
        
        t_capturas = threading.Thread(target=generate_data, args=(self.modo,))
        
        # Marcamos todos como hilos daemon para que mueran si cerramos el programa principal
        t_grabar.daemon = True
        t_procesar.daemon = True
        t_capturas.daemon = True
        
        # Arrancamos los tres procesos paralelos
        t_grabar.start()
        t_procesar.start()
        t_capturas.start()
        print("📸 [DataCollector] Hilo asíncrono de capturas iniciado.")
        
        # 4. Ejecutar el orquestador principal en el hilo principal
        try:
            self.bucle_interaccion_principal()
        except KeyboardInterrupt:
            print("\n🛑 Apagando el controlador central...")
            self.ejecutando = False
            self.stt.ejecutando = False
            print("👋 Sistema cerrado correctamente.")

    def leer_configuracion(self, etiqueta="modo"):
        """
        Lee el archivo config.json de forma estricta. 
        Si el archivo no existe, está corrupto o no tiene la etiqueta, 
        el programa se caerá deteniendo la ejecución por completo.
        """
        ruta_config = "config.json"

        #Si el archivo no existe, lanzamos un error de archivo no encontrado
        if not os.path.exists(ruta_config):
            raise FileNotFoundError(f"❌ CRÍTICO: El archivo obligatorio de configuración '{ruta_config}' no existe.")

        #Intentamos abrir y parsear el JSON
        with open(ruta_config, "r", encoding="utf-8") as archivo:
            # Si el JSON está mal formateado, json.load() lanzará json.JSONDecodeError automáticamente y tirará el programa
            datos = json.load(archivo)
            
        # Validar si la etiqueta existe dentro del archivo
        if etiqueta not in datos:
            raise KeyError(f"❌ CRÍTICO: La etiqueta '{etiqueta}' es obligatoria en el archivo {ruta_config} pero no fue encontrada.")
        valor_encontrado = datos[etiqueta]
        
        #Validar que el modo sea uno de los dos permitidos estrictamente
        modos_validos = ["compania", "coach"]
        if valor_encontrado not in modos_validos:
            raise ValueError(
                f"❌ CRÍTICO: El modo '{valor_encontrado}' no es válido. Debe ser: {modos_validos}"
            )

        print(f"⚙️ [Config] Configuración cargada con éxito de forma estricta: {etiqueta} = '{valor_encontrado}'")
        return valor_encontrado

if __name__ == "__main__":
    controlador = ControladorJuegoIA()
    controlador.iniciar_sistema()