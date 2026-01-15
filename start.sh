echo "Iniciando Sistema de Streaming Distribuído..."
echo ""

if ! pgrep -x "rabbitmq-server" > /dev/null && ! pgrep -x "beam.smp" > /dev/null; then
    echo "AVISO: RabbitMQ não está rodando!"
    echo "   Execute: sudo systemctl start rabbitmq-server"
    echo "   Ou: sudo rabbitmq-server"
    echo ""
    read -p "Deseja continuar mesmo assim? (s/n) " -n 1 -r
    echo ""
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

echo "Ambiente virtual ativado"
echo ""

start_service() {
    local service_name=$1
    local command=$2
    
    echo "Iniciando $service_name..."
    
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal --title="$service_name" -- bash -c "source venv/bin/activate && $command; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -title "$service_name" -e "source venv/bin/activate && $command; bash" &
    elif command -v konsole &> /dev/null; then
        konsole --title "$service_name" -e bash -c "source venv/bin/activate && $command; exec bash" &
    else
        echo "Nenhum emulador de terminal encontrado!"
        echo "Execute manualmente: $command"
        return 1
    fi
    
    sleep 1
}

echo "Iniciando serviços distribuídos..."
echo ""

start_service "Catálogo Service" "python services/catalogo.py"
start_service "Usuários Service" "python services/usuarios.py"
start_service "Playlists Service" "python services/playlists.py"

echo "Aguardando serviços iniciarem..."
sleep 3

start_service "Gateway" "python gateway.py"

echo "Aguardando gateway iniciar..."
sleep 2

start_service "Cliente" "python client.py"

echo ""
echo "Todos os serviços foram iniciados!"
echo ""
echo "Use o terminal 'Cliente' para interagir com o sistema"
echo ""
