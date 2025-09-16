import csv #biblioteca para manipulação de arquivos CSV

with open('sensores.csv', mode='w',newline='') as arquivo: #criar um arquivo CSV
    escritor = csv.writer(arquivo) #criar um objeto escritor CSV
    escritor.writerow(['sensor','data','temperatura','pressao']) #escrever o cabeçalho

    escritor.writerow(['1','2023-01-01','96','1012']) #escrever dados
    escritor.writerow(['2','2023-01-02','53','1013']) #escrever dados
    escritor.writerow(['3','2023-01-03','54','1011']) #escrever dados
    escritor.writerow(['4','2023-01-04','51','1010']) #escrever dados
    escritor.writerow(['5','2023-01-05','49','1009']) #escrever dados
    
  
        
#gera o arquivo CSV com dados de produção
#from random import randint #biblioteca para gerar números aleatórios


with open('sensores.csv',mode='r') as arquivo: #abrir o arquivo CSV para leitura
    leitor = csv.reader(arquivo) #criar um objeto leitor CSV
    next(leitor) #pular o cabeçalho

    for linha in leitor: #percorrer as linhas do arquivo
        if int(linha[2]) >= 50: #se a temperatura for maior que 50
            print(linha) #imprimir a linha



