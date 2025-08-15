import tkinter
import random
import socket
from tkinter import messagebox
import threading
import queue
import json

# --- Configurações e Variáveis Globais do Jogo ---

# Dicionário que mapeia números para cores
CORES_MAP = {
    1: 'red',
    2: 'green',
    3: 'blue',
    4: 'orange',
    5: 'purple',
    6: 'white',
}

# Variáveis de controle do jogo
primeira_escolha_btn = None
segunda_escolha_btn = None
cartoes_encontrados = 0
botoes = []
is_cheking = False

# --- NOVAS VARIÁVEIS PARA MULTIPLAYER ---
minha_vez = True  # Controla se é a vez do jogador local
comunicacao = None  # Socket para comunicação
protocolo = None   # TCP ou UDP
endereco_op = None # Endereço do oponente (para UDP)
minha_pontuacao = 0
pontuacao_oponente = 0
jogo_ativo = True
fila_mensagens = queue.Queue()  # Para comunicação entre threads

# Variáveis da interface
janela_principal = None
frame_tabuleiro = None
matriz_logica = None
label_status = None
label_placar = None

# --- Funções de Rede ---

def protocolo_criar_mensagem(tipo, dados):
    """Cria mensagem seguindo protocolo definido"""
    return json.dumps({
        'tipo': tipo,
        'dados': dados
    })

def protocolo_parsear_mensagem(mensagem_raw):
    """Decodifica mensagem recebida"""
    try:
        return json.loads(mensagem_raw)
    except:
        return None

def enviar_jogada_rede(jogada_dados):
    """Envia jogada através da rede"""
    global comunicacao, protocolo, endereco_op
    
    try:
        mensagem = protocolo_criar_mensagem('JOGADA', jogada_dados)
        
        if protocolo == 'TCP':
            comunicacao.send(mensagem.encode())
        else:  # UDP
            comunicacao.sendto(mensagem.encode(), endereco_op)
            
    except Exception as e:
        messagebox.showwarning(f"ERRO",f"Erro ao enviar jogada: {e}")

def thread_receber_mensagens():
    """Thread para receber mensagens do oponente"""
    global comunicacao, protocolo, fila_mensagens, jogo_ativo
    
    comunicacao.settimeout(1.0)

    while jogo_ativo:
        try:
            if protocolo == 'TCP':
                dados = comunicacao.recv(1024).decode()
            else:  # UDP
                dados, _ = comunicacao.recvfrom(1024)
                dados = dados.decode()
            
            mensagem = protocolo_parsear_mensagem(dados)
            if mensagem:
                fila_mensagens.put(mensagem)
                
        except socket.timeout:
            continue
        except Exception as e:
            if jogo_ativo:  # Só mostra erro se o jogo ainda estiver ativo
                messagebox.showwarning("ERRO",f"Erro ao receber mensagem: {e}")
            break

# --- Funções de Lógica do Jogo ---

def criar_tabuleiro():
    """Gera a matriz lógica do jogo com pares de números aleatórios."""
    lista_num_cores = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
    random.shuffle(lista_num_cores)

    matriz = [
        lista_num_cores[0:4],
        lista_num_cores[4:8],
        lista_num_cores[8:12]
    ]
    return matriz

def atualizar_interface():
    """Atualiza labels da interface com informações do jogo"""
    global label_status, label_placar, minha_vez, minha_pontuacao, pontuacao_oponente
    
    if matriz_logica is None:
        status_text = "⏳ AGUARDANDO TABULEIRO..."
        cor_status = "orange"
    elif minha_vez:
        status_text = "🎯 SUA VEZ - Clique em duas cartas!"
        cor_status = "green"
    else:
        status_text = "⏳ VEZ DO OPONENTE - Aguarde..."
        cor_status = "red"
    
    label_status.config(text=status_text, fg=cor_status)
    label_placar.config(text=f"Você: {minha_pontuacao} | Oponente: {pontuacao_oponente}")

