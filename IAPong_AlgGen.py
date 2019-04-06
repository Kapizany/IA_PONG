from random import random
from random import randint
import matplotlib.pyplot as plt
import math
import enum

class Constantes(enum.Enum):
    
    nota_max = 100
    nota_min = 0.01
    tamanho_populacao = 30
    taxa_mutacao = 0.01
    numero_geracoes = 200
    board_size = 66*3

def gerarBase(windowWidth,max_pos_ball,min_pos_ball):
    'a base determina as posicoes de maximo e minimo da bola ocm base no tamanho da janela '
    distance = max_pos_ball - min_pos_ball
    base = [[], []]

    for j in range(0,windowWidth+1,3):
        for i in range (0,distance +1,5):
            base[0].append(j) # posiçao da raquete
            base[1].append(i + min_pos_ball) #posição da bolinha
    return base

class Jogada:

    def __init__(self, x_raquete, x_ball):
        self.x_raquete = x_raquete
        self.x_ball = x_ball

class Jogador:

    def __init__(self, difference,board_size, geracao=0):
        'A construtora da classe Jogador (populacao)'
        self.difference = difference # diferenca entre x_ball e x_raquete, nessa ordem. Se >0 bolinha a direita da raquete, se < 0 bolinha e esquerda da raquete.
        self.board_size = board_size #tamanho da raquete
        self.geracao = geracao
        self.nota_avaliacao = 0
        self.notas_jogadas = []
        self.cromossomo = []

        for i in range(len(difference)):
            #os valores do cromossomo sao binarios. 
            self.cromossomo.append(randint(0,1)) # 0 esquerda e 1 direita

    def avaliacao (self):
        'A avaliacao atribui nota a cada individuo de acordo com o cromossomo e a diferenca entre '
        'a posicao da raquete e a posicao da bola.'
        'Se o cromossomo e a diferenca forem para a mesma direcao, isto e, o cromossomo manda a raquete'
        'para a direcao por onde a bola passa, entao a nota maxima e somada.'
        'Caso contrario, a nota minima e somada.'
        'A selecao de individuos ocorre ao escolher os membros com nota mais alta para a ... copula'
        nota = 0
        for i in range(len(self.cromossomo)):
            if ((self.cromossomo[i] == 0) and (self.difference[i]<=0)): # Se manda a raquete para a esquerda e a bolinha esta a esquerda ok
                nota += Constantes.nota_max.value
                self.notas_jogadas.append(Constantes.nota_max.value)
            elif ((self.cromossomo[i] == 1) and (self.difference[i] > 0)): # Se manda a raquete para a direita e a bolinha esta a direita ok
                nota += Constantes.nota_max.value
                self.notas_jogadas.append(Constantes.nota_max.value)
            else: #se nao eh nenhum dos 3, errouw
                nota += Constantes.nota_min.value
                self.notas_jogadas.append(Constantes.nota_min.value)

        self.nota_avaliacao = nota

    def crossover(self, outro_individuo):
        'O crossover é responsável por uma troca de cromossomos'
        'entre dois pais em uma regiao de corte selecionada'
        'aleatoriamente na lista.'
        'Formam-se dois filhos que receberao as trocas de cromossomos e passam a fazer'
        'parte da populacao.'

        corte = round(random()*len(self.cromossomo))
        #corte e um inteiro que define a posicao da lista que sera 'dividida' e trocada

        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        #apos estabelecer o corte, a lista de cromossomos e divida em dois. 
        # filho1 = [comeco da lista ate o corte do pai1] + [corte em diante do pai 2]
        #filho2 = [comeco da lista ate o corte do pai 2] + [corte em diante do pai 1]
        filhos =[Jogador(self.difference,self.board_size, self.geracao + 1), Jogador(self.difference,self.board_size, self.geracao + 1)]
        #filhos sao adicionadas a classe Jogador e depois ganham os atributos de cromossomo trocados acima
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos

    def mutacao (self, taxa_mutacao):
        'A mutacao altera aleatoriamente o valor de um cromossomo'
        'a probabilidade dessa mutacao ocorrer e dado pela taxa de mutacao'
        'se ela for maior que um float entre 0 e 1 a mutacao ocorre'
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == 0:
                    self.cromossomo[i] = 1
                else:
                    self.cromossomo[i] = 0
        return self

