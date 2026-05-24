\documentclass[11pt, letterpaper]{article}

% --- Paquetes de Idioma y Formato ---
\usepackage[spanish, es-tabla]{babel}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\geometry{margin=2.5cm}
\usepackage{authblk}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{enumitem}

% --- Configuración de Hipervínculos ---
\hypersetup{
    colorlinks=true,
    linkcolor=black,
    urlcolor=blue,
    citecolor=black
}

% --- Títulos y Autores ---
\title{\textbf{Impacto del Rol del Agente Virtual en el Disfrute Percibido y la Interacción del Jugador: Compañero vs Coach}}

\author{Sebastián Vargas Soto}
\affil{Programa de Posgrado en Computación e Informática, Universidad de Costa Rica}
\date{\small PF-3311 Temas Especiales de Ingeniería de Sistemas de Información: Agentes Virtuales Inteligentes \\ Prof. Alexander Barquero Elizondo \\ 4 de mayo de 2026}

\begin{document}

\maketitle

\section{Condiciones}

El experimento está compuesto por tres condiciones: un agente virtual en modo compañero, un agente virtual en modo coach y una condición base (control) sin agente. Todas las condiciones comparten un conjunto de elementos constantes, los cuales se describen a continuación:

\begin{itemize}[label=\textbullet, leftmargin=1.5cm]
    \item Videojuego \textit{Infinitode 2}.
    \item La misma dificultad del juego.
    \item El mismo tiempo de sesión.
    \item El mismo hardware o computadora.
    \item El mismo volumen de audio.
    \item Las mismas instrucciones iniciales.
    \item El mismo entorno físico de prueba.
\end{itemize}

\subsection*{Características generales compartidas por ambos agentes}

Las dos condiciones experimentales utilizan el mismo agente virtual inteligente corporizado, integrado como complemento del videojuego \textit{Infinitode 2}. Ambos agentes fueron desarrollados utilizando \textit{Unity} y \textit{Python}, e incorporan un modelo de lenguaje ejecutado localmente mediante \textit{Ollama} junto con tecnologías de reconocimiento y síntesis de voz (STT/TTS) para permitir una interacción conversacional en tiempo real con el jugador.

Ambos agentes comparten el mismo conocimiento contextual sobre el estado de la partida y pueden interpretar eventos relevantes del juego para responder de forma coherente. Debido a que el juego no requiere una gran carga cognitiva en comparación con otros géneros, ambos agentes se comunican con el jugador en momentos específicos: al inicio, tras la interacción del usuario y cuando el jugador no ha pausado el juego. Además, el usuario puede interrumpir al agente en cualquier momento, lo que detiene su intervención de forma inmediata.

Se establecieron dos objetivos diferenciados para cada tipo de agente debido a sus distintas formas de operación. Todas las condiciones mantienen las mismas características técnicas y visuales, así como la misma duración de sesión, videojuego, configuración experimental y modalidad de interacción por voz, variando únicamente el rol conductual del agente o su ausencia.

\subsection{Descripción de la apariencia física del agente}

El agente virtual contará con un nivel de \textit{embodiment} (corporización) estructurado a través de un modelo visual en 3D con apariencia humana. Técnicamente, el avatar integrará sistemas de \textit{blendshapes} y \textit{lipsync} para lograr que sus movimientos y gestos faciales ocurran de manera sincrónica con la voz generada por el sistema de síntesis de audio \textit{Kokoro}.

El diseño visual del agente se caracteriza por su apariencia neutral, lo que evita que el jugador se distraiga por un diseño extravagante durante el juego. La neutralidad del agente es ideal para utilizarse en ambas condiciones del experimento, ya que permite al personaje adaptarse de forma natural tanto al rol de un profesor o \textit{coach} que da instrucciones estratégicas, como al de un compañero cercano que brinda apoyo emocional.

\subsubsection{Lineamientos expresivos según la modalidad}

El diseño físico y expresivo del agente se modula de forma dinámica para cumplir con dos objetivos relacionales y psicológicos completamente distintos según la configuración del piloto:

\textbf{Modalidad de Acompañante (Compañero)}
\begin{itemize}[leftmargin=1cm]
    \item \textbf{Atributos transmitidos:} Cercanía, empatía, confianza y una profunda serenidad.
    \item \textbf{Expresividad:} El agente manifestará una personalidad alegre, amigable y emocionalmente expresiva. Utilizará sus gestos faciales y corporales para transmitir calidez de manera abierta. Sus movimientos buscarán ``contagiar'' emociones positivas durante la sesión de juego. El lenguaje no verbal respalda la interacción informal, relajada y casual (como la narración de chistes o anécdotas contextuales), emulando la sensación de estar jugando una partida compartida en tiempo real con un amigo.
