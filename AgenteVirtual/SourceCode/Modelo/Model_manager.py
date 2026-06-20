import sys
import os
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton
)
# Importamos los componentes de video nativos de Qt
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget

os.environ["FFMPEG_LOG_LEVEL"] = "quiet"
os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.info=false;*.warning=false"

class Model_manager(QMainWindow):
    def __init__(self, video_inicial, video_alterno, callback_coach=None, callback_acompanante=None):
        super().__init__()
        self.setWindowTitle("Alex")
        
        # Guardar y convertir rutas a rutas absolutas del sistema para Qt
        self.video_actual = os.path.abspath(video_inicial)
        self.video_siguiente = os.path.abspath(video_alterno)

        # Forzar ventana siempre arriba
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        # Contenedor principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout vertical principal
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # =====================================================================
        # MOTOR DE VIDEO PROFESIONAL (HARDWARE ACCELERATED)
        # =====================================================================
        # 1. Creamos el widget donde se pintará el video (Usa la GPU del sistema)
        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("background-color: black;")
        self.main_layout.addWidget(self.video_widget)

        # 2. Creamos el reproductor multimedia y le asignamos el widget de salida
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)
        
        # Configurar bucle automático (Loop) nativo cuando el video termine
        self.player.loopsChanged.connect(lambda: self.player.setLoops(QMediaPlayer.Loops.Infinite))
        self.player.setLoops(QMediaPlayer.Loops.Infinite)

        # =====================================================================
        # INTERFAZ GRÁFICA Y BOTONERA (MISMA ESTRUCTURA SOLICITADA)
        # =====================================================================
        # Barra de controles inferior fija
        self.frame_barra_control = QWidget()
        self.frame_barra_control.setStyleSheet("background-color: #1e1e1e;")
        self.frame_barra_control.setFixedHeight(60)
        self.main_layout.addWidget(self.frame_barra_control)

        self.barra_layout = QHBoxLayout(self.frame_barra_control)
        self.barra_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.barra_layout.setContentsMargins(10, 0, 10, 0)

        # --- GRUPO DINÁMICO (IZQUIERDA - SE OCULTA) ---
        self.widget_acciones = QWidget()
        self.layout_acciones = QHBoxLayout(self.widget_acciones)
        self.layout_acciones.setContentsMargins(0, 0, 0, 0)
        self.layout_acciones.setSpacing(10)

        self.callback_coach_externo = callback_coach
        self.callback_acompanante_externo = callback_acompanante
        
        self.btn_acompanante = QPushButton("Acompañante")
        self.btn_acompanante.clicked.connect(self.accion_compania)


        self.btn_coach = QPushButton("Coach")
        self.btn_coach.clicked.connect(self.accion_coach)
        
        self.btn_cambiar = QPushButton("Reiniciar tiempo")
        self.btn_cambiar.clicked.connect(self.reiniciar_tiempo)
        
        self.layout_acciones.addWidget(self.btn_acompanante)
        self.layout_acciones.addWidget(self.btn_coach)
        self.layout_acciones.addWidget(self.btn_cambiar) 
        self.barra_layout.addWidget(self.widget_acciones)

        # Estilo de botones
        estilo_botones = "font-weight: bold; font-size: 14px; padding: 6px 15px;"
        self.btn_acompanante.setStyleSheet(estilo_botones)
        self.btn_coach.setStyleSheet(estilo_botones)
        self.btn_cambiar.setStyleSheet(estilo_botones)

        # --- GRUPO FIJO (DERECHA - NUNCA SE OCULTA) ---
        self.botones_visibles = True
        self.btn_toggle = QPushButton("👁")
        self.btn_toggle.setFixedWidth(40)
        self.btn_toggle.setStyleSheet("font-size: 14px; padding: 4px;")
        self.btn_toggle.clicked.connect(self.toggle_botones)
        self.barra_layout.addWidget(self.btn_toggle)

        # Temporizador Asíncrono Blanco
        self.tiempo_restante = 10 * 60
        self.lbl_timer = QLabel("10:00")
        self.lbl_timer.setStyleSheet("color: white; font-weight: bold; font-size: 16px; margin-left: 10px; margin-right: 10px;")
        self.barra_layout.addWidget(self.lbl_timer)

        # Reloj asíncrono secundario
        self.timer_reloj = QTimer()
        self.timer_reloj.timeout.connect(self.actualizar_temporizador)
        self.timer_reloj.start(1000)

        # Cargar e iniciar el primer video
        self.cargar_y_reproducir(self.video_actual)
        
        # Tamaño inicial estándar
        self.resize(1280, 780)

    def cargar_y_reproducir(self, ruta_video):
        """
        Carga el archivo de video en el motor nativo, validando el nombre
        y la ruta para capturar errores de formato o archivos faltantes.
        """
        print(f"\n[Media Engine] Intentando cargar la fuente: '{ruta_video}'")
        
        # 1. Validación: ¿La ruta está vacía o no es un string?
        if not ruta_video or not isinstance(ruta_video, str):
            print(f"❌ ERROR CRÍTICO: La ruta proporcionada no es un texto válido. Recibido: {type(ruta_video)} -> {ruta_video}")
            return
        
        # 2. Convertir a ruta absoluta para asegurar el rastreo en el disco
        ruta_absoluta = os.path.abspath(ruta_video)
        
        # 3. Validación: Comprobar si el archivo realmente existe en esa ruta
        if not os.path.exists(ruta_absoluta):
            print(f"❌ ERROR DE ARCHIVO: No se encuentra el video en el sistema.")
            print(f"   -> Ruta intentada: {ruta_absoluta}")
            print(f"   -> Carpeta de ejecución actual: {os.getcwd()}")
            
            # Rastreador de errores en el nombre/extensión:
            if not ruta_absoluta.lower().endswith('.mp4'):
                print(f"   💡 Sugerencia: El archivo no termina en '.mp4'. ¿Olvidaste incluir la extensión al llamarlo?")
            elif ruta_absoluta.count('.mp4') > 1:
                print(f"   💡 Sugerencia: Detectamos múltiples extensiones (.mp4.mp4). Revisa tu regex de animaciones.")
            return

        # Si el archivo existe, se envía directamente al reproductor
        print(f"✅ ÉXITO: Archivo localizado. Pasando al reproductor de hardware.")
        self.player.setSource(QUrl.fromLocalFile(ruta_absoluta))
        self.player.play()

    def toggle_botones(self):
        """Oculta o muestra los botones dinámicos de acción."""
        if self.botones_visibles:
            self.widget_acciones.hide()
            self.btn_toggle.setText("❌")
            self.botones_visibles = False
        else:
            self.widget_acciones.show()
            self.btn_toggle.setText("👁")
            self.botones_visibles = True

    def reiniciar_tiempo(self):
        """Intercambio instantáneo de fuente multimedia en la GPU."""
        """Reinicia el temporizador."""
        self.tiempo_restante = 10 * 60
        self.lbl_timer.setText("10:00")
        print("[Sistema] Coach reinició el temporizador.")
        
    
    def reproducir_animacion(self, animacion = "idle"):
        animacion = f"Modelo/{animacion}"
        animacion = f"{animacion}.mp4"
        self.cargar_y_reproducir(animacion)

    def accion_compania(self):
        """Reinicia el temporizador visual y notifica al controlador."""
        
        # Si el controlador nos pasó su método, lo ejecutamos aquí
        if self.callback_acompanante_externo:
            self.callback_acompanante_externo("compania")

    def accion_coach(self):
        """Reinicia el temporizador visual y notifica al controlador."""
        
        # Si el controlador nos pasó su método, lo ejecutamos aquí
        if self.callback_coach_externo:
            self.callback_coach_externo("coach")

    def actualizar_temporizador(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            minutos = self.tiempo_restante // 60
            segundos = self.tiempo_restante % 60
            self.lbl_timer.setText(f"{minutos:02d}:{segundos:02d}")
        else:
            self.lbl_timer.setText("00:00")


if __name__ == "__main__":
    # Necesitas instalar en terminal: pip install PyQt6 PyQt6-Multimedia
    app = QApplication(sys.argv)
    ex = Model_manager("idle.mp4")
    ex.show()
    sys.exit(app.exec())