# Impacto del Rol del Agente Virtual en el Disfrute Percibido y la Interacción del Jugador: Compañero vs. Coach

## Descripción

Este proyecto consiste en el desarrollo y evaluación de un **agente virtual corporizado** que integra modelos de lenguaje extensos (**LLMs**) junto con tecnologías avanzadas de síntesis de voz (**TTS**) y reconocimiento de voz (**STT**). 

El objetivo principal es realizar un estudio comparativo entre dos roles de comportamiento distintos para el agente dentro del juego de estrategia *Infinitode 2*:
- **Compañero:** Orientado a la interacción social, la empatía y el humor.
- **Coach:** Orientado a la optimización de habilidades, el rendimiento y la entrega de consejos técnicos.

---

## Estructura del Proyecto

El repositorio está organizado en las siguientes carpetas y archivos principales:

```text
PROYECTOAGENTESVIRTUALES/
│
├── AgenteVirtual/
│   ├── SourceCode/
│   │   ├── images/
│   │   ├── Logs/
│   │   ├── Modelo/
│   │   │   ├── happy.mp4
│   │   │   ├── idle.mp4
│   │   │   ├── pantalla_negra.mp4
│   │   │   ├── talk.mp4
│   │   │   ├── video1.mkv
│   │   │   ├── wave.mp4
│   │   │   └── Model_manager.py
│   │   │
│   │   ├── Test/
│   │   │   └── AgenteVirtualMock.py
│   │   │
│   │   ├── TTS/
│   │   ├── AnimationManager.py
│   │   ├── AudioTest.py
│   │   ├── config.json
│   │   ├── dataCollector.py
│   │   ├── FasterWhisperIntegration.py
│   │   ├── MainController.py
│   │   └── QwenIntegration.py
│   │
│   ├── venv/
│   ├── emergency_environment_reset.bat
│   ├── instrucciones.txt
│   ├── requirements.txt
│   ├── setup_variables_de_ambiente.bat
│   └── setup.bat
│
├── Cuestionarios/
│   ├── public/
│   │   └── index.html
│   ├── venv/
│   └── parser.py
│
├── dependencies/
│   ├── piper_windows_amd64/
│   └── SteamSetup.exe
│
├── docs/
│   ├── Consentimiento informado.docx
│   ├── Entregable 2 avance para agente virtual e investigación.pdf
│   ├── Entregable 3 y final.pdf
│   ├── guion_protocolo.html
│   ├── Propuesta agentes virtuales inteligentes en videojuego.pdf
│   └── Sebastián Vargas Soto Diseño del Protocolo de Evaluación y ...
│
├── F/FrontEnd/
│   ├── .vs/
│   ├── Assets/
│   ├── Library/
│   ├── Logs/
│   ├── obj/
│   ├── Packages/
│   ├── ProjectSettings/
│   ├── UserSettings/
│   ├── .vsconfig
│   ├── Assembly-CSharp-Editor.csproj
│   ├── Assembly-CSharp.csproj
│   └── FrontEnd.sln
│
├── .gitignore
└── README.md
```

---

## Tecnologías Utilizadas (Stack Tecnológico)

El sistema se compone de las siguientes herramientas y versiones integradas:

* **Motor Gráfico:** `Unity 6.3`
    * Utilizado para dar vida al avatar 3D corporizado y garantizar un entorno interactivo fluido, aprovechando su alta compatibilidad con videojuegos y herramientas multimedia.
* **Lenguaje de Integración:** `Python 3.14`
    * Escogido como el núcleo de backend debido a su flexibilidad para conectar frameworks de Inteligencia Artificial y su facilidad de integración con el resto de componentes mediante un entorno virtual (`venv`).
* **Inteligencia Artificial (LLM):** `Ollama` con `Qwen2.5-VL 7B`
    * Encargado de procesar, razonar y estructurar las respuestas generadas por el agente virtual según el rol asignado. Se seleccionó esta familia de modelos por ser ligera, eficiente en ejecución local y contar con excelentes capacidades de visión artificial (procesamiento de imágenes y video).
* **Reconocimiento de Voz (STT):** `Faster Whisper (v1.2.1)`
    * Implementación optimizada de Whisper que otorga alta velocidad y precisión en la transcripción de voz a texto en tiempo real para el idioma español.
* **Síntesis de Voz (TTS):** `Piper (v1.2)`
    * Motor de texto a voz local de código abierto. Tras fases de pruebas empíricas, demostró una gran efectividad y velocidad de respuesta (baja latencia), con la capacidad de reproducir de manera óptima signos de expresión (interrogación y exclamación) en sus modelos de voz en español.
* **Entorno de Pruebas (Videojuego):** `Infinitode 2` (N/A)
    * Un juego de estrategia de defensa de torres (*tower defense*). Su diseño minimalista exige una carga cognitiva baja en los niveles iniciales pero retiene una alta profundidad técnica en árboles de habilidades. Esto permite evaluar con rigor científico el impacto de la asistencia del agente (Coach vs. Compañero) bajo escenarios controlados, comparando métricas reales frente a estudios previos con juegos de alta carga cognitiva.
* **Sistema Operativo Base:** `Windows 11`
    * Plataforma de desarrollo elegida por su compatibilidad nativa con el ecosistema de videojuegos, controladores de audio y soporte para la función de *Picture-in-Picture* (PiP) para superponer el agente virtual sobre el juego.

---


## Requisitos de Hardware


Para garantizar un rendimiento óptimo del sistema de interacción con el agente virtual, se recomiendan las siguientes especificaciones técnicas:

Memoria RAM: Se requiere un mínimo de 16 GB, aunque se recomienda contar con 24 GB para asegurar la estabilidad durante la ejecución simultánea del videojuego y los módulos de IA.

Tarjeta de video: Se recomienda una tarjeta gráfica con arquitectura moderna equivalente o superior a una NVIDIA GeForce RTX 4060, necesaria para el procesamiento gráfico del entorno y la aceleración de modelos de lenguaje.


## Enlace de videos de la tercera entrega

https://youtu.be/6WZDnkyOMSA

## Enlace de videos de la segunda entrega


https://www.youtube.com/watch?v=-GmoIPBeyEw

demo del modelo

https://youtu.be/7jKPCAtoC8Y


## Intruscciones de instalación

Instalar dependencias: ollama, steam, python e Inifitode 2

Ejecutar setup_variables_de_ambiente.bat en la carpeta AgenteVirtual si es necesario establecer la variables de ambiente de ollama y del manejo de memoria.

Si desea realizar la instalación automática entonces ejecute el archivo setup.bat en la carpeta AgenteVirtual, de los contrario ingrese a la carpeta AgenteVirtual y siga la siguientes instrucciones


```
python -m venv env

#activar ambiente virtual
.\env\Scripts\activate.bat

python.exe -m pip install --upgrade pip
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

cd .\SourceCode\
```

Abrir Infinitode 2 en la pantalla principal, ir a ajustes (opción con dibujo de engrane) y luego desactivar la pantalla completa y la música del juego.

```
python .\MainController.py 
```