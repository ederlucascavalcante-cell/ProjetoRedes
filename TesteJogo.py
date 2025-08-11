import random
import os
import platform


jogador_um = True
jogador_dois = False
escolha1,escolha2 = [],[]
l1, c1, l2, c2 = 0,0,0,0
lista_sigilo = [['xxxx','xxxx','xxxx','xxxx'],['xxxx','xxxx','xxxx','xxxx'],['xxxx','xxxx','xxxx','xxxx']]
lista_num_cores = [1,1,2,2,3,3,4,4,5,5,6,6]

def iniciar():
    matriz_memoria = []
    matriz_memoria_bool = []
    lista_num_cores = [1,1,2,2,3,3,4,4,5,5,6,6]

    for i in range (3):
        linha = []
        linha_bool = []
        for j in range(4):
            numero_da_vez = random.choice(lista_num_cores)
            linha_bool += [False]
            linha += [numero_da_vez]
            lista_num_cores.remove(numero_da_vez)
        matriz_memoria_bool += [linha_bool]
        matriz_memoria += [linha]
    ## aqui é selecionado um número entre os da matriz
    ## e esse mesmo número é retirado da lista inicial para que não possa ser escolhido novamente

    apelido = matriz_memoria

    lista_cores_reais = [['0','0','0','0'],['0','0','0','0'],['0','0','0','0']]
        ##criação da matriz vazia, para poder ser apresentada ao usuário

    for i in range(3):
        for j in range(4):
            lista_cores_reais[i][j] = found_colors(apelido[i][j])
    
    return apelido, lista_cores_reais, matriz_memoria_bool


def limpar_terminal():
    sistema_operacional = platform.system()

    if sistema_operacional == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def esconder_cartao():
    for i in range(3):
        print(lista_sigilo[i])
    print()


def mostrar_cartao(l,c,cor):
    lista_sigilo[l][c] = cor
    for i in range(3):
        print(lista_sigilo[i])
    print()
    lista_sigilo[l][c] = 'xxxx'


def atualizar_tabuleiro(l1,c1,cor1, l2, c2, cor2):
    lista_sigilo[l1][c1] = cor1
    lista_sigilo[l2][c2] = cor2


def atualizar_tabuleiro_bool(l1,c1, l2, c2):
    matriz_memoria_bool[l1][c1] = True
    matriz_memoria_bool[l2][c2] = True


def found_colors (n):
    if n == 1:
        return "red"
    if n == 2:
        return "green"
    if n == 3:
        return "blue"
    if n == 4:
        return "orange"
    if n == 5:
        return "black"
    if n == 6:
        return "white"

#  Cores e seus pares:
#   1 - red
#   2 - green
#   3 - blue
#   4 - orange
#   5 - black
#   6 - white

apelido, lista_cores_reais, matriz_memoria_bool = iniciar()

while True:

    esconder_cartao()


    if jogador_um:
        while True:
            escolha1 = input().split()
            l1 = int(escolha1[0])
            c1 = int(escolha1[1])
            if matriz_memoria_bool[l1][c1] == False:
                mostrar_cartao(l1, c1, lista_cores_reais[l1][c1])
                print()
                break
            else:
                print("Essa carta ja foi encontrada")
            
        while True:
            escolha2 = input().split()
            l2 = int(escolha2[0])
            c2 = int(escolha2[1])
            if matriz_memoria_bool[l2][c2] == False:
                mostrar_cartao(l2, c2, lista_cores_reais[l2][c2])
                print()
                break
            else:
                print("Essa carta ja foi encontrada")

        limpar_terminal()

        if apelido[l1][c1] == apelido[l2][c2]:
            print("You find one pair! Congratulations!")
            atualizar_tabuleiro(l1, c1, lista_cores_reais[l1][c1], l2, c2, lista_cores_reais[l2][c2])
            atualizar_tabuleiro_bool(l1,c1, l2,c2)
            esconder_cartao()