def processar_jogada_oponente(jogada_dados):
    """Processa jogada recebida do oponente"""
    global pontuacao_oponente, cartoes_encontrados, botoes, matriz_logica
    
    if matriz_logica is None:
        messagebox.showwarning("Erro: Tentativa de processar jogada sem tabuleiro sincronizado!")
        return
    
    linha1 = jogada_dados['linha1']
    coluna1 = jogada_dados['coluna1']
    linha2 = jogada_dados['linha2']
    coluna2 = jogada_dados['coluna2']
    resultado = jogada_dados['resultado']
    
    # Encontra os botões correspondentes
    btn1 = None
    btn2 = None
    
    for btn in botoes:
        grid_info = btn.grid_info()
        if grid_info['row'] == linha1 and grid_info['column'] == coluna1:
            btn1 = btn
        elif grid_info['row'] == linha2 and grid_info['column'] == coluna2:
            btn2 = btn
    
    if btn1 and btn2:
        # Mostra as cartas viradas pelo oponente
        cor1 = CORES_MAP[matriz_logica[linha1][coluna1]]
        cor2 = CORES_MAP[matriz_logica[linha2][coluna2]]
        
        btn1.config(bg=cor1, state=tkinter.DISABLED)
        btn2.config(bg=cor2, state=tkinter.DISABLED)
        
        def processar_resultado():
            global minha_vez, pontuacao_oponente, cartoes_encontrados
            
            if resultado == 'acerto':
                # Par encontrado: mantém as cartas viradas
                btn1.config(relief=tkinter.SUNKEN)
                btn2.config(relief=tkinter.SUNKEN)
                pontuacao_oponente += 1
                cartoes_encontrados += 2
                # Oponente continua jogando
                messagebox.showinfo("INFO","Oponente encontrou um par!")
            else:
                # Não é par: vira as cartas de volta
                btn1.config(bg='gray', state=tkinter.NORMAL)
                btn2.config(bg='gray', state=tkinter.NORMAL)
                # Passa a vez para o jogador local
                minha_vez = True
                messagebox.showinfo("INFO","Oponente errou! Sua vez!")
            
            atualizar_interface()
            verificar_fim_jogo()
        
        # Processa o resultado após 2 segundos para o jogador ver
        janela_principal.after(2000, processar_resultado)

def verificar_fim_jogo():
    """Verifica se o jogo terminou e mostra o resultado"""
    global cartoes_encontrados, jogo_ativo
    
    if cartoes_encontrados == 12:
        jogo_ativo = False
        
        if minha_pontuacao > pontuacao_oponente:
            resultado = "VOCÊ VENCEU!"
        elif pontuacao_oponente > minha_pontuacao:
            resultado = "VOCÊ PERDEU!"
        else:
            resultado = "EMPATE!"
        
        messagebox.showinfo("Fim de Jogo", 
                          f"{resultado}\n\n"
                          f"Placar Final:\n"
                          f"Você: {minha_pontuacao} pares\n"
                          f"Oponente: {pontuacao_oponente} pares")
        
        janela_principal.quit()

def checar_par():
    """Verifica se as duas cartas viradas formam um par."""
    global primeira_escolha_btn, segunda_escolha_btn, cartoes_encontrados, is_cheking
    global minha_pontuacao, minha_vez

    if matriz_logica is None:
        return

    # Acessa as coordenadas das cartas
    l1 = primeira_escolha_btn.grid_info()['row']
    c1 = primeira_escolha_btn.grid_info()['column']
    l2 = segunda_escolha_btn.grid_info()['row']
    c2 = segunda_escolha_btn.grid_info()['column']

    # Verifica se é um par
    eh_par = matriz_logica[l1][c1] == matriz_logica[l2][c2]
    
    # Prepara dados da jogada para enviar
    jogada_dados = {
        'linha1': l1,
        'coluna1': c1,
        'linha2': l2,
        'coluna2': c2,
        'resultado': 'acerto' if eh_par else 'erro'
    }
    
    # Envia jogada pela rede
    enviar_jogada_rede(jogada_dados)

    if eh_par:
        # Par encontrado
        primeira_escolha_btn.config(state=tkinter.DISABLED, relief=tkinter.SUNKEN)
        segunda_escolha_btn.config(state=tkinter.DISABLED, relief=tkinter.SUNKEN)
        cartoes_encontrados += 2
        minha_pontuacao += 1
        # Continua sendo minha vez
        messagebox.showinfo("INFO","Você encontrou um par! Jogue novamente!")
    else:
        # Não é um par
        primeira_escolha_btn.config(bg='gray', state=tkinter.NORMAL)
        segunda_escolha_btn.config(bg='gray', state=tkinter.NORMAL)
        # Passa a vez para o oponente
        minha_vez = False
        messagebox.showinfo("INFO","Não foi um par! Vez do oponente.")

    # Reset das variáveis
    primeira_escolha_btn = None
    segunda_escolha_btn = None
    is_cheking = False
    
    atualizar_interface()
    verificar_fim_jogo()