\end{itemize}

\textbf{Modalidad de Coach} \\
En esta configuración, el avatar se transforma en una guía de asistencia estratégica orientada al aprendizaje progresivo y la optimización del desempeño técnico dentro de \textit{Infinitode 2}.
\begin{itemize}[leftmargin=1cm]
    \item \textbf{Atributos transmitidos:} Autoridad, seriedad constructiva y confiabilidad técnica.
    \item \textbf{Expresividad:} La neutralidad de su diseño visual se utiliza para proyectar un tono analítico y un carácter estructurado. Sus expresiones faciales transmiten la serenidad necesaria para no influir en el estado emocional del jugador de forma negativa durante la toma de decisiones.
\end{itemize}

\newpage

\subsection{Especificación de las Condiciones Experimentales}

\textbf{Condición experimental 1: agente compañero (Condición A1)} \\
\textbf{Descripción General:} Esta condición sitúa al participante en un entorno de juego asistido por un agente virtual enfocado en el soporte afectivo y la interacción social casual. Su propósito fundamental es mitigar la sensación de aislamiento y potenciar el disfrute percibido mediante el humor, la empatía y el acompañamiento conversacional continuo. \\
\textbf{Características Conductuales:} Realiza comentarios sobre acontecimientos recientes dentro del juego sin interrumpir momentos críticos. Aunque posee el mismo conocimiento del juego que el agente \textit{coach}, no ofrece consejos ni evaluaciones del desempeño. Su función principal es mantener una conversación fluida y natural, desviando el diálogo de forma contextual; por ejemplo, puede responder con chistes relacionados o anécdotas, priorizando la experiencia social y el entretenimiento. El agente adapta su comportamiento a la situación del juego para mantener una experiencia ligera y dinámica.

\vspace{0.3cm}
\textbf{Condición experimental 2: agente coach (Condición A2)} \\
\textbf{Descripción General:} Esta condición expone al jugador a un agente virtual configurado con un rol de mentoría técnica y analítica. Su objetivo principal es optimizar el desempeño del usuario dentro del videojuego, proveyendo asistencia estratégica accionable y reduciendo la tasa de frustración o deserción temprana en las etapas críticas del juego. \\
\textbf{Características Conductuales:} Se enfoca en la optimización del desempeño del jugador, ofreciendo recomendaciones únicamente al final de cada ola de enemigos, siempre que identifique áreas de mejora. Sus intervenciones se basan en patrones observados durante el juego y tienen un carácter más estructurado y analítico. A diferencia del agente compañero, el \textit{coach} mantiene un enfoque estratégico, con intervenciones menos frecuentes pero más orientadas a la retroalimentación directa y accionable. Su tono es neutral y su objetivo principal es apoyar el aprendizaje progresivo del jugador sin interferir durante la acción.

\vspace{0.3cm}
\textbf{Condición de control o baseline: sin agente virtual (Condición B)} \\
Esta condición representa el entorno tradicional y comercial del videojuego \textit{Infinitode 2} en su estado puro, carente de cualquier tipo de agente virtual o inteligencia artificial conversacional. En este escenario, un jugador se enfrenta de manera totalmente autónoma a las mecánicas clásicas de estrategia estilo defensa de torres (\textit{tower defense}) durante una sesión de 10 minutos. 

El usuario interactúa de forma directa y exclusiva con la interfaz nativa del software, encargándose manualmente de seleccionar las baldosas del mapa, construir y mejorar sus torres defensivas empleando los recursos de la partida, y gestionar el posicionamiento táctico para resistir las oleadas consecutivas de enemigos automatizados. Toda la experiencia se desenvuelve en absoluto aislamiento conversacional; no se dispone de un avatar gráfico en pantalla, cuadros de texto superpuestos ni estímulos de voz artificiales. El progreso de la partida, los aciertos tácticos y la tolerancia a la frustración ante el aumento progresivo de la dificultad dependen únicamente de las destrezas motrices, la atención y la capacidad de toma de decisiones del propio participante. Esta configuración permite registrar una línea base del comportamiento, disfrute e inmersión habitual del usuario sin elementos externos de asistencia.

\subsection{Justificación Metodológica de la Comparación}

