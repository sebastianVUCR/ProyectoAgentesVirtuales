# Impacto del Rol del Agente Virtual en el Disfrute Percibido y la Interacción del Jugador: Compañero vs. Coach

## Descripción

Este proyecto consiste en el desarrollo y evaluación de un **agente virtual corporizado** que integra modelos de lenguaje extensos (**LLMs**) junto con tecnologías avanzadas de síntesis de voz (**TTS**) y reconocimiento de voz (**STT**). 

El objetivo principal es realizar un estudio comparativo entre dos roles de comportamiento distintos para el agente dentro del juego de estrategia *Infinitode 2*:
- **Compañero:** Orientado a la interacción social, la empatía y el humor.
- **Coach:** Orientado a la optimización de habilidades, el rendimiento y la entrega de consejos técnicos.

---

## Estructura del Proyecto

El repositorio está organizado en las siguientes carpetas y archivos principales:

| Carpeta / Archivo | Descripción |
| :--- | :--- |
| 📁 `SourceCode` | Contiene el código en **Python** encargado de la orquestación e integración de todas las herramientas (LLM, TTS, STT). |
| ├── 📁 `images` / `respaldo` | Capturas y recursos visuales del entorno y pruebas temporales. |
| ├── 📁 `TTS` | Módulos internos y cachés específicos para la generación de voz. |
| |   ├── 📄 `es_ES-davefx-medium.onnx` (.json) | Modelo y configuración de voz regional en español para Piper. |
| |   ├── 📄 | `PiperIntegration.py` Implementación y gestión del motor TTS (Piper). |
| ├── 📄 `AudioTest.py` | Script de pruebas unitarias para la entrada y salida de audio. |
| ├── 📄 `config.json` | Parámetros de configuración global del sistema y credenciales locales. |
| ├── 📄 `dataCollector.py` | Módulo encargado de la recolección de métricas de juego e interacción. |
| ├── 📄 `FasterWhisperIntegration.py` | Implementación y gestión del motor STT (Faster Whisper). |
| ├── 📄 `MainController.py` | Orquestador principal del ciclo de vida del agente y la comunicación. |
| ├── 📄 `QwenIntegration.py` | Integración local con los modelos de lenguaje mediante Ollama. |
| 📁 `FrontEnd` | Gestiona la interfaz y el flujo de comunicación directa con el usuario. |
| 📁 `AgenteVirtual` | Contiene el proyecto de **Unity**, incluyendo el modelo 3D del agente y el entorno virtual corporizado. |
| 📄 `instrucciones.txt` / `upgrades.txt` | Notas de desarrollo, guías de instalación rápida y control de mejoras. |
| 📄 `requirements.txt` | Lista de dependencias y librerías de Python requeridas para el entorno virtual (`venv`). |

---

## Tecnologías Utilizadas (Stack Tecnológico)

El sistema se compone de las siguientes herramientas y versiones integradas:

* **Motor Gráfico:** `Unity 6.3`
    * Utilizado para dar vida al avatar 3D corporizado y garantizar un entorno interactivo fluido, aprovechando su alta compatibilidad con videojuegos y herramientas multimedia.
* **Lenguaje de Integración:** `Python 3.14`
    * Escogido como el núcleo de backend debido a su flexibilidad para conectar frameworks de Inteligencia Artificial y su facilidad de integración con el resto de componentes mediante un entorno virtual (`venv`).
* **Inteligencia Artificial (LLM):** `Ollama` con `Qwen2.5-VL 7B` / `Qwen2.5-VL`
    * Encargado de procesar, razonar y estructurar las respuestas generadas por el agente virtual según el rol asignado. Se seleccionó esta familia de modelos por ser ligera, eficiente en ejecución local y contar con excelentes capacidades de visión artificial (procesamiento de imágenes y video).
* **Reconocimiento de Voz (STT):** `Faster Whisper (v1.2.1)`
    * Implementación optimizada de Whisper que otorga alta velocidad y precisión en la transcripción de voz a texto en tiempo real para el idioma español.
* **Síntesis de Voz (TTS):** `Piper (v1.2)`
    * Motor de texto a voz local de código abierto. Tras fases de pruebas empíricas, demostró una gran efectividad y velocidad de respuesta (baja latencia), con la capacidad de reproducir de manera óptima signos de expresión (interrogación y exclamación) en sus modelos de voz en español.
* **Entorno de Pruebas (Videojuego):** `Infinitode 2` (N/A)
    * Un juego de estrategia de defensa de torres (*tower defense*). Su diseño minimalista exige una carga cognitiva baja en los niveles iniciales pero retiene una alta profundidad técnica en árboles de habilidades. Esto permite evaluar con rigor científico el impacto de la asistencia del agente (Coach vs. Compañero) bajo escenarios controlados, comparando métricas reales frente a estudios previos con juegos de alta carga cognitiva.
* **Sistema Operativo Base:** `Windows 11`
    * Plataforma de desarrollo elegida por su compatibilidad nativa con el ecosistema de videojuegos, controladores de audio y soporte para la función de *Picture-in-Picture* (PiP) para superponer el agente virtual sobre el juego.