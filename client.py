from messaging import RPCClient
import time
import json

def mostrar_menu():
    print("\n--- Streaming Distribuído ---")
    print("1. Listar Músicas")
    print("2. Pesquisar Música")
    print("3. Ver meu Perfil")
    print("4. Ver Playlists")
    print("5. Criar Playlist")
    print("6. Tocar Música (Async History)")
    print("7. Ver Histórico")
    print("0. Sair")
    return input("Escolha uma opção: ")

def main():
    client = RPCClient()
    client.connect()
    
    user_id = "user1"  # Simulado

    while True:
        opcao = mostrar_menu()
        
        if opcao == "1":
            resposta = client.call("gateway_queue", {"service": "catalogo", "action": "listar_musicas"})
            for musica in resposta.get("data", []):
                print(f"{musica['id']}: {musica['titulo']} - {musica['artista']}")
        
        elif opcao == "2":
            query = input("Digite o nome ou artista: ")
            resposta = client.call("gateway_queue", {"service": "catalogo", "action": "pesquisar", "query": query})
            for musica in resposta.get("data", []):
                print(f"{musica['id']}: {musica['titulo']} - {musica['artista']}")

        elif opcao == "3":
            resposta = client.call("gateway_queue", {"service": "usuarios", "action": "get_perfil", "user_id": user_id})
            print(resposta.get("data"))

        elif opcao == "4":
            resposta = client.call("gateway_queue", {"service": "playlists", "action": "listar_playlists", "user_id": user_id})
            for pl in resposta.get("data", []):
                print(f"{pl['id']}: {pl['nome']} ({len(pl['musicas'])} músicas)")

        elif opcao == "5":
            nome = input("Nome da playlist: ")
            client.call("gateway_queue", {"service": "playlists", "action": "criar_playlist", "user_id": user_id, "nome": nome})
            print("Playlist criada!")

        elif opcao == "6":
            # Primeiro pegamos a lista para o usuário ver
            id_musica = int(input("Digite o ID da música para tocar: "))
            # Buscando a música localmente na simulação para enviar o objeto (simplificado)
            # Em um sistema real, o ID seria enviado e o serviço buscaria.
            musica = {"id": id_musica, "titulo": f"Musica {id_musica}"} 
            resposta = client.call("gateway_queue", {
                "service": "usuarios", 
                "action": "registrar_reproducao", 
                "user_id": user_id,
                "musica": musica
            })
            print(resposta.get("message", "Tocando..."))

        elif opcao == "7":
            resposta = client.call("gateway_queue", {"service": "usuarios", "action": "get_historico", "user_id": user_id})
            for musica in resposta.get("data", []):
                print(f"Ovida: {musica['titulo']}")

        elif opcao == "0":
            break
        
        else:
            print("Opção inválida.")

    client.close()

if __name__ == "__main__":
    main()

