import tkinter
import random
from tkinter import messagebox

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
botoes = []  # Lista para armazenar os objetos Button
is_cheking = False  # Flag para evitar cliques enquanto o par está sendo verificado

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


def iniciar():
    janela_principal = tkinter.Tk()
    janela_principal.title("Jogo da Memória")
    janela_principal.geometry("400x300")
    janela_principal.resizable(False, False)

    frame_tabuleiro = tkinter.Frame(janela_principal, bg="#333333", padx=10, pady=10)
    frame_tabuleiro.pack(pady=20)

    matriz_logica = criar_tabuleiro()

    return frame_tabuleiro, janela_principal, matriz_logica

# Comentário enquanto estiver usando a classe principal
frame_tabuleiro, janela_principal, matriz_logica = iniciar()
# Comentário enquanto estiver usando a classe principal


def checar_par():
    """Verifica se as duas cartas viradas formam um par."""
    global primeira_escolha_btn, segunda_escolha_btn, cartoes_encontrados, is_cheking

    # Acessa as coordenadas diretamente das variáveis globais
    l1, c1 = primeira_escolha_btn.grid_info()['row'], primeira_escolha_btn.grid_info()['column']
    l2, c2 = segunda_escolha_btn.grid_info()['row'], segunda_escolha_btn.grid_info()['column']

    if matriz_logica[l1][c1] == matriz_logica[l2][c2]:
        # Par encontrado: desabilita os botões e os afunda visualmente
        primeira_escolha_btn.config(state=tkinter.DISABLED, relief=tkinter.SUNKEN)
        segunda_escolha_btn.config(state=tkinter.DISABLED, relief=tkinter.SUNKEN)
        cartoes_encontrados += 2

        if cartoes_encontrados == 12:
            messagebox.showinfo("Parabéns!", "Você encontrou todos os pares!")
            janela_principal.quit()  # Fecha a janela do jogo
    else:
        # Não é um par: vira as cartas de volta
        primeira_escolha_btn.config(bg='gray', state=tkinter.NORMAL)
        segunda_escolha_btn.config(bg='gray', state=tkinter.NORMAL)

    # Reseta as variáveis para a próxima jogada
    primeira_escolha_btn = None
    segunda_escolha_btn = None
    is_cheking = False


def virar_carta(l, c, cartao_clicado):
    """Lida com o clique do jogador em uma carta."""
    global primeira_escolha_btn, segunda_escolha_btn, is_cheking

    if is_cheking or cartao_clicado == primeira_escolha_btn:
        # Impede cliques enquanto o jogo está checando um par ou se o jogador clicou na mesma carta
        return

    cor_carta = CORES_MAP[matriz_logica[l][c]]

    # Vira a carta na interface
    cartao_clicado.config(bg=cor_carta, state=tkinter.DISABLED)

    if not primeira_escolha_btn:
        primeira_escolha_btn = cartao_clicado
    else:
        segunda_escolha_btn = cartao_clicado
        is_cheking = True
        # Agenda a checagem do par para ocorrer após 1 segundo
        janela_principal.after(1000, checar_par)


# --- Criação da Interface Gráfica ---
def mainJ():
    # Cria e posiciona os botões do tabuleiro
    for l in range(3):
        for c in range(4):
            cartao = tkinter.Button(frame_tabuleiro, text=' ', font=('Arial', 18), width=5, height=2, bg='gray', activebackground='lightgray')
            
            # Correção: Passa l e c diretamente para a função usando lambda
            cartao.config(command=lambda linha=l, coluna=c, btn=cartao: virar_carta(linha, coluna, btn))
            
            # Posiciona o botão na grade
            cartao.grid(row=l, column=c, padx=5, pady=5)
            botoes.append(cartao)

    # --- Inicia a aplicação ---
    janela_principal.mainloop()


if __name__ == "__main__":
    mainJ()
    iniciar()
