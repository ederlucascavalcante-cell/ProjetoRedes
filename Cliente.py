import socket
import tkinter as tk
from tkinter import messagebox
import sys
# 'receber_dados', 'enviar_dados', e 'socket_comunicacao' devem estar no módulo 'Servidor'
from Servidor import receber_dados, socket_comunicacao, enviar_dados
from JogoInterface import iniciar_jogo_multiplayer, mainJ, iniciar, criar_tabuleiro

# Variáveis de comunicação, que serão configuradas na janela inicial
comunicacao = None
protocolo = None
endereco_op = None
sou_hospedeiro = False
jogo_ativo = True

def iniciar_conexao_e_jogo(host, modo, porta, protocolo_usado):
    """
    Estabelece a conexão de rede e inicia o jogo.
    Esta função é chamada após o usuário clicar em 'Conectar' na GUI.
    """
    global comunicacao, protocolo, endereco_op, sou_hospedeiro, jogo_ativo
    
    sock = None
    conn = None
    
    try:
        sock = socket_comunicacao(protocolo_usado, host, porta)
        sock.settimeout(10)  # Define um tempo limite para a conexão

        if modo == 'H':
            sou_hospedeiro = True
            sock.bind((host, porta))
            
            if protocolo_usado == 'TCP':
                sock.listen(1)
                messagebox.showinfo("Aguardando Conexão","Aguardando um oponente se conectar...")
                print()
                conn, addr = sock.accept()
                print()
                messagebox.showinfo("INFO", f"Oponente conectado de {addr}. Partida iniciada!")
                comunicacao = conn
                endereco_op = addr
            elif protocolo_usado == 'UDP':
                messagebox.showinfo("Aguardando Conexão", "Aguardando a primeira mensagem do oponente...")
                print()
                # O hospedeiro precisa esperar a primeira mensagem para obter o endereço do oponente
                iniciar_msg, endereco_op = receber_dados(sock, 'UDP')
                if iniciar_msg and iniciar_msg.get('cond') == 'iniciar':
                    messagebox.showinfo("[INFO]",f"Oponente conectado de {endereco_op}. Partida iniciada!")
                    comunicacao = sock
                else:
                    raise ConnectionAbortedError("Erro ao receber mensagem de início do oponente.")

        else:  # Modo cliente
            sou_hospedeiro = False
            endereco_op = (host, porta)
            
            if protocolo_usado == 'TCP':
                messagebox.showinfo("Conectando", "Tentando conectar ao hospedeiro...")
                print()
                sock.connect(endereco_op)
                print()
                messagebox.showinfo("INFO", "Conectado ao hospedeiro.")
                comunicacao = sock
            elif protocolo_usado == 'UDP':
                messagebox.showinfo("Conectando", "Enviando mensagem para iniciar a conexão...")
                print()
                dados_resposta = {'cond' : 'iniciar'}
                enviar_dados(sock, 'UDP', dados_resposta, endereco_op)
                messagebox.showinfo("INFO", "Mensagem inicial enviada.")
                comunicacao = sock
        
        # Chama a função do JogoInterface para injetar os dados de rede
        iniciar_jogo_multiplayer(comunicacao, protocolo_usado, endereco_op, sou_hospedeiro)

        # Inicia a interface do jogo da memória
        mainJ()

    except socket.timeout:
        messagebox.showerror("Erro de Conexão", "Tempo limite de conexão esgotado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao estabelecer conexão: {e}")
    finally:
        # A lógica de fechar os sockets agora deve ser gerenciada pelo JogoInterface
        # para evitar fechar antes do jogo terminar.
        pass

def criar_janela_configuracao():
    """Cria a interface gráfica para coletar os dados de configuração."""
    
    janela = tk.Tk()
    janela.title("Configuração de Partida - Jogo da Memória")
    janela.geometry("600x500")
    janela.resizable(False, False)

    # Variáveis para armazenar as escolhas do usuário
    var_modo = tk.StringVar(value='C')  # 'H' ou 'C'
    var_protocolo = tk.StringVar(value='TCP')  # 'TCP' ou 'UDP'

    # Frame principal
    frame = tk.Frame(janela, padx=20, pady=20)
    frame.pack(expand=True)

    # Título
    tk.Label(frame, text="Configuração de Partida", font=("Arial", 16, "bold")).pack(pady=(0, 10))

    # Campo para o IP
    tk.Label(frame, text="Endereço IP do Hospedeiro:").pack(anchor='w')
    entry_host = tk.Entry(frame, width=30)
    entry_host.insert(0, '127.0.0.1')  # IP padrão para testes locais
    entry_host.pack(pady=(0, 10))

    # Campo para a Porta
    tk.Label(frame, text="Porta:").pack(anchor='w')
    entry_porta = tk.Entry(frame, width=30)
    entry_porta.insert(0, '12345')
    entry_porta.pack(pady=(0, 10))

    # Escolha de Modo
    tk.Label(frame, text="Modo:").pack(anchor='w')
    tk.Radiobutton(frame, text="Hospedar Partida", variable=var_modo, value='H').pack(anchor='w')
    tk.Radiobutton(frame, text="Conectar a Partida", variable=var_modo, value='C').pack(anchor='w')

    # Escolha de Protocolo
    tk.Label(frame, text="Protocolo:").pack(anchor='w', pady=(10, 0))
    tk.Radiobutton(frame, text="TCP", variable=var_protocolo, value='TCP').pack(anchor='w')
    tk.Radiobutton(frame, text="UDP", variable=var_protocolo, value='UDP').pack(anchor='w')

    # Botão de conexão
    def on_conectar_click():
        try:
            host = entry_host.get()
            porta = int(entry_porta.get())
            modo = var_modo.get()
            protocolo_usado = var_protocolo.get()
            
            if not 1024 <= porta <= 65535:
                messagebox.showerror("Erro", "Porta inválida. Use um valor entre 1024 e 65535.")
                return

            janela.destroy()
            iniciar_conexao_e_jogo(host, modo, porta, protocolo_usado)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número inteiro válido para a porta.")

    btn_conectar = tk.Button(janela, text="Conectar e Iniciar Jogo", command=on_conectar_click)
    btn_conectar.pack(pady=20)
    
    janela.mainloop()

if __name__ == "__main__":
    criar_janela_configuracao()