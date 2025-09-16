import csv #biblioteca para manipulação de arquivos CSV

with open('producao.csv', mode='w',newline='') as arquivo: #criar um arquivo CSV
    escritor = csv.writer(arquivo) #criar um objeto escritor CSV
    escritor.writerow(['Maquina', 'Turno', 'Produzido']) #escrever o cabeçalho
    escritor.writerow(['M1', 'Manha',250])
    escritor.writerow(['M1', 'Tarde',300])
        
#gera o arquivo CSV com dados de produção
#from random import randint #biblioteca para gerar números aleatórios


with open('producao.csv',mode='r') as arquivo: #abrir o arquivo CSV para leitura
    leitor = csv.reader(arquivo) #criar um objeto leitor CSV

    for linha in leitor: #percorrer as linhas do arquivo
        print(linha) #imprimir a linha
        