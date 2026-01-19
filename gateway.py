from messaging import RPCServer, RPCClient, AsyncPublisher
import json
import threading

class Gateway:
    def __init__(self):
        self.rpc_client = RPCClient()
        self.rpc_client.connect()
        
        self.async_publisher = AsyncPublisher()
        self.async_publisher.connect()
        self.async_publisher.declare_queue("usuarios_async_queue")

    def handle_client_request(self, request):
        service = request.get("service")
        
        if service == "catalogo":
            return self.rpc_client.call("catalogo_queue", request)
        
        elif service == "playlists":
            return self.rpc_client.call("playlists_queue", request)
        
        elif service == "usuarios":
            if request.get("action") == "registrar_reproducao":
                def publish_async():
                    try:
                        self.async_publisher.publish("usuarios_async_queue", request)
                    except Exception as e:
                        print(f" [!] Erro ao publicar mensagem assíncrona: {e}")
                
                threading.Thread(target=publish_async, daemon=True).start()
                return {"status": "success", "message": "Reprodução registrada assincronamente"}
            
            return self.rpc_client.call("usuarios_queue", request)
        
        return {"status": "error", "message": "Serviço não encontrado"}

if __name__ == "__main__":
    gateway = Gateway()
    
    server = RPCServer(queue_name="gateway_queue", callback=gateway.handle_client_request)
    server.start()
