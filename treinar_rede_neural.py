import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

f = open('base_treino.txt', 'r')
table = []
for line in f:
    linha = line.split()
    linha[0] = float(linha[0])
    linha[1] = float(linha[1])
    linha[2] = int(linha[2])
    table.append(linha)
f.close()
df = pd.DataFrame(data=table, columns=['x_ball','x_raquete','Movimento'])
moviment = pd.get_dummies(df['Movimento'],drop_first=False)
df.drop(['Movimento'],axis=1,inplace=True)
df = pd.concat([df,moviment], axis=1)
print(df.head())
df.columns = ['x_ball','x_raquete','Left','No_Move','Right']
'''x_ball = np.asarray(df['x_ball'])
x_raquete = np.asarray(df['x_raquete'])
no_move = np.asarray(df['No_Move'])
right = np.asarray(df['Right'])'''
previsores = df.iloc[:, 0:2].values
classe_dummy = df.iloc[:, 2::].values
previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = train_test_split(previsores, classe_dummy, test_size=0.25)

classificador = Sequential()
classificador.add(Dense(units = 10, activation = 'sigmoid', input_dim = 2))
classificador.add(Dense(units = 30, activation = 'sigmoid'))
classificador.add(Dense(units = 3, activation = 'softmax'))
classificador.compile(optimizer = 'adam', loss = 'categorical_crossentropy',
                      metrics = ['categorical_accuracy'])
classificador.fit(previsores_treinamento, classe_treinamento, batch_size = 10,
                  epochs = 1000)

resultado = classificador.evaluate(previsores_teste, classe_teste)
previsoes = classificador.predict(previsores_teste)
#print(previsoes)
classe_teste2 = [np.argmax(t) for t in classe_teste]
previsoes2 = [np.argmax(t) for t in previsoes]
previsoes3 = []
for i in range(len(previsoes2)):
    
    
    previsoes3.append([0,0,0])
    previsoes3[i][previsoes2[i]] = 1
from sklearn.metrics import confusion_matrix,classification_report
matriz = confusion_matrix(previsoes2, classe_teste2)
print(classification_report(previsoes2, classe_teste2))
print(str(matriz))