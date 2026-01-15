import sys
import os

# Adiciona o diretório pai ao sys.path para permitir a importação de 'messaging'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from messaging import RPCServer
import json

USUARIOS = {
    "user1": {"nome": "Antonio", "email": "antonio@example.com"},
    "user2": {"nome": "Maria", "email": "maria@example.com"}
}

HISTORICO = {
    "user1": [],
    "user2": []
}

def handle_request(request):
    action = request.get("action")
    user_id = request.get("user_id")

    if action == "get_perfil":
        perfil = USUARIOS.get(user_id)
        if perfil:
            return {"status": "success", "data": perfil}
        return {"status": "error", "message": "Usuário não encontrado"}

    elif action == "registrar_reproducao":
        musica = request.get("musica")
        if user_id in HISTORICO:
            HISTORICO[user_id].append(musica)
            print(f" [x] Histórico atualizado para {user_id}: {musica['titulo']}")
            return {"status": "success"}
        return {"status": "error", "message": "Usuário não encontrado"}

    elif action == "get_historico":
        return {"status": "success", "data": HISTORICO.get(user_id, [])}

    return {"status": "error", "message": "Ação inválida"}

if __name__ == "__main__":
    server = RPCServer(queue_name="usuarios_queue", callback=handle_request)
    server.start()
