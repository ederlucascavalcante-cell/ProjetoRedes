# Jogo da Memória com Suporte a Múltiplos Protocolos

## Descrição do Projeto
Este projeto consiste na implementação de uma aplicação de rede peer-to-peer (P2P) para um típico jogo da memória. O objetivo principal
é aplicar e demonstrar os conceitos fundamentais das camadas de Rede e Transporte do modelo TCP/IP, permitindo então a competição entre 
dois jogadores em diferentes configurações de rede.
O projeto foi desenvolvido na linguagem Python e utilizando a biblioteca 'socket' para comunicação direta entre jogadores. Essa biblioteca
oferece a flexibilidade de escolha entre os protocolos TCP e UDP e possui suporte para endereçamentos IPv4 e IPv6.

## Participantes 
- João Victor Barbosa do Nascimento - Matrícula: 20231054010036
- João Augusto de Sá Leitão Dantas - Matrícula: 20231054010002
- Pedro Lucas Cavalcante dos Santos - Matrícula: 20231054010012
- Eder Lucas de Oliveira Cavalcanti - Matrícula: 20231054010023
- Reysson Medeiros Gomes de Brito - Matrícula: 20231054010017

## Instruções para execução da aplicação
Para jogar, ambos os jogadores precisam ter o Python 3 instalado em suas máquinas.
O jogo será executado por meio do terminal, seguindo os passos adiante:

1 - Abra o Prompt de Comando    
2 - Vá até a pasta onde estão os arquivos do projeto.    
3 - Execute o cliente, por meio do seguinte comando:

	python Cliente.py

4 - Em seguida o programa irá te guiar por meio de um menu interativo para poder configurar a partida.

### Como Hospedar uma Partida (Jogador 1)
1 - Execute 'python Cliente.py'                             
2 - Quando perguntado, digite 'h' para hospedar uma partida			                                                                                                 	          
3 - Escolha o protocolo de transporte (TCP ou UDP)				                                                                                        
4 - Insira o endereço IP da sua máquina (IPv4 ou IPv6)					                                 
5 - Escolha a porta para comunicação (ex:8000)				                                 
6 - Aguarde a comunicação do outro jogador		

### Como se conectar a uma partida (Jogador 2)
1 - Execute python Cliente.py                                
2 - Quando perguntado, digite 'c' para se conectar                             
3 - Escolha o mesmo protocolo que o Jogador 1 selecionou                            
4 - Insira o endereço IP do Jogador 1                          
5 - Insira a mesma porta que o Jogador 1 definiu                           
6 - A conexão será estabelecida e o jogo vai começar                           

## Protocolo de camada de aplicação
Para garantir um padrão na comunicação entre os cliente, um protocolo de camada de aplicação simples foi definido. As mensagens são trocadas no formato JSON, que oferece flexibildiade e clareza. Todas as mensagens enviadas contêm um campo 'tipo' que define sua finalidade.

### Tipos de Mensagens Definidos: 
- INICIAR_CONEXAO (Apenas UDP)
- Descrição: Usada pelo cliente que se conecta para que o hospedeiro (host) descubra o seu endereço IP e porta.
- Exemplo: 

		{
		  "tipo": "INICIAR_CONEXAO",
		  "dados": {
		    "mensagem": "quero_conectar"
		  }
		}

- JOGADA
- Descição: Enviada por um jogador para informar ao oponente qual carta foi virada. São enviadas duas mensagens deste tipo por turno.
- Exemplo:

		{
		  "tipo": "JOGADA",
		  "dados": {
		    "jogador": "Jogador 1",
		    "linha": 0,
		    "coluna": 2
		  }
		}

- ATUALIZAR_ESTADO
- Descrição: Enviada após uma jogada para sincronizar o estado do jogo em ambos os clientes. Informa qual o tabuleiro atual, de quem é a vez e a pontuação.
- Exemplo:

		  {
		  "tipo": "ATUALIZAR_ESTADO",
		  "dados": {
		    "tabuleiro_sigilo": "[['xxxx', 'blue', ...], ...]",
		    "turno": "Jogador 2",
		    "pares_j1": 3,
		    "pares_j2": 1
		  }
		}

- FIM_DE_JOGO
- Descrição: Anuncia que todas as cartas foram encontradas e declara o vencedor.
- Exemplo:

		{
		  "tipo": "FIM_DE_JOGO",
		  "dados": {
		    "vencedor": "Jogador 1",
		    "mensagem": "Parabéns, você venceu!"
		  }
		}


Arquivo README.md escrito por João Victor.
