import pandas as pd

# Criando uma Series a partir de uma lista
a = [1, 2, 3, 4, 5]
#print(a)

#colunas
serie_lista = pd.Series(a)
#print(serie_lista)

#acessando o índice
#print(serie_lista[4])

#creinado rotulo personalizado
serie_lista_rotulo = pd.Series(a, index=['a', 'b', 'c', 'd', 'e'])
#print(serie_lista_rotulo)
#print(serie_lista_rotulo['e'])


#criando uma Series a partir de um dicionário
dados = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
serie_dicionario = pd.Series(dados)
print(serie_dicionario)
print(serie_dicionario['d'])

#criando uma Series a partir de um dicionário com rótulos personalizados
dados = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
serie_dicionario = pd.Series(dados, index=['a', 'c', 'e'])
print(serie_dicionario)




#criando um DataFrame a partir de um dicionário
dados_dataframe = {
    "calorais": [420, 380, 390],
    "duracao" : [50, 40, 45]
}

df = pd.DataFrame(dados_dataframe)
print(df)
print(df.loc[1]) #acessando a primeira linha
print(df.loc[[0,1]]) #acessando a primeira e segunda linha
print(df.loc[0:2]) #acessando a segunda linha


#criando um DataFrame a partir de um dicionário com rótulos personalizados

dados_dataframe = pd.DataFrame(dados_dataframe, index=['dia1', 'dia2', 'dia3'])
print(dados_dataframe)
print(dados_dataframe.loc['dia2'])