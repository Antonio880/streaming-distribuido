from messaging import RPCClient
import time
import json

def mostrar_musicas(musicas):
    """Exibe lista de músicas formatada com metadados"""
    if not musicas:
        print("Nenhuma música encontrada.")
        return
    
    print(f"\n{'='*80}")
    for i, musica in enumerate(musicas, 1):
        print(f"\n{i}. {musica['titulo']}")
        print(f"   Artista: {musica['artista']}")
        print(f"   Álbum: {musica['album']}")
        
        if 'duracao' in musica:
            mins = musica['duracao'] // 60
            secs = musica['duracao'] % 60
            print(f"   Duração: {mins}:{secs:02d}")
        
        if 'preview_url' in musica and musica['preview_url']:
            print(f"   Preview: {musica['preview_url']}")
        
        if 'capa' in musica:
            print(f"   Capa: {musica['capa']}")
    
    print(f"\n{'='*80}")

def mostrar_menu():
    print("\n--- Streaming Distribuído ---")
    print("1. Listar Músicas (Top Tracks)")
    print("2. Pesquisar Música")
    print("3. Ver meu Perfil")
    print("4. Ver Playlists")
    print("5. Criar Playlist")
    print("6. Tocar Música (Async History)")
    print("7. Ver Histórico")
    print("8. Adicionar Música à Playlist")
    print("0. Sair")
    return input("Escolha uma opção: ")

def main():
    client = RPCClient()
    client.connect()
    
    user_id = "user1"
    ultima_busca = []

    while True:
        opcao = mostrar_menu()
        
        if opcao == "1":
            print("\n🎵 Buscando top tracks no Deezer...")
            resposta = client.call("gateway_queue", {"service": "catalogo", "action": "listar_musicas"})
            ultima_busca = resposta.get("data", [])
            mostrar_musicas(ultima_busca)
        
        elif opcao == "2":
            query = input("\n🔍 Digite o nome da música ou artista: ")
            print(f"\n🎵 Pesquisando '{query}' no Deezer...")
            resposta = client.call("gateway_queue", {"service": "catalogo", "action": "pesquisar", "query": query})
            ultima_busca = resposta.get("data", [])
            mostrar_musicas(ultima_busca)

        elif opcao == "3":
            resposta = client.call("gateway_queue", {"service": "usuarios", "action": "get_perfil", "user_id": user_id})
            print(resposta.get("data"))

        elif opcao == "4":
            resposta = client.call("gateway_queue", {"service": "playlists", "action": "listar_playlists", "user_id": user_id})
            playlists = resposta.get("data", [])
            if not playlists:
                print("\nVocê não tem playlists.")
            for pl in playlists:
                print(f"\nID: {pl['id']} - Nome: {pl['nome']}")
                for m in pl['musicas']:
                    print(f"   - {m['titulo']} ({m['artista']})")

        elif opcao == "5":
            nome = input("Nome da playlist: ")
            client.call("gateway_queue", {"service": "playlists", "action": "criar_playlist", "user_id": user_id, "nome": nome})
            print("Playlist criada!")

        elif opcao == "6":
            if not ultima_busca:
                print("\nPrimeiro pesquise ou liste músicas (opção 1 ou 2).")
                continue
            
            idx = int(input(f"Digite o número da música (1-{len(ultima_busca)}): ")) - 1
            if 0 <= idx < len(ultima_busca):
                musica = ultima_busca[idx]
                resposta = client.call("gateway_queue", {
                    "service": "usuarios", 
                    "action": "registrar_reproducao", 
                    "user_id": user_id,
                    "musica": musica
                })
                print(f"\n▶ Tocando agora: {musica['titulo']} - {musica['artista']}")
                print(resposta.get("message", ""))
            else:
                print("Índice inválido.")

        elif opcao == "7":
            resposta = client.call("gateway_queue", {"service": "usuarios", "action": "get_historico", "user_id": user_id})
            historico = resposta.get("data", [])
            if not historico:
                print("\n Seu histórico está vazio. Toque algumas músicas para começar!")
            else:
                print("\n Seu Histórico de Reprodução:")
                for musica in historico:
                    print(f"  ♪ {musica['titulo']} - {musica['artista']}")

        elif opcao == "8":
            if not ultima_busca:
                print("\nPrimeiro pesquise ou liste músicas (opção 1 ou 2) para escolher uma.")
                continue

            idx_m = int(input(f"Digite o número da música (1-{len(ultima_busca)}): ")) - 1
            if not (0 <= idx_m < len(ultima_busca)):
                print("Música inválida.")
                continue
            
            musica_escolhida = ultima_busca[idx_m]

            print("\nSua(s) Playlist(s):")
            resp_pl = client.call("gateway_queue", {"service": "playlists", "action": "listar_playlists", "user_id": user_id})
            playlists = resp_pl.get("data", [])
            if not playlists:
                print("Você não tem playlists. Crie uma primeiro (opção 5).")
                continue
            
            for pl in playlists:
                print(f"ID: {pl['id']} - {pl['nome']}")
            
            id_playlist = int(input("\nDigite o ID da playlist onde deseja adicionar: "))

            client.call("gateway_queue", {
                "service": "playlists",
                "action": "adicionar_musica",
                "user_id": user_id,
                "playlist_id": id_playlist,
                "musica": musica_escolhida
            })
            print(f"\n '{musica_escolhida['titulo']}' adicionada com sucesso!")

        elif opcao == "0":
            break
        
        else:
            print("Opção inválida.")

    client.close()

if __name__ == "__main__":
    main()

