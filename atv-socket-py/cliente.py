import socket
import threading # Biblioteca usada para gerenciar os "threads", que são processos que podem ser executados de forma simutânea

HEADER = 64
PORT = 5050
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "Desconectar"
SERVER = "" # "IP da do Servidor"

ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Indica que o "Cliente" vai usar os protocolos IPV4 (AF_INET) e o TCP (SOXK_STREAM)

try:
    client.connect(ADDR) # Vai tentar conectar o "Cliente" ao "Servidor", passando o endereço IP e em qual 'porta' o "Servidor" está recebendo as conexões
except:
    print('Conexão negada.')

username = input('Usuário: ')
print('Conectado.')

def receberMensagens(client):
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT) # Vai tentar receber as mensagens pelo "Servidor", e as mensagens recebidas em forma de "byte" serão transformadas em "String" pelo método ".decode()"
            if msg:
                print(msg)
            else:
                break
        except:
            print('\nUsuário foi desconectado do servidor.')
            print('Pressione <Enter> para continuar...')
            client.close()
            break

def enviarMensagens(client, username):
    while True:
        try:
            msg = input('Digite sua mensagem: ')
            mensagem = f'\n<{username}> enviou: {msg}\nDigite sua mensagem:'.encode(FORMAT) # Vai tentar transformar a mensagem do "Cliente" ao "Servidor" de "String" para "byte" pelo método ".encode()"
            tamanhoMensagem = len(mensagem)
            enviaMensagem = str(tamanhoMensagem).encode(FORMAT)
            enviaMensagem += b' ' * (HEADER - len(enviaMensagem))
            client.send(enviaMensagem)
            client.send(mensagem) # Vai tentar enviar a mensagem ao "Servidor"
            if msg == DISCONNECT_MESSAGE:
                client.send(DISCONNECT_MESSAGE.encode(FORMAT))
                print("Desconectado do servidor.")
                client.close()
                break
        except:
            print('\nMensagem não enviada.')
            client.close()
            break

#Criação dos threads, para que as funções de receber e mandar mensgaens funcionem simultaniamente
thread1 = threading.Thread(target=receberMensagens, args=[client]) # Parâmetro 'target' recebe a função que vai ser executada, e o parâmetro 'args' é o argumento(s) dentro de uma lista que a função recebe
thread2 = threading.Thread(target=enviarMensagens, args=[client, username])

# Inicializando as funções simultaniamente (1º iniciando a função de receber mensagens)
thread1.start()
thread2.start()