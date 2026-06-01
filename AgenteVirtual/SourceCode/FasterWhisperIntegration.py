import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import tempfile
import threading
import queue
import time

class WhisperSTTContinuo:

    def __init__(self, model_size="small", device="cpu", compute_type="int8", cola_salida_texto=None):
        print("🧠 Cargando modelo Whisper...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print("✅ Modelo cargado correctamente")
        
        self.cola_audio = queue.Queue()
        # NUEVO: Guardamos la referencia a la cola del controlador central (opcional)
        self.cola_salida_texto = cola_salida_texto
        self.ejecutando = True

    # ========================================================
    # HILO 1: GRABACIÓN (Micrófono perpetuo, sin cierres)
    # ========================================================
    def _hilo_grabacion(self, umbral_silencio, segundos_silencio):
        fs = 16000
        bloque_duracion = 0.1
        bloque_muestras = int(fs * bloque_duracion)
        
        audio_acumulado = []
        silencio_acumulado = 0.0
        hablando = False
        
        print("\n🎤 [MICRÓFONO ABIERTO] Empieza a leer cuando gustes...")

        q_entrada = queue.Queue()
        def callback(indata, frames, time, status):
            q_entrada.put(indata.copy())

        with sd.InputStream(samplerate=fs, channels=1, dtype='float32', callback=callback, blocksize=bloque_muestras):
            while self.ejecutando:
                try:
                    bloque = q_entrada.get(timeout=0.5)
                except queue.Empty:
                    continue

                audio_acumulado.append(bloque)
                energia = np.sqrt(np.mean(bloque**2))
                
                if (energia > umbral_silencio):
                    if not hablando:
                        hablando = True
                    silencio_acumulado = 0.0
                else:
                    if hablando:
                        silencio_acumulado += bloque_duracion
                
                if hablando and silencio_acumulado >= segundos_silencio:
                    audio_enviar = np.concatenate(audio_acumulado, axis=0)
                    self.cola_audio.put(audio_enviar)
                    
                    audio_acumulado = []
                    silencio_acumulado = 0.0
                    hablando = False
                    
                if not hablando and len(audio_acumulado) > int(5 / bloque_duracion):
                    audio_acumulado = []

    # ========================================================
    # HILO 2: PROCESAMIENTO (Ahora integrado y limpio)
    # ========================================================
    def _hilo_procesamiento(self, language):
        fs = 16000
        while self.ejecutando:
            try:
                audio_completo = self.cola_audio.get(timeout=1)
            except queue.Empty:
                continue

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                path = f.name
                write(path, fs, audio_completo)

            # Transcribir usando parámetros de estabilidad
            segments, info = self.model.transcribe(
                path, 
                language=language,
                beam_size=5,
                vad_filter=True, 
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            texto = " ".join(segment.text for segment in segments).strip()

            if texto and len(texto) > 2:
                print(f"\n📝 [STT - Detectado]: {texto}")
                
                # Si tenemos una cola externa asignada, enviamos el texto ahí
                if self.cola_salida_texto is not None:
                    self.cola_salida_texto.put(texto)
                else:
                    print("-" * 50)
            
            self.cola_audio.task_done()

    def iniciar(self, language="es", umbral_silencio=0.013, segundos_silencio=2.0):
        t_grabar = threading.Thread(target=self._hilo_grabacion, args=(umbral_silencio, segundos_silencio))
        t_procesar = threading.Thread(target=self._hilo_procesamiento, args=(language,))
        
        t_grabar.start()
        t_procesar.start()
        
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n🛑 Apagando el sistema...")
            self.ejecutando = False
            t_grabar.join()
            t_procesar.join()

# if __name__ == "__main__":
#     # Si se ejecuta solo, funciona de manera autónoma como antes
#     stt = WhisperSTTContinuo(model_size="small", device="cpu", compute_type="int8")
#     stt.iniciar(
#         language="es", 
#         umbral_silencio=0.013,   
#         segundos_silencio=1.5    
#     )