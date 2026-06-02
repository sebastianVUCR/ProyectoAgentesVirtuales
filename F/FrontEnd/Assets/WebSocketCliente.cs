using System;
using System.Collections.Concurrent;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

public class WebSocketClient : MonoBehaviour
{
    // Cambiado 'localhost' por '127.0.0.1' para emparejar perfectamente con Python
    private string serverUri = "ws://127.0.0.1:8999";
    private ClientWebSocket webSocket = null;
    private CancellationTokenSource cancellationTokenSource;

    // Cola segura para pasar datos del hilo del WebSocket al hilo de Unity
    private ConcurrentQueue<string> messageQueue = new ConcurrentQueue<string>();

    // Referencia al Animator de tu modelo
    private Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
        if (animator == null)
        {
            Debug.LogError("[WebSocketClient] ¡ERROR! No se encontró el componente Animator en este GameObject.");
        }

        cancellationTokenSource = new CancellationTokenSource();

        // Iniciar la conexión asíncrona
        StartConnection();
    }

    async void StartConnection()
    {
        webSocket = new ClientWebSocket();
        try
        {
            Debug.Log($"[WebSocketClient] Intentando conectar a {serverUri}...");
            await webSocket.ConnectAsync(new Uri(serverUri), cancellationTokenSource.Token);

            // Verificación estricta del estado
            if (webSocket.State == WebSocketState.Open)
            {
                Debug.Log("<color=green>[WebSocketClient] ¡CONECTADO EXITOSAMENTE al backend de Python!</color>");
                // Comenzar a escuchar mensajes
                _ = ReceiveMessages();
            }
            else
            {
                Debug.LogWarning($"[WebSocketClient] El socket terminó en un estado inesperado: {webSocket.State}");
            }
        }
        catch (Exception e)
        {
            Debug.LogError($"[WebSocketClient] Error de conexión: {e.Message}");
        }
    }

    async Task ReceiveMessages()
    {
        byte[] buffer = new byte[1024 * 4];

        try
        {
            while (webSocket.State == WebSocketState.Open && !cancellationTokenSource.Token.IsCancellationRequested)
            {
                var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), cancellationTokenSource.Token);

                if (result.MessageType == WebSocketMessageType.Close)
                {
                    Debug.LogWarning("[WebSocketClient] Conexión cerrada por el servidor de Python.");
                    await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Cerrando", cancellationTokenSource.Token);
                }
                else
                {
                    // Convertir bytes a string y encolar el mensaje
                    string message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                    messageQueue.Enqueue(message);
                }
            }
        }
        catch (Exception e)
        {
            // Solo muestra error si no fue una cancelación manual al detener el juego
            if (!cancellationTokenSource.Token.IsCancellationRequested)
            {
                Debug.LogError($"[WebSocketClient] Error en la recepción de datos: {e.Message}");
            }
        }
    }

    void Update()
    {
        // El Update corre en el hilo principal de Unity, aquí sí podemos mover el modelo
        while (messageQueue.TryDequeue(out string instruction))
        {
            ProcessInstruction(instruction);
        }
    }

    void ProcessInstruction(string instruction)
    {
        // Limpiamos espacios en blanco o saltos de línea invisibles que mande Python
        string cleanInstruction = instruction.Trim();
        Debug.Log($"[WebSocketClient] Instrucción recibida y procesada: '{cleanInstruction}'");

        if (animator == null) return;

        // Tus animaciones personalizadas
        switch (cleanInstruction)
        {
            case "Talk":
                Debug.Log("TRIGGER TALK");
                animator.ResetTrigger("TrIdle");
                animator.SetTrigger("TrTalk");
                break;

            case "Idle":
                Debug.Log("TRIGGER IDLE");
                animator.ResetTrigger("TrTalk");
                animator.SetTrigger("TrIdle");
                break;
        }
    }

    private async void OnDestroy()
    {
        if (webSocket != null)
        {
            cancellationTokenSource.Cancel();
            if (webSocket.State == WebSocketState.Open)
            {
                await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Cerrando aplicación", CancellationToken.None);
            }
            webSocket.Dispose();
            Debug.Log("[WebSocketClient] WebSocket liberado y cerrado limpiamente.");
        }
    }
}