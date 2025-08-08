import socket
import sys
from Servidor import receber_dados, socket_comunicacao, enviar_dados, receber_dados

def inicializacao():
    while True:
        modo = input('Você gostaria de hospedar uma partida[h] ou se conectar a uma[c]? ')
        if modo.upper() == 'H' or modo.upper() == 'C':
            break
        else:
            print('Digite uma opção válida.')

    while True:
        protocolo = input('Qual procolo será utilizado? UDP ou TCP? ')
        if protocolo.upper() == 'TCP' or protocolo.upper() == 'UDP':
            break
        else:
            print('Digite uma opção válida.')

    while True:
        try:
            porta = int(input('Por qual porta você gostaria de acessar a conexão? '))
            if porta > 1024 or porta > 65535:
                break
            else:
                print('Porta incorreta. Experimento pôr alguma no intervalo entre 1024 e seis5535')
        except ValueError:
                print('Por favor, insira um valor inteiro.')

    host = input("Digite o endereço IP: ")
    
    return host, modo, porta, protocolo

def main():
    try:
        host, modo, porta, protocolo = inicializacao()

    except ValueError as e:
        print('Erro ao adicionar os valores, erro')
        sys.exit(1)

    sock = None
    conn = None
    jogador = ''
    endereco_op = None
    
    try:
        sock = socket_comunicacao(protocolo, host, porta)
        # Definindo o socket a partir da função que estabelece a comunicação entre os clientes

        if modo == 'H':
            jogador = 'Jogador 1'
            sock.bind(host, porta)
            # Associa um endereço ip a uma porta

            if protocolo == 'TCP':
                sock.listen()
                # Aqui o servidor está 'ouvindo', esperando alguém formar conexão

                conn, addr = sock.accept()
                # Ele aceita a requisição daquele endereço ip para a conexão

                comunicacao = conn
                # Aqui, o código está passando as informações contidas em
                # conn para uma nova variável e depois menciona-la novamente
                # em um momento posterior do código. Por ser uma conexão fixa, usamos o conn

            elif protocolo == 'UDP':
                print()
                iniciar, endereco_op = receber_dados(sock, 'UDP')
                # Em UDP, como não há conexão fixa, o hospedeiro é obrigado a
                # aguardar primeiro uma mensagem de quem está tentando se conectar
                # para assim observar qual o endereço desse host

                if iniciar and iniciar.get('cond') == 'iniciar':
                    print('Oponente conectado')
                    # A partir da função que foi adicionada na situação em que há o usuário
                    # é quem está se conectando, recebemos a confirmação de que o software
                    # pode ser iniciado, assim como recebemos o endereçço.

                else:
                    raise ConnectionAbortedError('Erro ao estabelecer conexão')
                
                comunicacao = sock
                # Em UDP, por ser um protocolo em que precisa é necessário a atualização
                # do endereço IP, sempre vai ser necessário estabelecer a conexão através do sock 

        elif modo == 'C':
            jogador = 'Jogador 2'
            endereco_op = (host, porta)
            # Define o endereço do oponente através do IP do hospedeiro(host) e da porta

            if protocolo == 'TCP':
                sock.connect(endereco_op)
                # Conecta o socket para o endereço IP do hospedeiro

                comunicacao = sock
                # Novamente define o comunicao e, como agora o usuário precisa do 
                # endereço IP do outro maluco, agora utilizamos do sock também

            elif protocolo == 'UDP':
                enviar_dados(sock,'UDP',{'cond' : 'iniciar'},endereco_op)
                # Esta parte será a que enviará a confirmação de conexão para o hospedeiro
                # a partir do cond:iniciar

                comunicacao = sock
                # A questão lá da comunicação que por precisar do IP é preciso o sock


        while True:


            vencedor = None
            turno_atual = 'Jogador 1'


    except Exception as e:
        print('Erro: '[e])

main()
