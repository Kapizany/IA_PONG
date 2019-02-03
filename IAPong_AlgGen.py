from random import random
from random import randint
import matplotlib.pyplot as plt
import math

def gerarBase(windowWidth,max_pos_ball,min_pos_ball):
    distance = max_pos_ball - min_pos_ball
    base = [[], []]
    '''f =  open('base-jogadas.txt', 'w')
    f.write('x_raquete ')
    f.write('x_ball\n')'''
    for j in range(0,windowWidth+1,5):
        for i in range (0,distance +1,5):
            '''f.write(str(j) + ' ') # posiçao da raquete
            f.write(str(i + min_pos_ball)) #posição da bolinha 
            f.write('\n')'''
            base[0].append(j) # posiçao da raquete
            base[1].append(i + min_pos_ball) #posição da bolinha
    #f.close()
    return base

class Jogada:

    def __init__(self, x_raquete, x_ball):
        self.x_raquete = x_raquete
        self.x_ball = x_ball

class Jogador:

    def __init__(self, difference,board_size, geracao=0):
        self.difference = difference # diferenca entre x_ball e x_raquete, nessa ordem. Se >0 bolinha a direita da raquete, se < 0 bolinha e esquerda da raquete.
        self.board_size = board_size #tamanho da raquete
        self.geracao = geracao
        self.nota_avaliacao = 0
        self.notas_jogadas = []
        self.cromossomo = []

        for i in range(len(difference)):
            self.cromossomo.append(randint(-1,1)) # 0 fica parado, -1 esquerda e 1 direita

    def avaliacao (self):
        nota = 0
        for i in range(len(self.cromossomo)):
            if ((self.cromossomo[i] == 0) and (math.fabs(self.difference[i])<= self.board_size*0.5)): # Se manda ficar parado e a bola esta no alcance da raquete ok
                nota += 100
                self.notas_jogadas.append(100)
            elif ((self.cromossomo[i] == -1) and (self.difference[i] < 0)): # se a bolinha esta a esquerda da raquete e manda ir pra esquerda ok
                nota += 100
                self.notas_jogadas.append(100)
            elif ((self.cromossomo[i] == 1) and (self.difference[i] > 0)): # se a bolinha esta a direita da raquete e manda ir pra direita ok
                nota += 100
                self.notas_jogadas.append(100)
            else: #se nao eh nenhum dos 3, errouw
                nota += 0.01
                self.notas_jogadas.append(0.01)

        self.nota_avaliacao = nota

    def crossover(self, outro_individuo):
        corte = round(random()*len(self.cromossomo))

        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]

        filhos =[Jogador(self.difference,self.board_size, self.geracao + 1), Jogador(self.difference,self.board_size, self.geracao + 1)]

        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos

    def mutacao (self, taxa_mutacao):
        #print("Antes: %s" %self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == -1:
                    self.cromossomo[i] = 0
                elif self.cromossomo[i] == 0:
                    self.cromossomo[i] = 1
                else:
                    self.cromossomo[i] = -1
        #print("Depois: %s" %self.cromossomo)
        return self

class AlgoritmoGenetico:

    def __init__(self,tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = [] 

    def inicializa_populacao(self, difference, board_size):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Jogador(difference,board_size))
        self.melhor_solucao = self.populacao[0]

    def ordenaPopulacao(self):
        self.populacao= sorted(self.populacao, 
                                    key = lambda populacao: populacao.nota_avaliacao, reverse = True)

    def melhorJogador(self,jogador):
        if jogador.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = jogador

    def somaAvaliacoes(self):
        soma = 0
        for jogador in self.populacao:
            soma += jogador.nota_avaliacao
        return soma
    def selecionaPai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random()*soma_avaliacao
        soma = 0
        i=0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai

    '''def vizualiza_geracao(self):
        melhor = self.populacao[0]
        print("G: %s  ->  Valor: %s  Espaco: %s  Cromossomo: %s" %(self.populacao[0].geracao,
                                                                        melhor.nota_avaliacao, melhor.espaco_usado,
                                                                        melhor.cromossomo)) '''

    def resolver(self, taxa_mutacao, numero_geracoes, difference, board_size):
        self.inicializa_populacao(difference, board_size)

        for jogador in self.populacao:
            jogador.avaliacao()
        
        self.ordenaPopulacao()
        self.melhorJogador(self.populacao[0])
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao) 
        #self.vizualiza_geracao()

        for geracao in range(numero_geracoes):
            soma_avaliacao = self.somaAvaliacoes()
            nova_populacao = []

            for individuos_gerados in range(0,self.tamanho_populacao,2):
                pai1 = self.selecionaPai(soma_avaliacao)
                pai2 = self.selecionaPai(soma_avaliacao)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            self.populacao = list(nova_populacao)

            for jogador in self.populacao:
                jogador.avaliacao()
            
            self.ordenaPopulacao()
            #self.vizualiza_geracao()
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao) 
            self.melhorJogador(melhor)
        return self.melhor_solucao.cromossomo


x_ball = []
x_raquete = []
difference = []
base = gerarBase(960,15*44,3*44)
#base [0] coluna posicao raquete
#base[1] coluna posicao bolinha
x_raquete = base[0][:]
x_ball = base[1][:]
for i in range(len(base[0])):
    difference.append(x_ball[i] - x_raquete[i])

tamanho_populacao = 30
taxa_mutacao = 0.01
numero_geracoes = 200
board_size = 66*3

ag = AlgoritmoGenetico(tamanho_populacao)

resultado = ag.resolver(taxa_mutacao, numero_geracoes, difference, board_size)
f = open('base_treino.txt', 'w')
j=0
for i in range(len(base[0])):
    if ag.melhor_solucao.notas_jogadas[i] == 100:
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