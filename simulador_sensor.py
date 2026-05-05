

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         SIMULADOR DE SENSOR INDUSTRIAL — TECELAGEM                         ║
║         Frameworks para Big Data — SENAI-SP                                 ║
║         Pós-Graduação Lato Sensu em Inteligência Artificial                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

DESCRIÇÃO
---------
Simula telemetria de teares (powerlooms) de uma indústria têxtil com 6 máquinas
em 3 linhas de produção. Gera dados realistas com variações por turno, por
equipamento e por tipo de tecido, incluindo chaves de integração (batch_id e
roll_number) que permitem correlacionar os dados IoT com sistemas de inspeção
de qualidade do tecido.

Inclui problemas de qualidade intencionais para o laboratório da Aula 9.

MODOS DE USO
------------
1. BATCH  — gera um arquivo CSV com histórico volumoso (usado nas Aulas 2, 7, 8, 9)
2. STREAM — publica mensagens JSON em tempo real no Azure Event Hubs (Aulas 5, 6)

PRÉ-REQUISITOS
--------------
    pip install azure-eventhub

COMO EXECUTAR
-------------
    # Modo batch — gera 500.000 registros limpos em CSV
    python simulador_sensor.py --modo batch --registros 500000 --saida dados_tecelagem.csv

    # Modo batch com problemas de qualidade (para Aula 9)
    python simulador_sensor.py --modo batch --registros 100000 --saida dados_ruim.csv --qualidade ruim

    # Modo streaming — publica no Event Hubs indefinidamente
    python simulador_sensor.py --modo stream --conexao "SEU_CONNECTION_STRING" --hub "nome-do-hub"

    # Modo streaming com intervalo personalizado (default: 2 segundos)
    python simulador_sensor.py --modo stream --conexao "SEU_CONNECTION_STRING" --hub "nome-do-hub" --intervalo 1

