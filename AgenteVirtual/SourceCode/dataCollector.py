import os
import threading
from mss import mss
from PIL import Image
import time
from datetime import datetime
from pathlib import Path
import threading


def capturar_pantalla(nombre_archivo="captura.jpg", modo="compania"):
    carpeta_destino = "images"
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    ruta_final_archivo = os.path.join(carpeta_destino, nombre_archivo)

    sct = mss()
    try:
        monitor_principal = sct.monitors[1]
        captura_raw = sct.grab(monitor_principal)
        
        imagen = Image.frombytes("RGB", captura_raw.size, captura_raw.bgra, "raw", "BGRX")
        
        if modo == "coach":
            ancho_fijo = 672
            alto_fijo = 378
        else:
            ancho_fijo = 448
            alto_fijo = 252
    
        imagen = imagen.resize((ancho_fijo, alto_fijo), Image.Resampling.BILINEAR)
        
        imagen.save(ruta_final_archivo, "JPEG", quality=75)
        print(f"✅ Captura guardada exitosamente: {nombre_archivo}")
        
    except Exception as e:
        print(f"❌ Error en la captura: {e}")
    finally:
        sct.close() 

def limpiar_carpeta_images(ruta_carpeta="images"):
    """Elimina todas las imágenes .jpg de la carpeta especificada."""
    carpeta = Path(ruta_carpeta)
    if not carpeta.is_dir():
        return
        
    try:
        count = 0
        for archivo in carpeta.iterdir():
            if archivo.is_file() and archivo.suffix.lower() in [".jpg"]:
                archivo.unlink()
                count += 1
        if count > 0:
            print(f"🧹 [Limpieza Async] Se eliminaron {count} imágenes antiguas de '{ruta_carpeta}'.")
    except Exception as e:
        print(f"⚠️ No se pudo limpiar la carpeta de imágenes: {e}")


def generate_data(modo="compania"):

    while True:
        limpiar_carpeta_images()
        sleep_time = 20
        
        file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
        capturar_pantalla(nombre_archivo=file_name, modo=modo)
        time.sleep(sleep_time)
        
        
        file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
        capturar_pantalla(nombre_archivo=file_name, modo=modo)

        time.sleep(sleep_time)


# if __name__ == "__main__":
#     time.sleep(3) 
#     print("🚀 Probando mss con vaciado de caché estricto...")
#     generate_data()