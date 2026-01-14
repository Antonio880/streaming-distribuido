from messaging import RPCServer, RPCClient, AsyncPublisher
import json
import threading

class Gateway:
    def __init__(self):
        self.rpc_client = RPCClient()
        self.rpc_client.connect()
        
        self.async_publisher = AsyncPublisher()
        self.async_publisher.connect()

    def handle_client_request(self, request):
        service = request.get("service")
        
        # Rotear para o serviço apropriado via RPC
        if service == "catalogo":
            return self.rpc_client.call("catalogo_queue", request)
        
        elif service == "playlists":
            return self.rpc_client.call("playlists_queue", request)
        
        elif service == "usuarios":
            # Exemplo de coordenação: se a ação for registrar reprodução, podemos fazer de forma assíncrona
            if request.get("action") == "registrar_reproducao":
                self.async_publisher.publish("usuarios_queue", request)
                return {"status": "success", "message": "Reprodução registrada assincronamente"}
            
            return self.rpc_client.call("usuarios_queue", request)
        
        return {"status": "error", "message": "Serviço não encontrado"}

if __name__ == "__main__":
    gateway = Gateway()
    
    # O Gateway também atua como um servidor RPC para o cliente
    server = RPCServer(queue_name="gateway_queue", callback=gateway.handle_client_request)
    server.start()
