import sys
import os
import requests

# Adiciona o diretório pai ao sys.path para permitir a importação de 'messaging'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from messaging import RPCServer
import json

DEEZER_API_BASE = "https://api.deezer.com"

def buscar_musicas_deezer(query, limit=15):
    """
    Busca músicas na API do Deezer
    
    Args:
        query: Termo de busca (artista, música, álbum)
        limit: Número máximo de resultados
    
    Returns:
        Lista de músicas formatadas para o sistema
    """
    try:
        response = requests.get(
            f"{DEEZER_API_BASE}/search",
            params={"q": query, "limit": limit},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        # Formata os dados no padrão do sistema
        musicas = []
        for track in data.get("data", []):
            musicas.append({
                "id": track["id"],
                "titulo": track["title"],
                "artista": track["artist"]["name"],
                "album": track["album"]["title"],
                "duracao": track["duration"],
                "preview_url": track.get("preview"),  # 30s de preview MP3
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
        # Usa o endpoint de charts para pegar os sucessos reais
        try:
            response = requests.get(f"{DEEZER_API_BASE}/chart/0/tracks", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            musicas = []
            # O endpoint de chart retorna uma lista em data['data'] ou data['tracks']['data']
            tracks = data.get("data", []) if "data" in data else data.get("tracks", {}).get("data", [])
            
            for track in tracks[:10]: # Limitando a 10 como o usuário pediu
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
