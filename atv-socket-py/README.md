# Atividade Chat Via Socket
- Disciplina: Redes de Computadores
- Prof.: Daniel Bezerra

# Integrantes
- Matheus Vinícius G. de Andrade
- Maria Cecília Sitcovsky
-------------------------------------------------------------

## Introdução
Projeto simples de comunicação entre usuários via "socket" por um servidor, executando funções simultaneamente através dos "threads".

### Servidor
Abaixo estará as configurações de um servidor que pode receber vários clientes e administrar a sua comunicação e troca de dados entre eles.

#### Cabeçalho
O cabeçalho é definido em 64 "bytes", representando o tamanho que cada mensagem precisa possuir ao ser enviada a um servidor.
#### Endereço Local IP
Para descobrir o endereço IP da sua máquina, digite no cmd `ipconfig` e no protocolo IPV4 é onde estará o seu IP, ou use o segundo script para obter automaticamente o seu IP.
~~~
SERVER = "127.0.0.1"
SERVER = socket.gethostbyname(socket.gethostname())
~~~
#### Outras Configurações
* ADDR serve para vincular o soquete, em forma de tupla, ao servidor que possuia informações dos protocolos IPV4(endereço IP da máquina) e porta de comunicação do servidor;
* Sempre ao enviar uma mensagem, ela precisa ser codificada em formato `UTF-8`, para que o usuário possa entender a mensagem;
* Definimos uma forma de como um cliente posssa se desconectar com o servidor de forma "amigável".
* Criamos uma lista de clientes, para que o servidor possa suportar vários clientes e administrar quem vai enviar a mensagem e recebe-lá.
~~~
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "Desconectar"
clients = []
~~~
#### Indicando a Conexão Específica
* Vinculamos ao servidor, um tipo específico de soquete, `SOCK_STREAM` (que indica oprotocolo TCP que será usado nas transmissões das mensagens);
* Colocamos a conexão do servidor em um bloco `try-catch`, para tratar uma exceção caso venha acontecer durante a inicialização do servidor.
~~~
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
    print('Servidor Iniciado...')
except:
    print('Servidor não foi inicializado.')
~~~
#### Conexão Cliente-Servidor
Função que lidará com as multiplas conexões dentro do servidor de forma simultânea, em sua própria "thread".
~~~
def tratarCliente(client, addr):
    //código aqui...
~~~
* Aqui, mostramos que uma nova conexão foi estabelecida no servidor e o endereço do cliente que se conectou;
* Ao conectar, dizemos que a conexão com o servidor é verdadeira e colocamos o cliente conectado na lista de clientes do servidor.
~~~
print(f"[NOVA CONEXÃO] {addr} conectado.")
conectado = True
clients.append(client)
~~~
* Enquanto a conexão é verdadeira, tentamos em um bloco `try-catch`, receber a primeira mensagem do cliente, passando o tamanho real dessa mensagem `HEADER`, nisso o código para sua execução até receber a mensagem, e depois decodifica a mensagem pelo formato informado `FORMAT`, transformando ela de "bytes" para "String".
~~~
tamanhoMensagem = client.recv(HEADER).decode(FORMAT)
~~~
* Aqui, conferimos se o "tamanhoMensagem"  não está vazio;
* Depois, convertemos o tamanho da mensagem em um número inteiro;
* Assim, recebe-se a mensagem real que o cliente enviou com base no tamanho especificado.
~~~
if tamanhoMensagem:
    tamanhoMensagem = int(tamanhoMensagem.strip())
    msg = client.recv(tamanhoMensagem).decode(FORMAT)
~~~
* Agora, temos uma condição que caso a mensagem do cliente seja "Desconectar", sua conxão seja cortada com o servidor, mudando a condição do "while" pela variável "conectar" para falso;
* E informamos aos outros clientes conectados lançando um broadcast para avisar que tal cliente foi desconectado.
~~~
if msg == DISCONNECT_MESSAGE:
    conectado = False
    print(f"[DESCONECTADO] {addr} foi desconectado.")
    broadcast(f"[{addr}] desconectado.".encode(FORMAT), client)
else:
    print(f"[{addr}] {msg}")
    broadcast(msg.encode(FORMAT), client)
~~~
* Após a condição do "while" for falso, seja por uma exceção encontrada ou pelo cliente se desconectando, fechamos a conexão do cliente depois do 'loop' e chamamos um método que retina o cliente da lista de clientes.
~~~
client.close()
remove(client)
~~~
#### Função para Mandar a Mensagem à Todos Conectados
Essa função faz com que a mensagem enviada por um cliente seja transmitida por todos os outros clientes conectados.
~~~
def broadcast(msg, client):
    for clientItem in clients:
