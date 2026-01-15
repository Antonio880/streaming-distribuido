# Sistema de Streaming Distribuído

Sistema de simulação de plataforma de streaming com arquitetura de microsserviços distribuídos em Python usando RabbitMQ como broker de mensagens.

### Componentes

- **Client** (`client.py`): Interface CLI para simular requisições de usuário
- **Gateway** (`gateway.py`): Middleware que roteia requisições para os serviços apropriados
- **Messaging** (`messaging.py`): Biblioteca de abstração para RPC e comunicação assíncrona via RabbitMQ
- **Serviços** (`services/`):
  - `catalogo.py`: Gerencia o catálogo de músicas
  - `playlists.py`: Gerencia playlists dos usuários
  - `usuarios.py`: Gerencia perfis e histórico de reprodução

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10+
- RabbitMQ rodando em `localhost:5672`

### Instalação Rápida

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#Aqui ele executa todos os serviços simultaneamente
chmod +x start.sh
./start.sh
```

### Execução Manual

Abra **5 terminais** separados e execute (com venv ativado):

```bash
python services/catalogo.py
python services/usuarios.py
python services/playlists.py
python gateway.py
python client.py
```

## 🔄 Conceitos de Sistemas Distribuídos Implementados

### 1. **RPC (Remote Procedure Call)**

Chamadas síncronas onde o cliente aguarda resposta.

**Exemplo**: Listar músicas do catálogo

```
Cliente → Gateway → catalogo_queue → Serviço Catálogo → Resposta
```

### 2. **Comunicação Assíncrona**

Operações que não bloqueiam o cliente.

**Exemplo**: Registrar histórico de reprodução

```python
self.async_publisher.publish("usuarios_queue", request)
return {"status": "success", "message": "Reprodução registrada assincronamente"}
```

### 3. **Comunicação Indireta (Broker)**

RabbitMQ medeia toda comunicação entre componentes.

**Filas utilizadas**:

- `gateway_queue`: Recebe requisições do cliente
- `catalogo_queue`: Processa consultas de músicas
- `playlists_queue`: Gerencia playlists
- `usuarios_queue`: Gerencia perfis e histórico

## 📦 Dependências

- `pika==1.3.2`: Cliente Python para RabbitMQ
