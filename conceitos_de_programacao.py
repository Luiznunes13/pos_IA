# entrada de dados

nome_peca = input("Nome da peça: ")
peso_medio_peca = float(input("Peso médio da peça (kg): "))
quantidade_pecas_produzidas = int(input("Quantidade de peças produzidas: "))
sensor = (input("Sensor de peso (ativo/inativo): "))

#calcular o peso total produzido naquela hora e exibir o resultado
peso_total = peso_medio_peca * quantidade_pecas_produzidas
print(f"Peso total produzido: {peso_total} kg")

#saídas 
print("Dados da peça:")
print(f"Nome da peça: {nome_peca} (tipo: {type(nome_peca).__name__})")
print(f"Peso médio da peça: {peso_medio_peca} (tipo: {type(peso_medio_peca).__name__})")
print(f"Quantidade de peças produzidas: {quantidade_pecas_produzidas} (tipo: {type(quantidade_pecas_produzidas).__name__})")
print(f"Sensor de peso ativo: {sensor} (tipo: {type(sensor).__name__})")