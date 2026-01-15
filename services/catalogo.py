import sys
import os

# Adiciona o diretório pai ao sys.path para permitir a importação de 'messaging'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from messaging import RPCServer
import json

MUSICAS = [
    {"id": 1, "titulo": "Bohemian Rhapsody", "artista": "Queen", "album": "A Night at the Opera"},
    {"id": 2, "titulo": "Imagine", "artista": "John Lennon", "album": "Imagine"},
    {"id": 3, "titulo": "Hotel California", "artista": "Eagles", "album": "Hotel California"},
    {"id": 4, "titulo": "Smells Like Teen Spirit", "artista": "Nirvana", "album": "Nevermind"},
    {"id": 5, "titulo": "Billie Jean", "artista": "Michael Jackson", "album": "Thriller"},
]

def handle_request(request):
    action = request.get("action")
    
    if action == "listar_musicas":
        return {"status": "success", "data": MUSICAS}
    
    elif action == "pesquisar":
        query = request.get("query", "").lower()
        resultados = [m for m in MUSICAS if query in m["titulo"].lower() or query in m["artista"].lower()]
        return {"status": "success", "data": resultados}
    
    return {"status": "error", "message": "Ação inválida"}

if __name__ == "__main__":
    server = RPCServer(queue_name="catalogo_queue", callback=handle_request)
    server.start()
