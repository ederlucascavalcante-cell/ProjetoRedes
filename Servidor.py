import socket
import json
import ipaddress

def TipoIp(host):
    try:
        ip = ipaddress.ip_address(host)
        # Coleta e analisa o endereço ip

        if isinstance(ip, ipaddress.IPv4Address):
            # Esse comando verifica se o primeiro parâmetro é pertecente
            # ao tipo do segundo parâmetro, isto é, se ip é pertence a IPv4
            
            return socket.AF_INET
            # Retorna que o tipo de IP é IPv4

        elif isinstance(ip, ipaddress.IPv6Address):
             # Esse comando verifica se o primeiro parâmetro é pertecente
            # ao tipo do segundo parâmetro, isto é, se ip é pertence a IPv4

            return socket.AF_INET6
            # Retorna que o tipo de IP é IPv6

    except ValueError:
        raise ValueError("Endereço IP inválido ")
    

def socket_comunicacao(protocolo, host, porta):
    family = TipoIp(host)
    # Family é o valor que referencia se o host é IPv4 ou IPv6


    if protocolo.upper() == 'TCP':
        tipo_socket = socket.SOCK_STREAM
        # Tipo de socket baseando-se no protocolo utilizado,
        # Em tcp, a entrega é confiável e ordenada

    elif protocolo.upper() == 'UDP':
        tipo_socket = socket.SOCK_DGRAM
        # Em udp, a entrega é mais rápida, mas menos confiável
        # Não garante a entrega correta de dados


    sock = socket.socket(family, tipo_socket)
    # Criamos o socket e atríbuimos a ele a familía do 
    # ip e tipo de protocolo usado nesse socket

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Coletânea de comandos que permite que alguma porta seja reutilizada, 
    # sem o chamado tempo de espera entre a ligação a uma porta e outra tentativa de ligação

    return sock


def enviar_dados(sock, protocolo, dados, ip_address=None):
    enviadao = json.dumps(dados).encode('utf-8')
    # Variável e comandos que serão responsáveis por converter algo em dicionário
    #  Python, isto é, dados semelhante a "'status':'iniciar' e transformar
    #  em uma string json, transformar em bits e assim poder enviar por um socket

    try:
        if protocolo.upper() == 'TCP':
            sock.sendall(enviadao)
            # Garante que todas as partes do pacotes sejam enviados 
            # evitando quaisquer fragmentações do pacote de dados
        else:
            sock.sendto(enviadao, ip_address)
            # O comando que usamos é sendto para garantir que o pacote 
            # seja enviado sempre para aquele endereço ip especificado

    except socket.error as e:
        print('Erro ao enviar o socket:', e)
        return False
    
    return True


def receber_dados(sock, protocolo, buffer_size = 1024):
    
    try:
        if protocolo.upper() == 'TCP':
            enviadao = sock.recv(buffer_size)
            if not enviadao:
                return None, None
            endereço_op = None

        elif protocolo.upper() == 'UDP':
            enviadao, endereço_op = sock.recvfrom(buffer_size)
        
        dados = json.loads(enviadao.decode('utf-8'))
        # Única coisa que faz vai ser basicamente decodificar 
        # o pacote de dados que enviei anteriormente com o enviadao
        
        return dados, endereço_op


    except (socket.error, json.JSONDecodeError, ConnectionAbortedError) as e:
        print('Erro ao receber dados')
        return None, None