def virar_carta(l, c, cartao_clicado):
    """Lida com o clique do jogador em uma carta."""
    global primeira_escolha_btn, segunda_escolha_btn, is_cheking, minha_vez

    # Verifica se o tabuleiro foi sincronizado
    if matriz_logica is None:
        messagebox.showwarning("Atenção", "Aguarde a sincronização do tabuleiro!")
        return

    # Verifica se é a vez do jogador
    if not minha_vez:
        messagebox.showwarning("Atenção", "Não é sua vez! Aguarde o oponente jogar.")
        return
    
    if is_cheking or cartao_clicado == primeira_escolha_btn:
        return

    cor_carta = CORES_MAP[matriz_logica[l][c]]
    cartao_clicado.config(bg=cor_carta, state=tkinter.DISABLED)

    if not primeira_escolha_btn:
        primeira_escolha_btn = cartao_clicado
    else:
        segunda_escolha_btn = cartao_clicado
        is_cheking = True
        # Agenda a checagem do par para ocorrer após 1 segundo
        janela_principal.after(1000, checar_par)

def confirmar_sincronizacao():
    """Confirma que recebeu o tabuleiro"""
    global comunicacao, protocolo, endereco_op
    
    confirmacao = {
        'tipo': 'CONFIRMACAO_SYNC',
        'dados': {'status': 'tabuleiro_recebido'}
    }
    
    try:
        mensagem = json.dumps(confirmacao)
        
        if protocolo == 'TCP':
            comunicacao.send(mensagem.encode())
        else:  # UDP
            comunicacao.sendto(mensagem.encode(), endereco_op)
                        
    except Exception as e:
        messagebox.showwarning(f"Erro ao confirmar sincronização: {e}")

def processar_mensagens_recebidas():
    """Processa mensagens recebidas da fila (versão atualizada)"""
    global matriz_logica, label_status
    
    try:
        while not fila_mensagens.empty():
            mensagem = fila_mensagens.get_nowait()
            
            if mensagem['tipo'] == 'JOGADA':
                processar_jogada_oponente(mensagem['dados'])
            
            elif mensagem['tipo'] == 'SYNC_TABULEIRO':
                # Recebe o tabuleiro do hospedeiro
                matriz_logica = mensagem['dados']['matriz']
                
                # Atualiza interface para mostrar que está pronto
                atualizar_interface()
                
                # Confirma recebimento
                confirmar_sincronizacao()
            
            elif mensagem['tipo'] == 'CONFIRMACAO_SYNC':
                # Hospedeiro pode começar a jogar
                atualizar_interface()
                
    except queue.Empty:
        pass
    
    # CORREÇÃO: Agenda a próxima verificação apenas uma vez
    if jogo_ativo:
        janela_principal.after(100, processar_mensagens_recebidas)

def iniciar_jogo_multiplayer(socket_comunicacao, protocolo_usado, endereco_oponente, sou_hospedeiro):
    """Inicializa o jogo multiplayer"""
    global comunicacao, protocolo, endereco_op, minha_vez
    
    comunicacao = socket_comunicacao
    protocolo = protocolo_usado
    endereco_op = endereco_oponente
    minha_vez = sou_hospedeiro  # Hospedeiro sempre começa
    