~~~
E através de uma iteração dentro da lista de clientes, verificamos se a mensagem não será trasmitida ao cliente que à enviou.
~~~
if clientItem != client:
    try:
        clientItem.send(msg)
    except:
        clientItem.close()
        remove(clientItem)
~~~
#### Função que Remove o Cliente da Lista
Função que serve somente para retirar um cliente da lista de clientes do servidor, caso alguma condição necessite que tire-se um cliente, chamamos ela dentro de uma linha de código.
~~~
def remove(client):
    clients.remove(client)
~~~
#### Função para Iniciar o Servidor
A função "start" serve para darmos um inicío a função de "tratarCliente", de forma simultânea à outras funções existentes.
* Nessa função, serve para iniciarmos o servidor, primeiro deixando-o em modo de escuta, pronto para aceitar as conexões de clientes.
~~~
server.listen()
print(f'O Servidor [{SERVER}] está escutando...')
~~~
* E agora, enquando a condição for verdadeira, o servidor aceita algum cliente que deseja se conectar a ele, depois se cria uma "thread" para o servidor conseguir lidar com múltiplas conexões de clientes de forma simultânea e após isso, iniciamos uma nova "thread" para lidar com novos clientes a se conectar.
~~~
while True:
    client, addr = server.accept()
    thread = threading.Thread(target=tratarCliente, args=[client, addr])
    thread.start()
~~~

-------------------------------------------------------------
### Cliente
Aqui, mostraremos as configurações para um cliente se conectar a um servidor, receber mensagens e envia-las.

#### Configurações Iniciais
* Primeiro, definimos o IP do servidor em `SERVER`, indicando em qual máquina o cliente irá se conectar.
~~~
SERVER = "127.0.0.1"
~~~
* Depois, passamos o IP do servidor e a porta que ele poderá se conectar.
~~~
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
~~~
* Agora, em um bloco de exceções, tentamos conectar o cliente com o servidor passando as informaçoes de qual o endereço do servidor ele irá se conectar, caso dê certo, o cliente poderá informar o seu nome de usuário, para uma melhor identificação na comunicação com outros clientes.
~~~
try:
    client.connect(ADDR)
except:
    print('Conexão negada.')

username = input('Usuário: ')
print('Conectado.')
~~~
#### Função de Mandar Mensagem
* Enquanto o cliente estiver conectado ao servidor, dentro de um bloco de exceções, ele poderá mandar uma mensagem ao servidor, capturando ela e depois, transformando essa mensagem de "String" em "bytes", de forma que o servidor consiga entender a mensagem que está sendo enviada.
~~~
def enviarMensagens(client, username):
    while True:
        try:
            msg = input('Digite sua mensagem: ')
            mensagem = f'\n<{username}> enviou: {msg}\nDigite sua mensagem:'.encode(FORMAT)
            tamanhoMensagem = len(mensagem)
~~~
* Depois, informamos o tamanho da mensagem e preenchemos o cabeçalho com espaços, garantindo que ele tenha um comprimento definido pelo `HEADER`.
~~~
enviaMensagem = str(tamanhoMensagem).encode(FORMAT)
enviaMensagem += b' ' * (HEADER - len(enviaMensagem))
~~~
* Após essas operações, mandamos a mensagem do cliente ao servidor, primeiro o cabeça~ho e depois a mensagem real, e caso a mensagem do cliente seja "Desconectar", temosuma condiçãoque indica que o cliente fechou sua conexão com o servidor.
~~~         
client.send(enviaMensagem)
client.send(mensagem) # Vai tentar enviar a mensagem ao "Servidor"
if msg == DISCONNECT_MESSAGE:
    client.send(DISCONNECT_MESSAGE.encode(FORMAT))
    print("Desconectado do servidor.")
    client.close()
~~~
#### Função de Receber Mensagem
Quando um cliente qualquer envia uma mensagem, o servidor manda um broadcast aos outros clientes, que recebem essa mensagem.
* Enquanto o cliente estiver conectado, ele poderá receber mensagens, e ao recebe-lá, tentamos em um bloco `try-catch`, trasnformar a mensagem vinda do servidor em forma de byte, em String, e caso seja válida a mensagem, ela será imprimida.
~~~
def receberMensagens(client):
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)
            if msg:
                print(msg)
            else:
                break
~~~
### Configurações dos Threads
Agora, colocamos as funções de receber e enviar mensagens em "therads", para que elas funcionem de forma simultânea, quando o cliente se conecta a um servidor, permitindo o cliente de enviar e receber mensagens ao mesmo tempo.
~~~
thread1 = threading.Thread(target=receberMensagens, args=[client])
thread2 = threading.Thread(target=enviarMensagens, args=[client, username])

thread1.start()
thread2.start()
~~~
