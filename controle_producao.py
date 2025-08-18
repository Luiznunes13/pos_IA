# 🎯 Capacidades Técnicas:
# • Propor soluções efetivas para problemas computacionais.
# • Elaborar programas computacionais para resolução de problemas reais.
# • Compreender procedimentos e algoritmos em sistemas computacionais.
# • Utilizar dados estruturados em algoritmos e programas.
# • Aplicar estruturas de controle e modularização.
# 
# 🤝 Capacidades Socioemocionais:
# • Demonstrar postura proativa e adaptabilidade.
# • Dialogar com empatia e escuta ativa em ambientes profissionais.
# 
# 📚 Conhecimentos:
# 
# Programação
#  1.1. Padrões da linguagem
#  1.2. Ambientes de desenvolvimento
#  1.3. Estrutura de dados
#  1.4. Estruturas de decisão
#  1.5. Estruturas de repetição
# 
# Aplicações em Inteligência Artificial
#  2.1. Visão geral
#  2.2. Aplicações
# 
# 🎁 Conteúdo:
# Listas: criação, acesso, manipulação
# Tuplas: criação, acesso
# Dicionários: criação, acesso, manipulação
# Aplicações de listas, tuplas e dicionários em manufatura
# 
# 📌 Importância para o case:
# A manipulação de estruturas compostas permite representar dados industriais como registros de produção e parâmetros operacionais. O domínio dessas estruturas é essencial para a análise e automação de processos.
# 
# 📝 Atividade:
# 💼 Situação-Problema: Sistema de Controle de Produção
# A equipe de desenvolvimento de sistemas de uma fábrica que adota foi encarregada de criar um que permita registrar e analisar dados de peças produzidas durante um turno.
# 
# O sistema deve:
# 
# 1) Registrar os nomes das peças produzidas em uma lista.
# 2) Armazenar os limites de peso aceitáveis em uma tupla (mínimo e máximo).
# 3) Guardar em um dicionário o nome da peça como chave e uma lista com os pesos medidos como valor.
# 4) Solicitar também o material de cada peça produzida e armazenar os materiais únicos em um conjunto, ou seja, todos os tipos diferentes de materiais utilizados no turno, sem repetições.
# 5) Utilizar funções para:
# Coletar dados das peças (nome, peso, material).
# Classificar a peça como aprovada ou reprovada com base nos limites de peso da tupla.
# Exibir um relatório final com: quantidade de peças, lista completa de peças, quantidade de peças aprovadas e reprovadas e materiais únicos registrados.
# Sistema de Controle de Produção
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Função para coletar os dados das peças produzidas.
# 1) Registrar os nomes das peças produzidas em uma lista.
# 2) Armazenar os limites de peso aceitáveis em uma tupla (mínimo e máximo).
# 3) Guardar em um dicionário o nome da peça como chave e uma lista com os pesos medidos como valor.
# 4) Solicitar também o material de cada peça produzida e armazenar os materiais únicos em um conjunto.
def coletar_dados():
    """Coleta os dados das peças produzidas."""
    pecas = []
    limites_peso = (float(input("Digite o peso mínimo aceitável: ")), float(input("Digite o peso máximo aceitável: ")))
    dicionario_pesos = {}
    materiais_unicos = set()

    while True:
        nome = input("Digite o nome da peça (ou 'sair' para finalizar): ")
        if nome.lower() == 'sair':
            break
        pecas.append(nome)

        pesos = list(map(float, input(f"Digite os pesos medidos para a peça {nome}, separados por espaço: ").split()))
        dicionario_pesos[nome] = pesos

        material = input(f"Digite o material da peça {nome}: ")
        materiais_unicos.add(material)

    return pecas, limites_peso, dicionario_pesos, materiais_unicos

# Função para classificar as peças como aprovadas ou reprovadas.
# 5) Classificar a peça como aprovada ou reprovada com base nos limites de peso da tupla.
def classificar_pecas(dicionario_pesos, limites_peso):
    """Classifica as peças como aprovadas ou reprovadas com base nos limites de peso."""
    aprovadas = 0
    reprovadas = 0

    for nome, pesos in dicionario_pesos.items():
        for peso in pesos:
            if limites_peso[0] <= peso <= limites_peso[1]:
                aprovadas += 1
            else:
                reprovadas += 1

    return aprovadas, reprovadas

# Função para exibir o relatório final.
# 5) Exibir um relatório final com:
#    - Quantidade de peças.
#    - Lista completa de peças.
#    - Quantidade de peças aprovadas e reprovadas.
#    - Materiais únicos registrados.
def exibir_relatorio(pecas, aprovadas, reprovadas, materiais_unicos):
    """Exibe o relatório final."""
    print("\n--- Relatório Final ---")
    print(f"Quantidade total de peças: {len(pecas)}")
    print(f"Lista completa de peças: {', '.join(pecas)}")
    print(f"Quantidade de peças aprovadas: {aprovadas}")
    print(f"Quantidade de peças reprovadas: {reprovadas}")
    print(f"Materiais únicos registrados: {', '.join(materiais_unicos)}")

# Função principal que integra todas as funcionalidades do sistema.
def main():
    """Função principal do sistema."""
    pecas, limites_peso, dicionario_pesos, materiais_unicos = coletar_dados()
    aprovadas, reprovadas = classificar_pecas(dicionario_pesos, limites_peso)
    exibir_relatorio(pecas, aprovadas, reprovadas, materiais_unicos)

if __name__ == "__main__":
    main()
