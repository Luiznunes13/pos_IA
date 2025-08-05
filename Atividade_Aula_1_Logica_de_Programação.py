# Solicita os dados ao usuário
nome_maquina = input("Nome da máquina: ")
tempo_operacao = float(input("Tempo de operação (horas): "))
potencia_media = float(input("Potência média (kW): "))

# Exibe o nome da máquina e seu tipo de dado
print(f"Nome da máquina: {nome_maquina} (tipo: {type(nome_maquina).__name__})")

# Calcula o consumo total de energia
consumo_total = potencia_media * tempo_operacao
print(f"Consumo total de energia no turno: {consumo_total} kWh")

# Exibe o tipo de dado de todas as variáveis
print("Tipos de dados das variáveis:")
print(f"nome_maquina: {type(nome_maquina).__name__}")
print(f"tempo_operacao: {type(tempo_operacao).__name__}")
print(f"potencia_media: {type(potencia_media).__name__}")
print(f"consumo_total: {type(consumo_total).__name__}")