def sincronizar_tabuleiro():
    """Hospedeiro cria e envia o tabuleiro para o oponente"""
    global matriz_logica, comunicacao, protocolo, endereco_op
        
    if not minha_vez:  # Se não sou hospedeiro, não crio tabuleiro
        return
        
    # Se ainda não tem tabuleiro, cria
    if matriz_logica is None:
        matriz_logica = criar_tabuleiro()
    
    # Prepara dados para envio
    dados_tabuleiro = {
        'tipo': 'SYNC_TABULEIRO',
        'dados': {
            'matriz': matriz_logica,
        }
    }
    
    try:
        mensagem = json.dumps(dados_tabuleiro)
        
        if protocolo == 'TCP':
            comunicacao.send(mensagem.encode())
        else:  # UDP
            comunicacao.sendto(mensagem.encode(), endereco_op)
            
        atualizar_interface()
        
    except Exception as e:
        messagebox.showwarning(f"Erro ao enviar tabuleiro: {e}")

def iniciar():
    """Inicializa a interface gráfica"""
    global janela_principal, frame_tabuleiro, matriz_logica, label_status, label_placar
    
    janela_principal = tkinter.Tk()
    janela_principal.title("Jogo da Memória - Multiplayer")
    janela_principal.geometry("500x400")
    janela_principal.resizable(False, False)

    # Frame para informações do jogo
    frame_info = tkinter.Frame(janela_principal, bg="#222222")
    frame_info.pack(fill='x', padx=10, pady=5)

    label_status = tkinter.Label(frame_info, text="🎯 PREPARANDO JOGO...", font=('Arial', 12, 'bold'), 
                                bg="#222222", fg="yellow")
    label_status.pack(pady=5)

    label_placar = tkinter.Label(frame_info, text="Você: 0 | Oponente: 0", font=('Arial', 10), 
                                bg="#222222", fg="white")
    label_placar.pack()

    # Frame para o tabuleiro
    frame_tabuleiro = tkinter.Frame(janela_principal, bg="#333333", padx=10, pady=10)
    frame_tabuleiro.pack(pady=10)

    # LÓGICA DO TABULEIRO BASEADA EM QUEM É HOSPEDEIRO
    if minha_vez:  # Se sou hospedeiro
        matriz_logica = None  # Será criado na sincronização
        # Agenda sincronização após interface estar pronta
        janela_principal.after(2000, sincronizar_tabuleiro)
    else:
        # Cliente aguarda receber o tabuleiro
        matriz_logica = None

    return frame_tabuleiro, janela_principal

def mainJ():
    """Função principal que cria a interface do jogo"""
    global botoes, jogo_ativo
    
    # Inicializa a interface
    frame_tabuleiro, janela_principal = iniciar()
    
    # Inicia thread para receber mensagens do oponente
    if comunicacao:
        thread_recv = threading.Thread(target=thread_receber_mensagens, daemon=True)
        thread_recv.start()
        
        # Inicia processamento de mensagens na interface
        janela_principal.after(100, processar_mensagens_recebidas)
    
    # Cria e posiciona os botões do tabuleiro
    botoes = []  # Reset da lista de botões
    for l in range(3):
        for c in range(4):
            cartao = tkinter.Button(frame_tabuleiro, text=' ', font=('Arial', 18), 
                                  width=5, height=2, bg='gray', activebackground='lightgray')
            
            cartao.config(command=lambda linha=l, coluna=c, btn=cartao: virar_carta(linha, coluna, btn))
            cartao.grid(row=l, column=c, padx=5, pady=5)
            botoes.append(cartao)

    # Atualiza interface inicial
    atualizar_interface()
    
    # Configura o fechamento da janela
    def ao_fechar():
        global jogo_ativo
        jogo_ativo = False
        if comunicacao:
            try:
                comunicacao.close()
            except:
                pass
        janela_principal.destroy()
    
    janela_principal.protocol("WM_DELETE_WINDOW", ao_fechar)
    
    # Inicia a aplicação
    janela_principal.mainloop()

if __name__ == "__main__":
    # Para teste local sem rede
    mainJ()