La comparación entre las tres condiciones permite aislar el impacto específico del rol conductual del agente virtual sobre la experiencia del jugador. Las condiciones de agente compañero y agente \textit{coach} comparten las mismas características técnicas y visuales, lo que permite controlar variables relacionadas con la corporización, el uso de inteligencia artificial y la comunicación mediante voz. Las diferencias observadas entre ambas condiciones podrán atribuirse principalmente al tipo de comportamiento e interacción ofrecida por el agente. 

Por otra parte, la inclusión de una condición \textit{baseline} sin agente virtual permite determinar si la presencia de un agente inteligente produce cambios significativos en métricas como inmersión, disfrute, \textit{engagement} o percepción emocional en comparación con una experiencia de juego tradicional sin acompañamiento virtual.

\section{Matriz de Consistencia Metodológica}

\noindent\textbf{RQ1:} ¿Existe una diferencia significativa en las dimensiones de experiencia de juego medidas mediante el GEQ entre las condiciones de juego sin agente virtual, con un agente virtual configurado como compañero y con un agente virtual configurado como tutor de destrezas?

\begin{table}[h]
\centering
\begin{tabular}{|l|p{3.5cm}|p{3.5cm}|p{3.5cm}|}
\hline
\textbf{Elemento} & \textbf{Condición base} & \textbf{Compañero} & \textbf{Coach} \\ \hline
Variables & Experiencia de juego & Experiencia de juego & Experiencia de juego \\ \hline
Instrumento & GEQ & GEQ & GEQ \\ \hline
Tarea asociada & Jugar sin agente & Jugar con agente compañero & Jugar con agente coach \\ \hline
\end{tabular}
\caption{RQ1: Comparación de experiencia de juego entre condiciones}
\label{tab:rq1}
\end{table}

\vspace{0.5cm}
\noindent\textbf{RQ2:} ¿Existe diferencia significativa en la dimensión Inmersión del IEQ entre la condición Coach y la condición de Compañero en el piloto?

\begin{table}[h]
\centering
\begin{tabular}{|l|p{3.5cm}|p{3.5cm}|p{3.5cm}|}
\hline
\textbf{Elemento} & \textbf{Condición base} & \textbf{Compañero} & \textbf{Coach} \\ \hline
Variables & Inmersión & Inmersión & Inmersión \\ \hline
Instrumento & IEQ & IEQ & IEQ \\ \hline
Tarea asociada & Jugar sin agente & Jugar con agente compañero & Jugar con agente coach \\ \hline
\end{tabular}
\caption{RQ2: Comparación de inmersión entre condiciones}
\label{tab:rq2}
\end{table}

\section{Justificación Teórica en HCI}
La presente propuesta define un agente virtual inteligente diseñado como un complemento innovador para el entorno de juego, con el objetivo de elevar el nivel de disfrute y satisfacción del jugador a través de una interacción más inmersiva.

Una de las preocupaciones más grandes al realizar este estudio es la carga cognitiva que podría agregar el agente virtual inteligente y el videojuego; sin embargo, hay estudios que determinaron que muchos jugadores realizan \textit{multitasking} de todas formas (Rideout, 2010). Si bien el estudio encontrado es antiguo, la tendencia parece mantenerse o incluso haber aumentado de acuerdo con estudios más recientes pero de fuentes más informales.

Se busca que el agente sea capaz de transmitir emociones de alegría y que sea percibido como amigable en un contexto casual. Esta decisión se fundamenta en el estudio de Nick Yee y Jeremy Bailenson, quienes determinaron que la apariencia y representación de un agente virtual influyen en la forma en la que el usuario interactúa con él (Yee \& Bailenson, 2007). En este caso, se espera que la representación del agente influya en la percepción del usuario sobre la interacción, generando una sensación de mayor cercanía o naturalidad dependiendo de sus características visuales y conductuales.

Bajo el Efecto Proteus, esta percepción puede reflejarse en cambios en el comportamiento del usuario durante el uso del agente (Yee \& Bailenson, 2007). Por ejemplo, cuando el agente es percibido como amigable y expresivo, el participante puede adoptar un estilo de interacción más abierto, respondiendo de manera más espontánea o aumentando la comunicación verbal con el sistema durante el juego. En contraste, una representación más neutra del agente podría llevar a interacciones más breves y funcionales, centradas únicamente en la ejecución de la tarea dentro del juego.

El agente se asemejará más a un humano ya que en la investigación realizada por Lin se obtuvo la conclusión de que se debían realizar mejoras en el agente virtual para que se transmitieran mejor las emociones y se utilizó un robot (Lin, 2024). Además, en la investigación realizada por Ruiz, si bien no era el propósito principal de la investigación, se obtuvieron mejores resultados en la percepción de las emociones cuando el agente se parecía más a los humanos (Ruiz et al., 2023).

