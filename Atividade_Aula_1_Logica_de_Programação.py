# 🎁 Conteúdo:
# Entenda o que é programação
# Dê os primeiros passos com Python
# Estude boas práticas desde o começo
# Preparação de ambiente
# Manufatura Inteligente
#
# 📌 Importância para o case:
# Introduz conceitos fundamentais de programação com Python, permitindo que os alunos comecem a desenvolver scripts básicos e compreendam a estrutura dos códigos utilizados em projetos de IA e manufatura inteligente.
#
# 📝 Atividade:
# 💼 Situação-Problema: Controle de Consumo Energético de Máquinas Industriais
# Uma fábrica inteligente deseja iniciar o controle do consumo energético das máquinas utilizadas durante os turnos de trabalho. Ao final de cada turno (manhã, tarde ou noite), o operador deve registrar as seguintes informações:
# Nome da máquina que operou (ex: “Prensa Hidráulica A1”)
# Tempo de operação da máquina no turno (em horas, ex: 6.5)
# Potência média consumida pela máquina durante o turno (em kW, ex: 12.4)
# Com base nesses dados, o sistema precisa:
# Exibir o nome da máquina e o tipo de dado correspondente.
# Calcular e exibir o consumo total de energia no turno, utilizando a fórmula: consumo total = potência média × horas de operação
# Exibir o tipo de dado de todas as variáveis utilizadas no sistema.

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

