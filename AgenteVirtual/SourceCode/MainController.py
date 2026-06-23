import json
import time
import queue
import threading
import os
import re
from Modelo.Model_manager import Model_manager
import sys
from PyQt6.QtWidgets import QApplication

# IMPORTACIONES DE MIS MÓDULOS
from QwenIntegration import AgenteVirtual, MODELO_IA, CONTEXTO_AGENTE_COMPANIA, listar_imagenes_recientes
from FasterWhisperIntegration import WhisperSTTContinuo
from TTS.PiperIntegration import ReproductorTTS
from dataCollector import generate_data
from Test.AgenteVirtualMock import AgenteVirtualMock

ENABLE_OLLAMA_MODEL = True

class Main_controller:
    def __init__(self):
        print("🚀 Inicializando el sistema integrado de IA...")
        
        # 1. Crear la cola que usará el STT para enviarnos los textos detectados
        self.model_manager = None
        self.cola_transcripciones = queue.Queue()
        self.ejecutando = True
        self.modo = self.leer_configuracion(etiqueta="modo")

        # 2. Inicializar los componentes pasándole la cola al STT
        self.tts = ReproductorTTS()
        
        if ENABLE_OLLAMA_MODEL:
            self.agente_llm = AgenteVirtual(
                modelo=MODELO_IA,
                contexto=self.modo
            )
        else:
            self.agente_llm = AgenteVirtualMock()
        
        # Pasamos self.cola_transcripciones al inicializador
        self.stt = WhisperSTTContinuo(
            model_size="small", 
            device="cpu", 
            compute_type="int8",
            cola_salida_texto=self.cola_transcripciones 
        )

        self.default_prompt = "Describe lo que hay en todas imágenes."
    
    def procesar_animaciones(self, texto_respuesta: str) -> str:
        """
        Parsea las etiquetas de animación [wave] o [happy] al inicio del string.
        """
        patron_animacion = r"^\[(wave|happy)\]\s*"
        coincidencia = re.match(patron_animacion, texto_respuesta)
        
        if coincidencia:
            animacion_encontrada = coincidencia.group(1)
            print(f"¡Animación detectada y enviada al avatar!: {animacion_encontrada}")
            nombre_animacion = animacion_encontrada
            texto_limpio = re.sub(patron_animacion, "", texto_respuesta)
            return texto_limpio, nombre_animacion
        else:
            nomre_animacion = "talk"
        return texto_respuesta, nomre_animacion
    
    def solicitar_cambio_modo(self, modo):
        self.agente_llm.establecer_contexto(modo)

    def agregar_a_log(self, nombre_archivo, texto_a_agregar):
        try:
            with open(nombre_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(texto_a_agregar + "\n")
        except Exception as e:
            print(f"[Error] No se pudo escribir en el archivo: {e}")

    def bucle_interaccion_principal(self):
        """Maneja el flujo lógico de eventos de forma asíncrona en su propio hilo."""

        

        t_capturas = threading.Thread(target=generate_data, args=(self.modo,))
        t_capturas.daemon = True
        t_capturas.start()


        print("\n🤖 El Agente Alex está escuchando... (Presiona Ctrl+C en consola para salir)")



        self.model_manager.reproducir_animacion("idle")
        while self.ejecutando:
            try:
                # Esperar a que el STT deposite una transcripción
                texto_usuario = self.cola_transcripciones.get(timeout=0.5)
                self.agregar_a_log("Logs/logs.txt", f"Usuario: {texto_usuario}")
            except queue.Empty:
                continue
            
            # Interrumpir a Alex si el usuario vuelve a hablar
            self.tts.detener()
            
            print(f"🧠 Consultando a Qwen ({MODELO_IA})...")
            inicio_ia = time.perf_counter()
            texto_usuario = "El usuario te está diciendo lo siguiente, si es una pregunta respóndele: " + texto_usuario
            print(texto_usuario)
            
            respuesta_ia = self.agente_llm.enviar_mensaje(texto_usuario, archivos=listar_imagenes_recientes())
            
            fin_ia = time.perf_counter()
            print(f"🤖 Alex: {respuesta_ia} [Tiempo: {fin_ia - inicio_ia:.2f}s]")
            
            respuesta_ia, animacion_inicial = self.procesar_animaciones(respuesta_ia)

            
            # Enviar a Piper TTS
            self.tts.reproducir_texto(respuesta_ia, self.model_manager.reproducir_animacion, animacion_inicial)       
            
            self.cola_transcripciones.task_done()
            self.agregar_a_log("Logs/logs.txt", f"Alex: {respuesta_ia}")

    def iniciar_sistema(self):
        # 1. Crear la aplicación de Qt y la interfaz en el HILO PRINCIPAL
        app = QApplication(sys.argv)
        
        self.model_manager = Model_manager(
            "idle", 
            "pantalla_negra", 
            self.solicitar_cambio_modo, 
            self.solicitar_cambio_modo
        )
        self.model_manager.show()

        if ENABLE_OLLAMA_MODEL:
            try:
                self.agente_llm.asegurar_modelo_activo() # Tu limpieza del LLM
            except Exception as e:
                print(f"[Aviso] No se pudo iniciar el LLM: {e}")
        
        t_grabar = threading.Thread(target=self.stt._hilo_grabacion, args=(0.013, 1.5))
        t_procesar = threading.Thread(target=self.stt._hilo_procesamiento, args=("es",))
        t_grabar.daemon = True
        t_procesar.daemon = True
        t_grabar.start()
        t_procesar.start()

        t_interaccion = threading.Thread(target=self.bucle_interaccion_principal)        
        

        t_interaccion.daemon = True
        
        # Arrancamos todos los procesos paralelos
        
        t_interaccion.start()
        
        print("📸 [DataCollector] Hilo asíncrono de capturas iniciado.")
        print("🧠 [Interaction] Hilo de procesamiento de IA iniciado.")
        
        # 4. Ceder el hilo principal a PyQt6 y capturar el cierre de la ventana
        # Al presionar la X, app.exec() terminará su bucle y continuará con las líneas de abajo
        app.exec() 
        
        # --- CÓDIGO DE APAGADO SEGURO (Se ejecuta AL PRESIONAR LA X) ---
        print("\n🛑 Ventana cerrada. Apagando el controlador central y limpiando hilos...")
        self.ejecutando = False       # Rompe el while de tu hilo de interacción
        self.stt.ejecutando = False    # Rompe los whiles de FasterWhisper si los tiene
            
        print("👋 Sistema cerrado correctamente. ¡Adiós!")

    def leer_configuracion(self, etiqueta="modo"):
        ruta_config = "config.json"
        if not os.path.exists(ruta_config):
            raise FileNotFoundError(f"❌ CRÍTICO: El archivo obligatorio de configuración '{ruta_config}' no existe.")

        with open(ruta_config, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            
        if etiqueta not in datos:
            raise KeyError(f"❌ CRÍTICO: La etiqueta '{etiqueta}' es obligatoria en el archivo {ruta_config} pero no fue encontrada.")
        valor_encontrado = datos[etiqueta]
        
        modos_validos = ["compania", "coach"]
        if valor_encontrado not in modos_validos:
            raise ValueError(f"❌ CRÍTICO: El modo '{valor_encontrado}' no es válido. Debe ser: {modos_validos}")

        print(f"⚙️ [Config] Configuración cargada con éxito de forma estricta: {etiqueta} = '{valor_encontrado}'")
        return valor_encontrado

if __name__ == "__main__":
    controlador = Main_controller()
    controlador.iniciar_sistema()