class AlgoritmoGenetico:

    def __init__(self,tamanho_populacao):
        'construtor do AlgoritmoGenetico, responsavel por criar e selecionar a populacao'
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = [] #armazena as melhores availiacoes

    def inicializa_populacao(self, difference, board_size):
        'Cria a populacao. Para cada inteiro no intervalo estabelecido pelo range,'
        'um novo Jogador e adicionado.'
        for i in range(self.tamanho_populacao):
            self.populacao.append(Jogador(difference,board_size))
        self.melhor_solucao = self.populacao[0]
        #inicialmente, escolhemos como melhor solucao o primeiro elemento da lista. 
        #a cada geracao, este individuo e substituido por outro com maior nota.

    def ordenaPopulacao(self):
        'usa o sort para ordenar a lista de jogadores, comecando por individuos com maior nota ate o que tem a menor'
        'nota.'
        self.populacao= sorted(self.populacao, 
                                    key = lambda populacao: populacao.nota_avaliacao, reverse = True)

    def melhorJogador(self,jogador):
        'A cada geracao, o jogador com maior nota fica em primeiro na lista'
        if jogador.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            #se a nota de avaliacao for maior que a nota do primeiro da lista, este e substituido por aquele.
            self.melhor_solucao = jogador

    def somaAvaliacoes(self):
        soma = 0
        for jogador in self.populacao:
            soma += jogador.nota_avaliacao
        return soma
    def selecionaPai(self, soma_avaliacao):
        ''
        pai = -1
        valor_sorteado = random()*soma_avaliacao
        soma = 0
        i=0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai


    def resolver(self, taxa_mutacao, numero_geracoes, difference, board_size):
        self.inicializa_populacao(difference, board_size)

        for jogador in self.populacao:
            #faz a avaliacao para os jogadores na populacao
            jogador.avaliacao()
        
        self.ordenaPopulacao()
        #ordena a populacao da nota mais alta ate a mais baixa
        self.melhorJogador(self.populacao[0])
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao) 

        for geracao in range(numero_geracoes):
            soma_avaliacao = self.somaAvaliacoes()
            nova_populacao = []

            for individuos_gerados in range(0,self.tamanho_populacao,2):
                #seleciona o pai para criar os filhos por meio de crossover.
                pai1 = self.selecionaPai(soma_avaliacao)
                pai2 = self.selecionaPai(soma_avaliacao)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                # a nova populacao passa por um processo de mutacao. Isto e, pode ou nao ter os valores
                #do cromossomo alterados
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            self.populacao = list(nova_populacao)

            for jogador in self.populacao:
                jogador.avaliacao()
            
            self.ordenaPopulacao()
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao) 
            self.melhorJogador(melhor)
        return self.melhor_solucao.cromossomo


x_ball = []
x_raquete = []
difference = []
base = gerarBase(960,15*44,3*44) #Escolhido com base no tamanho da tela e do range de onde a bolinha pode aparecer
#base [0] coluna posicao raquete
#base[1] coluna posicao bolinha
x_raquete = base[0][:]
x_ball = base[1][:]
for i in range(len(base[0])):
    difference.append(x_ball[i] - x_raquete[i])

tamanho_populacao = Constantes.tamanho_populacao.value
taxa_mutacao = Constantes.taxa_mutacao.value
numero_geracoes = Constantes.numero_geracoes.value
board_size = Constantes.board_size.value

ag = AlgoritmoGenetico(tamanho_populacao)

resultado = ag.resolver(taxa_mutacao, numero_geracoes, difference, board_size)
f = open('base_treino.txt', 'w')
#o arquivo aberto recebe as posicoes da raquete, da bola e do resultado da selecao de nota e ordenacao

j=0
for i in range(len(base[0])):
    if ag.melhor_solucao.notas_jogadas[i] == Constantes.nota_max.value:
        f.write(str(x_ball[i]) + ' ')
        f.write (str(x_raquete[i]) + ' ')
        f.write (str(resultado[i]) + '\n')
        j+=1
f.close()
print(len(resultado))
print(str(ag.melhor_solucao.nota_avaliacao))
print (j)
plt.plot(ag.lista_solucoes)
plt.title("Acompanhamento dos valores")
plt.show()