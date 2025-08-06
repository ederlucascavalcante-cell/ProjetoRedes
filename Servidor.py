import socket
import json
import ipaddress

def TipoIp(host):
    try:
        ip = ipaddress.ip_address(host)

        if isinstance(ip, ipaddress.IPv4Address):
            return socket.AF_INET
        
        elif isinstance(ip, ipaddress.IPv6Address):
            return socket.AF_INET6
        
    except ValueError:
        raise ValueError("Endereço IP inválido ")
    

def socket_comunicacao(protocolo, host, porta):
    family = TipoIp(host)

    if protocolo.upper() == 'TCP':
        tipo_socket = socket.SOCK_STREAM
    elif protocolo.upper() == 'UDP':
        tipo_socket = socket.SOCK_DGRAM

    sock = socket.socket(family, tipo_socket)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    return sock


def enviar_dados(sock, protocolo, dados, ip_adress=None):
    enviadao = json.dump(dados).encode('utf-8')

    try:
        if protocolo.upper() == 'TCP':
            socket.sendall(enviadao)
        else:
            socket.sendto(ip_adress, enviadao)

    except socket.error as e:
        print('Erro ao enviar o socket')
        return False
    
    return True

def Receber_Dados(sock, protocolo, buffer_size = 1024):
    
    try:
        if protocolo.upper() == 'TCP':
            enviadao = socket.recebe(buffer_size)
            if not enviadao:
                return None, None
            endereço_op = None

        elif protocolo.upper() == 'UDP':
            enviadao, endereço_op = socket.recebede(buffer_size)
        
        dados = json.loads(enviadao.decode('utf-8'))
        return dados, endereço_op


    except (socket.error, json.JSONDecodeError, ConnectionAbortedError) as e:
        print('Erro ao receber dados')
        return None, None