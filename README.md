# Sistema de Streaming Distribuído

Este é um projeto de simulação de uma plataforma de streaming utilizando uma arquitetura de serviços distribuídos em Python com RabbitMQ.

## Arquitetura

O sistema é composto por:

- **Gateway**: Middleware central que coordena as requisições entre o cliente e os serviços.
- **Serviços (Services/)**: Processos independentes para Catálogo, Playlists e Usuários/Histórico.
- **Messaging utility**: Abstração da biblioteca `pika` para facilitar RPC e chamadas assíncronas.
- **Client**: Simulador CLI para interação do usuário.

## Como Executar

### Pré-requisitos

- Python 3.10+
- RabbitMQ instalado e rodando (localhost:5672)

### Configuração do Ambiente

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Execução dos Componentes

Abra um terminal para cada comando abaixo (garanta que o `venv` esteja ativado):

1. **Catálogo**: `python services/catalogo.py`
2. **Usuários**: `python services/usuarios.py`
3. **Playlists**: `python services/playlists.py`
4. **Gateway**: `python gateway.py`
5. **Cliente**: `python client.py`

## Padrões de Comunicação Demonstrados

- **RPC (Remote Procedure Call)**: Utilizado em quase todas as consultas (ex: Listar músicas, ver perfil) onde o cliente espera uma resposta do serviço.
- **Comunicação Assíncrona**: O registro de histórico de reprodução é enviado de forma assíncrona pelo Gateway para o serviço de usuários, permitindo que o cliente continue sua experiência sem esperar a confirmação do log.
- **Comunicação Indireta**: O Broker (RabbitMQ) desacopla os serviços, permitindo que cada um rode em seu próprio processo.
