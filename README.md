# Sistema de Streaming Distribuído

Plataforma de streaming musical distribuída com comunicação via RabbitMQ, implementando padrões RPC e mensageria assíncrona.

## Arquitetura

Sistema baseado em **microsserviços** com comunicação **indireta via broker (RabbitMQ)**:

```
Cliente → Gateway → RabbitMQ → Serviços (Catálogo, Playlists, Usuários)
```

**Componentes:**
- **Client**: Interface CLI simulando ações do usuário
- **Gateway**: Middleware centralizador e roteador de requisições
- **Messaging**: Abstração para RPC síncrono e publicação assíncrona
- **Serviços independentes**: Catálogo (API Deezer), Playlists, Usuários/Histórico

## Dependências

- **Python 3.10+**
- **RabbitMQ** (localhost:5672)
- **pika** 1.3.2 - Cliente RabbitMQ
- **requests** - Integração API Deezer

## Execução

```bash
pip install -r requirements.txt

docker run -d -p 5672:5672 rabbitmq

chmod +x start.sh && ./start.sh
```

**Execução manual** (5 terminais):
```bash
python services/catalogo.py
python services/usuarios.py
python services/playlists.py
python gateway.py
python client.py
```

## Conceitos de Sistemas Distribuídos Implementados

### 1.Fluxo do Sistema

**1. Pesquisar Música (RPC Síncrono):**
```
Cliente --[pesquisa "Morada"]-->
  Gateway --[rpc_call]--> 
    catalogo_queue --> Serviço Catálogo --> API Deezer
      <--[15 músicas]--
    <--[resposta]--
  <--[JSON]--
Cliente [exibe lista]
```

**2. Tocar Música (Pub/Sub Assíncrono):**
```
Cliente --[registrar_reproducao]-->
  Gateway --[publish async]--> 
    usuarios_async_queue --> Serviço Usuários [atualiza histórico]
  <--[confirmação imediata]--
```

**Filas RabbitMQ:** `gateway_queue`, `catalogo_queue`, `playlists_queue`, `usuarios_queue`, `usuarios_async_queue`

## Exemplos de Saída

**Pesquisar música:**
```
Digite o nome da música ou artista: Brunão Morada
Pesquisando 'Brunão Morada' no Deezer...

1. Ele é
   Artista: Morada
   Álbum: Ele é
   Duração: 5:54
   🎵 Preview: https://...
```

**Ver playlists:**
```
ID: 1 - Nome: Favoritas
   - So tu és santo - Morada
   - Ele é - Morada
```