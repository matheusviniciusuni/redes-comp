import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "Desconectar"
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Indica que o "Servidor" vai usar os protocolos IPV4 (AF_INET) e o TCP (SOXK_STREAM)

clients = [] # Lista de "Clientes" que podem se conectar ao "Servidor"

try:
    server.bind(ADDR) # Vai tentar ligar o "Servidor", passando o seu endereço IP e em qual 'porta' receberá as conexões
    print('Servidor Iniciado...')
except:
    print('Servidor não foi inicializado.')

# Função que recebe a mensagem em forma de "byte" de um "Cliente" e a transmite aos outros "Clientes" conectados ao "Servidor"
def tratarCliente(client, addr):
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    conectado = True
    clients.append(client) # Adiciona um "Cliente" que se conectou ao "Servidor" na lista de clientes
    
    while conectado:
        try:
            tamanhoMensagem = client.recv(HEADER).decode(FORMAT)
            if tamanhoMensagem:
                tamanhoMensagem = int(tamanhoMensagem.strip())
                msg = client.recv(tamanhoMensagem).decode(FORMAT)
                
                if msg == DISCONNECT_MESSAGE:
                    conectado = False
                    print(f"[DESCONECTADO] {addr} foi desconectado.")
                    broadcast(f"[{addr}] desconectado.".encode(FORMAT), client)
                else:
                    print(f"[{addr}] {msg}")
                    broadcast(msg.encode(FORMAT), client)
        except:
            print(f'[ERRO] Cliente {addr} desconectado inesperadamente')
            conectado = False
 
    client.close()
    remove(client)
        
# Função que manda a mensagem de um "Cliente" aos outros que estão conectados ao "Servidor", e evita que a mensagem seja enviada para quem à enviou
def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client: # Verifica pela iteração feita da lista de clientes, se o "Cliente" que está mandando a mensagem é diferente do que recebe, caso seja ele envia
            try:
                clientItem.send(msg)
            except:
                clientItem.close()
                remove(clientItem)

# Função que serve para, caso o "Cliente" esteja desconectado do "Servidor", retire ele da lista de clientes
def remove(client):
    clients.remove(client)

# Função que inicia o "Servidor", permitindo a escutar "Clientes" que querem se conectar a ele
def start():
    server.listen() # Método para dizer que o "Servidor" está pronto para escutar/ouvir todas as conexões existentes
    print(f'O Servidor [{SERVER}] está escutando...')
    while True:
        client, addr = server.accept() # O "Servidor" aceita algum "Cliente" que requisita se conectar com ele, retornando o "Cliente" (objeto) e o seu "endereço" (addr)
        thread = threading.Thread(target=tratarCliente, args=[client, addr]) # Responsável por executar a função de tratar as mensagens e passar como argumento o "Cliente"
        thread.start()

start()