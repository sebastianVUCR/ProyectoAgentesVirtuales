import os
import subprocess
import threading
import sounddevice as sd
import soundfile as sf
from datetime import datetime
import time

TEST_STRING = """
    Hola, ¿cómo estás? Me alegra verte de nuevo. 
    Hoy hace un clima bastante agradable, aunque más temprano cayó una lluvia ligera. 
    Por cierto, ayer encontré una cafetería pequeña cerca del parque y el café sabía excelente.
    """

# =========================================================
# CLASE REPRODUCTOR TTS
# =========================================================

class ReproductorTTS:
    def __init__(self):
        # Configuración de rutas relativas para los ejecutables
        self.directorio_actual = os.path.dirname(os.path.abspath(__file__))
        
        self.piper_exe = os.path.normpath(os.path.join(
            self.directorio_actual, 
            "..", "..","..", "dependencies", "piper_windows_amd64", "piper", "piper.exe"
        ))
        
        self.model_path = os.path.join(self.directorio_actual, "es_ES-davefx-medium.onnx")
        
        # -------------------------------------------------------------
        # NUEVA CONFIGURACIÓN: Carpeta "audios" en el mismo directorio
        # -------------------------------------------------------------
        self.carpeta_temporales = os.path.join(self.directorio_actual, "audios")
        
        # Guardamos la ruta del archivo actual que se está operando
        self.archivo_actual = None
        
        # Variable para controlar el hilo de reproducción
        self.hilo_reproduccion = None

    def reproducir_texto(self, texto_input, detener_animacion=None):
        """Genera el audio con Piper en la carpeta 'audios' y lo reproduce en segundo plano."""
        self.detener()

        # Validaciones de archivos del sistema
        if not os.path.exists(self.piper_exe):
            print(f"Error: No se encontró el ejecutable de Piper en: {self.piper_exe}")
            return
        if not os.path.exists(self.model_path):
            print(f"Error: No se encontró el modelo de voz en: {self.model_path}")
            return
            
        # Asegurarse de que la carpeta "audios" exista, si no, la crea automáticamente
        if not os.path.exists(self.carpeta_temporales):
            os.makedirs(self.carpeta_temporales)

        print(f"\n[Piper] Generando audio...")
        
        # Generar nombre único basado en la fecha y hora: %Y-%m-%d_%H-%M-%S
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_archivo = f"audio_{timestamp}.wav"
        
        # Definimos la ruta completa apuntando a la carpeta de audios
        self.archivo_actual = os.path.join(self.carpeta_temporales, nombre_archivo)
        
        comando = [
            self.piper_exe,
            "--model", self.model_path,
            "--output_file", self.archivo_actual
        ]
        
        try:
            # Generar el archivo .wav único dentro de la carpeta /audios
            subprocess.run(
                comando, 
                input=texto_input.encode('utf-8'),
                capture_output=True,
                check=True
            )
            print(f"¡Audio generado con éxito! Guardado en: {self.archivo_actual}")
            
            # Leer el archivo generado
            data, fs = sf.read(self.archivo_actual)
            
            # Iniciamos la reproducción en un hilo separado
            self.hilo_reproduccion = threading.Thread(target=self._reproducir_async, args=(data, fs, self.archivo_actual, detener_animacion))
            self.hilo_reproduccion.daemon = True
            self.hilo_reproduccion.start()

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode('utf-8', errors='ignore')
            print(f"Error al ejecutar Piper:\n{error_msg}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al generar: {e}")

    def _reproducir_async(self, data, fs, ruta_archivo, detener_animacion=None):
        """Método interno que corre en el hilo secundario."""
        print("-> Reproduciendo audio... ")
        sd.play(data, fs)
        sd.wait()
        detener_animacion("idle")
        print("-> Reproducción finalizada por completo.")
        
        # Al terminar de reproducir de forma natural, borramos el archivo de la carpeta /audios
        self._eliminar_archivo_en_segundo_plano(ruta_archivo)

    def detener(self):
        """Detiene inmediatamente cualquier audio que se esté reproduciendo."""
        try:
            archivo_a_borrar = self.archivo_actual
            
            if sd.get_stream().active:
                sd.stop()
                print("[INFO] Audio interrumpido limpiamente.")
                # Al interrumpir, borramos el archivo de la carpeta /audios
                self._eliminar_archivo_en_segundo_plano(archivo_a_borrar)
            else:
                print("[INFO] No hay audio en reproducción para detener.")
        except RuntimeError:
            print("[INFO] El audio ya había finalizado o no se había iniciado.")

    def _eliminar_archivo_en_segundo_plano(self, ruta_archivo):
        """Crea un hilo aislado de fondo para borrar el archivo de la carpeta sin consumir recursos."""
        if ruta_archivo and os.path.exists(ruta_archivo):
            hilo_borrado = threading.Thread(target=self._borrar_audio_async, args=(ruta_archivo,))
            hilo_borrado.daemon = True
            hilo_borrado.start()

    def _borrar_audio_async(self, ruta_archivo):
        """Método asíncrono de fondo que se encarga de eliminar el archivo de la carpeta."""
        time.sleep(0.2)  # Pequeño tiempo de gracia para que Windows libere los recursos del archivo
        try:
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                print(f"[Sistema] Archivo eliminado de la carpeta audios: {os.path.basename(ruta_archivo)}")
        except Exception as e:
            print(f"[Error Sistema] No se pudo borrar el archivo de la carpeta audios: {e}")


# =========================================================
# EJEMPLO DE USO (MAIN)
# =========================================================

if __name__ == "__main__":
    tts = ReproductorTTS()
    tts.reproducir_texto(TEST_STRING)

    print("\n--- CONTROLES ---")
    print("Presiona ENTER en cualquier momento para DETENER el audio.")
    
    input()
    tts.detener()
    
    time.sleep(1)
    print("Script terminado.")