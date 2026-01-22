echo "Iniciando Sistema de Streaming Distribuído..."
echo ""

if ! pgrep -x "rabbitmq-server" > /dev/null && ! pgrep -x "beam.smp" > /dev/null; then
    echo "RabbitMQ não está rodando!"
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Instalando dependências..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo ""

start_service() {
    local service_name=$1
    local command=$2
        
    gnome-terminal --title="$service_name" -- bash -c "source venv/bin/activate && $command; exec bash"
    
    sleep 1
}

start_service "Catálogo Service" "python services/catalogo.py"
start_service "Usuários Service" "python services/usuarios.py"
start_service "Playlists Service" "python services/playlists.py"

sleep 2

start_service "Gateway" "python gateway.py"

sleep 2

start_service "Cliente" "python client.py"
