import sys
import os

# Adiciona o diretório pai ao sys.path para permitir a importação de 'messaging'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from messaging import RPCServer
import json

# Simulação de banco de dados de playlists
PLAYLISTS = {
    "user1": [
        {"id": 1, "nome": "Favoritas", "musicas": []}
    ],
    "user2": []
}

def handle_request(request):
    action = request.get("action")
    user_id = request.get("user_id")

    if action == "listar_playlists":
        return {"status": "success", "data": PLAYLISTS.get(user_id, [])}

    elif action == "criar_playlist":
        nome = request.get("nome")
        nova_playlist = {"id": len(PLAYLISTS.get(user_id, [])) + 1, "nome": nome, "musicas": []}
        if user_id not in PLAYLISTS:
            PLAYLISTS[user_id] = []
        PLAYLISTS[user_id].append(nova_playlist)
        return {"status": "success", "data": nova_playlist}

    elif action == "adicionar_musica":
        playlist_id = request.get("playlist_id")
        musica = request.get("musica")
        
        user_playlists = PLAYLISTS.get(user_id, [])
        for p in user_playlists:
            if p["id"] == playlist_id:
                p["musicas"].append(musica)
                return {"status": "success"}
        return {"status": "error", "message": "Playlist não encontrada"}

    return {"status": "error", "message": "Ação inválida"}

if __name__ == "__main__":
    server = RPCServer(queue_name="playlists_queue", callback=handle_request)
    server.start()
