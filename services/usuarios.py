import sys
import os
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from messaging import RPCServer, AsyncConsumer
import json

USUARIOS = {
    "user1": {"nome": "Antonio", "email": "antonio@example.com"},
    "user2": {"nome": "Maria", "email": "maria@example.com"}
}

HISTORICO = {
    "user1": [],
    "user2": []
}

def handle_rpc_request(request):
    action = request.get("action")
    user_id = request.get("user_id")

    if action == "get_perfil":
        perfil = USUARIOS.get(user_id)
        if perfil:
            return {"status": "success", "data": perfil}
        return {"status": "error", "message": "Usuário não encontrado"}

    elif action == "get_historico":
        return {"status": "success", "data": HISTORICO.get(user_id, [])}

    return {"status": "error", "message": "Ação inválida"}

def handle_async_message(message):
    action = message.get("action")
    user_id = message.get("user_id")

    if action == "registrar_reproducao":
        musica = message.get("musica")
        if user_id in HISTORICO:
            HISTORICO[user_id].append(musica)
            print(f" [x] Histórico atualizado para {user_id}: {musica['titulo']}")
        else:
            print(f" [!] Usuário {user_id} não encontrado para registrar reprodução")

if __name__ == "__main__":
    rpc_server = RPCServer(queue_name="usuarios_queue", callback=handle_rpc_request)
    async_consumer = AsyncConsumer(queue_name="usuarios_async_queue", callback=handle_async_message)
    
    async_thread = threading.Thread(target=async_consumer.start, daemon=True)
    async_thread.start()
    
    print(" [x] Serviço de Usuários iniciado")
    print(" [x] RPC Server rodando em usuarios_queue")
    print(" [x] Async Consumer rodando em usuarios_async_queue")
    
    rpc_server.start()