ESTRUTURA DO DADO GERADO
-------------------------
{
    "timestamp":         "2025-03-10T19:32:45",   # data e hora da telemetria
    "tear_id":           "POWERLOOM-03",           # identificador da máquina (Tear)
    "linha":             "Linha-B",                # linha de produção
    "turno":             "Morning",                # Morning / Evening / Night
    "batch_id":          898423,                   # CHAVE DE INTEGRAÇÃO (Lote do tecido)
    "roll_number":       363,                      # CHAVE DE INTEGRAÇÃO (Rolo do tecido)
    "fabric_type":       "polyester",              # polyester / silk / cotton / linen
    "temperatura":       28.1,                     # °C — faixa normal: 20–40
    "umidade":           67.8,                     # % — faixa normal: 50–80
    "vibracao":          2.1,                      # mm/s — métrica IoT para IA prever falhas
    "velocidade_rpm":    1420,                     # RPM — métrica IoT para IA
    "metros_produzidos": 47,                       # metros de tecido no ciclo
    "status":            "operando"                # operando / alerta / parado
}
"""

import argparse
import json
import random
import time
import csv
import sys
from datetime import datetime, timedelta


# ─── CONFIGURAÇÕES DO CENÁRIO TÊXTIL ─────────────────────────────────────────

TEARES = ["POWERLOOM-01", "POWERLOOM-02", "POWERLOOM-03",
          "POWERLOOM-04", "POWERLOOM-05", "POWERLOOM-06"]

LINHAS = ["Linha-A", "Linha-B", "Linha-C"]

TURNOS = ["Morning", "Evening", "Night"]

FABRIC_TYPES = ["polyester", "silk", "cotton", "linen"]

# Mapeamento tear → linha (fixo durante toda a simulação)
TEAR_LINHA = {
    "POWERLOOM-01": "Linha-A",
    "POWERLOOM-02": "Linha-A",
    "POWERLOOM-03": "Linha-B",
    "POWERLOOM-04": "Linha-B",
    "POWERLOOM-05": "Linha-C",
    "POWERLOOM-06": "Linha-C",
}

# Tipo de tecido predominante por tear (cada tear é especializado)
TEAR_FABRIC = {
    "POWERLOOM-01": "cotton",
    "POWERLOOM-02": "cotton",
    "POWERLOOM-03": "polyester",   # mais crítico — maior vibração
    "POWERLOOM-04": "polyester",
    "POWERLOOM-05": "silk",
    "POWERLOOM-06": "linen",
}

# Perfil de cada tear: base de temperatura, vibração e tendência a falha
# Temperatura em teares têxteis: ambiente + aquecimento do motor (20–40°C)
# Umidade: crítica para qualidade do fio (50–80%)
PERFIL_TEAR = {
    "POWERLOOM-01": {"temp_base": 26, "umidade_base": 62, "vibracao_base": 1.2, "rpm_base": 1350},
    "POWERLOOM-02": {"temp_base": 27, "umidade_base": 65, "vibracao_base": 1.5, "rpm_base": 1380},
    "POWERLOOM-03": {"temp_base": 32, "umidade_base": 70, "vibracao_base": 2.5, "rpm_base": 1420},  # mais crítico
    "POWERLOOM-04": {"temp_base": 29, "umidade_base": 68, "vibracao_base": 1.8, "rpm_base": 1400},
    "POWERLOOM-05": {"temp_base": 25, "umidade_base": 72, "vibracao_base": 1.0, "rpm_base": 1300},  # silk: mais lento
    "POWERLOOM-06": {"temp_base": 28, "umidade_base": 60, "vibracao_base": 1.6, "rpm_base": 1360},
}

# Fator de variação por turno
# Night = operadores mais cansados = mais alertas, menor produção
FATOR_TURNO = {
    "Morning": {"producao": 1.0,  "anomalia": 1.0},
    "Evening": {"producao": 0.95, "anomalia": 1.1},
    "Night":   {"producao": 0.85, "anomalia": 1.5},
}

# Contadores de lote e rolo — incrementam ao longo da simulação
_batch_counter = 800000
_roll_counter  = 100


def _proximo_batch():
    """Retorna um novo batch_id incrementando o contador global."""
    global _batch_counter
    _batch_counter += random.randint(1, 3)
    return _batch_counter


def _proximo_roll():
    """Retorna um novo roll_number incrementando o contador global."""
    global _roll_counter
    _roll_counter += 1
    return _roll_counter


# ─── GERADOR DE LEITURA ───────────────────────────────────────────────────────

# Mantém estado de lote e rolo por tear entre chamadas consecutivas
_estado_tear = {t: {"batch_id": _proximo_batch(), "roll_number": _proximo_roll(),
                    "metros_acumulados": 0}
                for t in TEARES}


def gerar_leitura(timestamp, tear_id, qualidade="boa"):
    """
    Gera uma leitura realista de telemetria para um tear e timestamp.

    Parâmetros:
        timestamp (datetime): momento da leitura
        tear_id   (str):      identificador do tear
        qualidade (str):      'boa' (dados limpos) ou 'ruim' (com problemas)

    Retorna:
        dict com os campos do sensor ou None (para simular perda de pacote)
    """
    perfil = PERFIL_TEAR[tear_id]
    hora   = timestamp.hour

    # Turno alinhado com inspection_shift do sistema de qualidade
    if 6 <= hora < 14:
        turno = "Morning"
    elif 14 <= hora < 22:
        turno = "Evening"
    else:
        turno = "Night"

    fator = FATOR_TURNO[turno]

    # ── Temperatura ambiente + aquecimento do motor ───────────────────────────
    # Faixa normal: 20–40°C; picos de até 45°C em sobrecarga
    temperatura = round(
        perfil["temp_base"]
        + random.gauss(0, 2.0)
        + (random.uniform(4, 10) if random.random() < 0.03 else 0),
        1
    )

    # ── Umidade relativa do ar ────────────────────────────────────────────────
    # Crítica para o fio: abaixo de 50% = quebra; acima de 80% = mofo
    umidade = round(
        perfil["umidade_base"]
        + random.gauss(0, 3.0)
        + (random.uniform(8, 15) if random.random() < 0.02 else 0),
        1
    )
    umidade = max(30.0, min(95.0, umidade))  # limitar a faixa física plausível

    # ── Vibração ──────────────────────────────────────────────────────────────
    vibracao = round(
        perfil["vibracao_base"]
        + random.gauss(0, 0.15)
        + (random.uniform(1.2, 2.5) if random.random() < 0.02 else 0),
        2
    )

    # ── RPM — varia com o turno e com o tipo de tecido ────────────────────────
    velocidade_rpm = int(
        random.gauss(perfil["rpm_base"] * fator["producao"], 40)
    )

    # ── Metros produzidos no ciclo ────────────────────────────────────────────
    metros_producao_base = 40 if TEAR_FABRIC[tear_id] == "silk" else 50
    metros_produzidos = max(0, int(
        random.gauss(metros_producao_base * fator["producao"], 4)
    ))

    # ── Gestão de lote e rolo ─────────────────────────────────────────────────
    estado = _estado_tear[tear_id]
    estado["metros_acumulados"] += metros_produzidos

    # Novo rolo a cada ~500 metros; novo lote a cada ~5 rolos
    if estado["metros_acumulados"] >= 500:
        estado["metros_acumulados"] = 0
        estado["roll_number"] = _proximo_roll()
        if estado["roll_number"] % 5 == 0:
            estado["batch_id"] = _proximo_batch()

    # ── Status baseado em temperatura, umidade e vibração ────────────────────
    if temperatura > 38 or vibracao > 3.0 or umidade > 82:
        status = "alerta"
    elif temperatura > 43 or vibracao > 4.0 or umidade > 88:
        status = "parado"
    else:
        status = "operando"

    leitura = {
        "timestamp":         timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
        "tear_id":           tear_id,
        "linha":             TEAR_LINHA[tear_id],
        "turno":             turno,
        "batch_id":          estado["batch_id"],
        "roll_number":       estado["roll_number"],
        "fabric_type":       TEAR_FABRIC[tear_id],
        "temperatura":       temperatura,
        "umidade":           umidade,
        "vibracao":          vibracao,
        "velocidade_rpm":    velocidade_rpm,
        "metros_produzidos": metros_produzidos,
        "status":            status,
    }

    # ── PROBLEMAS DE QUALIDADE INTENCIONAIS (modo 'ruim') ────────────────────
    # Usados na Aula 9 para laboratório de validação de dados.
    # Cada tipo de problema tem probabilidade baixa para ser realista.

    if qualidade == "ruim":

        # 1. Perda de pacote: sensor sem transmissão (2% das vezes)
        if random.random() < 0.02:
            return None

        # 2. Temperatura nula: sensor desconectado (1.5%)
        if random.random() < 0.015:
            leitura["temperatura"] = None

        # 3. Temperatura absurda: sensor com defeito físico (0.8%)
        if random.random() < 0.008:
            leitura["temperatura"] = round(random.uniform(-30, 300), 1)

        # 4. Umidade negativa: erro de calibração (0.6%)
        if random.random() < 0.006:
            leitura["umidade"] = round(random.uniform(-10, -0.1), 1)

        # 5. RPM negativo: erro de sinal (0.5%)
        if random.random() < 0.005:
            leitura["velocidade_rpm"] = -leitura["velocidade_rpm"]

        # 6. Status inválido: valor fora do domínio (0.4%)
        if random.random() < 0.004:
            leitura["status"] = random.choice(["ERRO", "N/A", "unknown", ""])

        # 7. tear_id inválido: ID corrompido (0.2%)
        if random.random() < 0.002:
            leitura["tear_id"] = "POWERLOOM-99"

        # 8. fabric_type inválido: valor fora do domínio (0.3%)
        if random.random() < 0.003:
            leitura["fabric_type"] = random.choice(["UNKNOWN", "N/A", "123", ""])

        # 9. batch_id nulo: falha de integração com sistema de lote (0.4%)
        if random.random() < 0.004:
            leitura["batch_id"] = None

    return leitura


# ─── MODO BATCH ───────────────────────────────────────────────────────────────

def modo_batch(n_registros, arquivo_saida, qualidade):
    """
    Gera um arquivo CSV com n_registros de leituras históricas.
    Os dados cobrem os últimos 6 meses, com leituras a cada 30 segundos por tear.

    Parâmetros:
        n_registros   (int): número total de registros a gerar
        arquivo_saida (str): caminho do arquivo CSV de saída
        qualidade     (str): 'boa' ou 'ruim'
    """
    print(f"\n{'='*60}")
    print(f"  SIMULADOR TÊXTIL — MODO BATCH")
    print(f"  Registros solicitados : {n_registros:,}")
    print(f"  Arquivo de saída      : {arquivo_saida}")
    print(f"  Qualidade dos dados   : {qualidade}")
    print(f"{'='*60}\n")

    data_fim    = datetime.now()
    data_inicio = data_fim - timedelta(days=180)
    intervalo_segundos = 30

    campos = [
        "timestamp", "tear_id", "linha", "turno",
        "batch_id", "roll_number", "fabric_type",
        "temperatura", "umidade", "vibracao", "velocidade_rpm",
        "metros_produzidos", "status"
    ]

    registros_gerados    = 0
    registros_rejeitados = 0

    with open(arquivo_saida, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

        ts_atual = data_inicio
        while registros_gerados < n_registros and ts_atual <= data_fim:

            for tear in TEARES:
                if registros_gerados >= n_registros:
                    break

                leitura = gerar_leitura(ts_atual, tear, qualidade)

                if leitura is None:
                    registros_rejeitados += 1
                    continue

                writer.writerow(leitura)
                registros_gerados += 1

                if registros_gerados % 50000 == 0:
                    pct = registros_gerados / n_registros * 100
                    print(f"  Progresso: {registros_gerados:>8,} / {n_registros:,}  ({pct:.1f}%)")

            ts_atual += timedelta(seconds=intervalo_segundos)

    print(f"\n  ✅ Concluído!")
    print(f"  Registros gerados   : {registros_gerados:,}")
    if qualidade == "ruim":
        print(f"  Pacotes perdidos    : {registros_rejeitados:,}  (nulos intencionais)")
    print(f"  Arquivo             : {arquivo_saida}")
    print(f"  Período coberto     : {data_inicio.strftime('%d/%m/%Y')} → {data_fim.strftime('%d/%m/%Y')}")
    print(f"\n  Faça o upload deste arquivo para a zona raw do seu ADLS Gen2.")
    print(f"{'='*60}\n")


# ─── MODO STREAMING ───────────────────────────────────────────────────────────

def modo_stream(connection_string, hub_name, intervalo_segundos):
    """
    Publica mensagens JSON em tempo real no Azure Event Hubs.
    Simula telemetria contínua de todos os teares.

    Parâmetros:
        connection_string  (str):   connection string do Event Hubs namespace
        hub_name           (str):   nome do hub (event hub)
        intervalo_segundos (float): intervalo entre lotes de leituras
    """
    try:
        from azure.eventhub import EventHubProducerClient, EventData
    except ImportError:
        print("\n  ERRO: Instale o SDK do Azure Event Hubs:")
        print("  pip install azure-eventhub\n")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  SIMULADOR TÊXTIL — MODO STREAMING")
    print(f"  Hub            : {hub_name}")
    print(f"  Intervalo      : {intervalo_segundos}s entre lotes")
    print(f"  Teares         : {', '.join(TEARES)}")
    print(f"  Pressione Ctrl+C para encerrar.")
    print(f"{'='*60}\n")

    producer = EventHubProducerClient.from_connection_string(
        conn_str=connection_string,
        eventhub_name=hub_name
    )

    total_publicadas = 0

    try:
        while True:
            ts_atual = datetime.now()
            lote     = producer.create_batch()
            leituras_no_lote = 0

            for tear in TEARES:
                leitura = gerar_leitura(ts_atual, tear, qualidade="boa")
                if leitura:
                    lote.add(EventData(json.dumps(leitura, ensure_ascii=False)))
                    leituras_no_lote += 1

            producer.send_batch(lote)
            total_publicadas += leituras_no_lote

            print(
                f"  [{ts_atual.strftime('%H:%M:%S')}] "
                f"{leituras_no_lote} mensagens publicadas | "
                f"Total: {total_publicadas:,}"
            )

            time.sleep(intervalo_segundos)

    except KeyboardInterrupt:
        print(f"\n\n  ⏹  Encerrado pelo usuário.")
        print(f"  Total de mensagens publicadas: {total_publicadas:,}")
    finally:
        producer.close()
        print(f"{'='*60}\n")


# ─── INTERFACE DE LINHA DE COMANDO ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Simulador de telemetria têxtil — SENAI Big Data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Gera 500.000 registros limpos em CSV
  python simulador_sensor.py --modo batch --registros 500000 --saida dados_tecelagem.csv

  # Gera 100.000 registros COM problemas de qualidade (Aula 9)
  python simulador_sensor.py --modo batch --registros 100000 --saida dados_ruim.csv --qualidade ruim

  # Publica em tempo real no Event Hubs
  python simulador_sensor.py --modo stream --conexao "Endpoint=sb://..." --hub teares-telemetria

  # Publica a cada 1 segundo
  python simulador_sensor.py --modo stream --conexao "Endpoint=sb://..." --hub teares-telemetria --intervalo 1
        """
    )

    parser.add_argument(
        "--modo",
        choices=["batch", "stream"],
        required=True,
        help="'batch' para gerar CSV histórico | 'stream' para publicar no Event Hubs"
    )
    parser.add_argument(
        "--registros",
        type=int,
        default=500000,
        help="Número de registros para o modo batch (default: 500000)"
    )
    parser.add_argument(
        "--saida",
        type=str,
        default="dados_tecelagem.csv",
        help="Nome do arquivo CSV de saída (modo batch)"
    )
    parser.add_argument(
        "--qualidade",
        choices=["boa", "ruim"],
        default="boa",
        help="'boa' para dados limpos | 'ruim' para dados com problemas intencionais (Aula 9)"
    )
    parser.add_argument(
        "--conexao",
        type=str,
        default="",
        help="Connection string do Azure Event Hubs namespace (modo stream)"
    )
    parser.add_argument(
        "--hub",
        type=str,
        default="teares-telemetria",
        help="Nome do Event Hub (modo stream)"
    )
    parser.add_argument(
        "--intervalo",
        type=float,
        default=2.0,
        help="Intervalo em segundos entre lotes no modo stream (default: 2.0)"
    )

    args = parser.parse_args()

    if args.modo == "batch":
        modo_batch(args.registros, args.saida, args.qualidade)
    elif args.modo == "stream":
        if not args.conexao:
            print("\n  ERRO: Informe a connection string do Event Hubs com --conexao\n")
            parser.print_help()
            sys.exit(1)
        modo_stream(args.conexao, args.hub, args.intervalo)


if __name__ == "__main__":
    main()