La propuesta del agente también toma en consideración los principios de diseño emocional en videojuegos descritos por Katherine Isbister, quien explica que muchos de los videojuegos más exitosos son experiencias compartidas entre amigos y que los videojuegos son capaces de generar respuestas emocionales significativas en los jugadores. La autora también destaca que el cuerpo y las expresiones físicas cumplen un papel importante en la transmisión de emociones durante la interacción, lo cual respalda el uso de un agente corporizado capaz de comunicar emociones mediante gestos, expresiones y comportamiento visual. Emociones como el entusiasmo, la emoción y la alegría pueden ser contagiosas durante actividades sociales (Isbister, 2016). A partir del principio de contagio de emociones, se busca que el agente virtual mantenga una personalidad amigable, alegre y emocionalmente expresiva para intentar contagiar al jugador de emociones positivas durante la sesión de juego y fomentar una experiencia más inmersiva y agradable.

Se usará un agente corporizado debido a que, según la investigación realizada por Gallaher, un agente corporizado ayuda a que la intensidad de las expresiones del agente se perciba mejor por los usuarios (Gallaher et al., 2009). Además, se consultó la investigación de Justine Cassell sobre agentes conversacionales corporizados, la cual respalda el uso de agentes con representación visual y comportamiento no verbal, ya que estos permiten mejorar la comunicación con el usuario mediante elementos como gestos, expresiones faciales, postura y sincronización conversacional, factores importantes para transmitir intención, emociones y naturalidad en la interacción (Cassell, 2000). Se mantiene la opción abierta para investigaciones futuras del uso de un agente virtual inteligente parcialmente corporizado porque se cree que la persona podría sentirse más identificada con ese tipo de agente, ya que se asemeja más a estar hablando con una persona por videollamada, lo cual es un escenario más común al jugar videojuegos.

La aplicación utilizará TTS/STT para ayudar a reducir la carga cognitiva en comparación a la comunicación por medio de texto; diversos estudios han demostrado una comunicación más natural y más efectiva por este medio (Guo et al., 2021). Si bien una herramienta de TTS/STT mejora la comunicación, se ha comprobado que participar en una conversación durante una sesión de videojuegos aumenta la carga cognitiva (Donohue et al., 2012), por lo que se establece que el público meta final son usuarios que frecuentemente juegan videojuegos, ya que el tiempo de respuesta de esta población disminuye menos que el resto cuando realizan las dos tareas al mismo tiempo.

\section*{Bibliografía}
\begin{enumerate}[leftmargin=*]
    \item IJsselsteijn, W. A., de Kort, Y. A. W., \& Poels, K. (2013). The Game Experience Questionnaire. Eindhoven University of Technology.
    \item Ruiz, J., \& colaboradores (2023). Acceptance of Assistants. Ruiz Lab.
    \item Lin, H. (2024). Analysis of the influence of artificial intelligence technology on the immersion of game players. ResearchGate.
    \item Gallaher, S., \& colaboradores (2009). Studies on gesture expressivity for a virtual agent. ResearchGate.
    \item Guo, H., Zhang, S., Soong, F. K., He, L., \& Xie, L. (2021). Conversational End-to-End TTS for Voice Agents. IEEE SLT.
    \item Donohue, S. E., James, B., Eslick, A. N., \& Mitroff, S. R. (2012). Cognitive pitfall! Videogame players are not immune to dual-task costs. Attention, Perception, \& Psychophysics.
    \item Rideout, V. (2010). Media Multitasking Among American Youth. Kaiser Family Foundation.
    \item Cassell, J., Sullivan, J., Prevost, S., \& Churchill, E. (Eds.). (2000). Embodied conversational agents. MIT Press.
    \item Yee, N., \& Bailenson, J. (2007). The Proteus effect: The effect of transformed self-representation on behavior. Human Communication Research, 33(3), 271–290. https://doi.org/10.1111/j.1468-2958.2007.00299.x
    \item Isbister, K. (2016). How games move us: Emotion by design. MIT Press.
    \item Jennett, C., Cox, A. L., Cairns, P., Dhoparee, S., Epps, A., Tijs, T., \& Walton, A. (2008). Measuring and defining the experience of immersion in games. International Journal of Human-Computer Studies, 66(9), 641–661.
\end{enumerate}

\end{document}
