import sys
import os
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from messaging import RPCServer
import json

DEEZER_API_BASE = "https://api.deezer.com"

def buscar_musicas_deezer(query, limit=15):
    try:
        response = requests.get(
            f"{DEEZER_API_BASE}/search",
            params={"q": query, "limit": limit},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        musicas = []
        for track in data.get("data", []):
            musicas.append({
                "id": track["id"],
                "titulo": track["title"],
                "artista": track["artist"]["name"],
                "album": track["album"]["title"],
                "duracao": track["duration"],
                "preview_url": track.get("preview"),
                "capa": track["album"]["cover_medium"]
            })
        
        print(f" [x] Buscou '{query}' no Deezer: {len(musicas)} resultados")
        return musicas
        
    except requests.exceptions.RequestException as e:
        print(f" [!] Erro ao buscar no Deezer: {e}")
        return []
    except Exception as e:
        print(f" [!] Erro inesperado: {e}")
        return []

def handle_request(request):
    action = request.get("action")
    
    if action == "listar_musicas":
        try:
            response = requests.get(f"{DEEZER_API_BASE}/chart/0/tracks", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            musicas = []
            tracks = data.get("data", []) if "data" in data else data.get("tracks", {}).get("data", [])
            
            for track in tracks[:10]:
                musicas.append({
                    "id": track["id"],
                    "titulo": track["title"],
                    "artista": track["artist"]["name"],
                    "album": track["album"]["title"],
                    "duracao": track["duration"],
                    "preview_url": track.get("preview"),
                    "capa": track["album"]["cover_medium"]
                })
            return {"status": "success", "data": musicas}
        except Exception as e:
            print(f" [!] Erro ao buscar charts: {e}")
            return {"status": "error", "message": str(e)}
    
    elif action == "pesquisar":
        query = request.get("query", "")
        if not query:
            return {"status": "error", "message": "Query vazia"}
        
        musicas = buscar_musicas_deezer(query, limit=15)
        return {"status": "success", "data": musicas}
    
    return {"status": "error", "message": "Ação inválida"}

if __name__ == "__main__":
    server = RPCServer(queue_name="catalogo_queue", callback=handle_request)
    server.start()
