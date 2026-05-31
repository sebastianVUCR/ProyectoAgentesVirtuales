import time
import queue
import threading

# IMPORTACIONES DE TUS MÓDULOS
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

        # 2. Inicializar los componentes pasándole la cola al STT
        self.tts = ReproductorTTS()
        
        self.agente_llm = AgenteVirtual(
            modelo=MODELO_IA,
            contexto=CONTEXTO_AGENTE_COMPANIA
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
        
        # Correrá en segundo plano y guardará las imágenes cada 20 segundos de forma independiente
        t_capturas = threading.Thread(target=generate_data)
        
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
            self.agente_llm.cerrar_sesion()
            print("👋 Sistema cerrado correctamente.")

if __name__ == "__main__":
    controlador = ControladorJuegoIA()
    controlador.iniciar_sistema()