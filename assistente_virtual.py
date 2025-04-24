import time
import pyautogui
import pandas as pd
from openpyxl import Workbook
import json
from datetime import datetime
import os

pyautogui.PAUSE = 0.7
pyautogui.FAILSAFE = True

ARQUIVO_TAREFAS = 'data/tarefas.csv'
ARQUIVO_POSICOES = 'data/posicoes.json'
DIRETORIO_RELATORIO = 'output'

def carregar_posicoes():
    try:
        with open(ARQUIVO_POSICOES, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Arquivo de posições não encontrado.")
        return {}

def realizar_clique(nome, posicoes):
    if nome in posicoes:
        x, y = posicoes[nome]
        pyautogui.click(x, y)
    else:
        raise Exception(f"Posição '{nome}' não encontrada.")


def executar_tarefas(caminho_csv):
    df = pd.read_csv(caminho_csv)
    relatorio = []
    posicoes = carregar_posicoes()

    for _, linha in df.iterrows():
        inicio = time.time()
        tarefa = linha['tarefa']
        tipo = linha['tipo']
        dado = str(linha['dado'])
        status = "Sucesso"

        try:
            if tipo == 'click':
                realizar_clique(dado, posicoes)
            elif tipo == 'texto':
                pyautogui.write(dado)
            elif tipo == 'tecla':
                pyautogui.press(dado)
            elif tipo == 'espera':
                time.sleep(float(dado))
            else:
                raise Exception("Tipo de ação desconhecido.")
        except Exception as e:
            status = f"Erro: {str(e)}"

        duracao = round(time.time() - inicio, 2)
        relatorio.append([tarefa, tipo, dado, status, duracao])

    gerar_relatorio_excel(relatorio)


def gerar_relatorio_excel(relatorio):
    os.makedirs(DIRETORIO_RELATORIO, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Relatório de Execução"

    ws.append(["Tarefa", "Tipo", "Dado", "Status", "Tempo (s)"])
    for linha in relatorio:
        ws.append(linha)

    nome_arquivo = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    caminho_completo = os.path.join(DIRETORIO_RELATORIO, nome_arquivo)
    wb.save(caminho_completo)

# Execução principal
if __name__ == "__main__":
    print("🍎 Iniciando Assistente Virtual...")
    executar_tarefas(ARQUIVO_TAREFAS)
    print("✅ Execução finalizada com sucesso. Relatório salvo na pasta '/output'.")
