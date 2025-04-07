import pyautogui  # type: ignore
import pandas as pd
import time
import json
from datetime import datetime
from openpyxl import Workbook
from colorama import Fore, Style, init

init(autoreset=True)

# Carregar posições salvas
try:
    with open("posicoes.json", "r") as f:
        posicoes_mapeadas = json.load(f)
except:
    posicoes_mapeadas = {}

def clicar(nome):
    if nome in posicoes_mapeadas:
        x, y = posicoes_mapeadas[nome]
        pyautogui.click(x, y)
        return True, f"Clique em '{nome}'"
    return False, f"Erro: posição '{nome}' não encontrada"

def digitar(texto):
    pyautogui.write(texto)
    return True, f"Digitou: '{texto}'"

def pressionar(tecla):
    pyautogui.press(tecla)
    return True, f"Tecla '{tecla}' pressionada"

def esperar(segundos):
    try:
        segundos = float(segundos)
        time.sleep(segundos)
        return True, f"Aguardou {segundos} segundos"
    except:
        return False, "Erro ao tentar esperar"

def executar_tarefa(tarefa, tipo, dado):
    inicio = time.time()
    try:
        if tipo == "click":
            status, msg = clicar(dado)
        elif tipo == "texto":
            status, msg = digitar(dado)
        elif tipo == "tecla":
            status, msg = pressionar(dado)
        elif tipo == "espera":
            status, msg = esperar(dado)
        else:
            tempo = round(time.time() - inicio, 2)
            return {
                "Tarefa": tarefa,
                "Status": "Tipo inválido",
                "Mensagem": tipo,
                "Tempo (s)": tempo,
            }

        tempo = round(time.time() - inicio, 2)
        return {
            "Tarefa": tarefa,
            "Status": "Sucesso" if status else "Falha",
            "Mensagem": msg,
            "Tempo (s)": tempo,
        }
    except Exception as e:
        tempo = round(time.time() - inicio, 2)
        return {
            "Tarefa": tarefa,
            "Status": "Erro",
            "Mensagem": str(e),
            "Tempo (s)": tempo,
        }

def gerar_relatorio(resultados):
    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"relatorio_execucao_{data}.xlsx"
    df = pd.DataFrame(resultados)
    df.to_excel(nome_arquivo, index=False)
    print(Fore.GREEN + f"Relatório salvo como: {nome_arquivo}")

def introducao():
    print(Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + "ASSISTENTE VIRTUAL AUTOMATIZADO")
    print(Fore.CYAN + "=" * 50)
    print("Lendo tarefas de 'tarefas.csv'")
    print("Iniciando em:")
    for i in range(5, 0, -1):
        print(f"{i} segundos...", end="\r")
        time.sleep(1)
    print("\nComeçando!\n")

def main():
    introducao()
    try:
        tarefas = pd.read_csv("tarefas.csv")
    except Exception as e:
        print(Fore.RED + f"Erro ao abrir 'tarefas.csv': {e}")
        return

    resultados = []

    for _, linha in tarefas.iterrows():
        print(Fore.BLUE + f"{linha['Tarefa']}")
        resultado = executar_tarefa(linha['Tarefa'], linha['Tipo'], linha['Dado'])
        status_cor = Fore.GREEN if resultado['Status'] == "Sucesso" else Fore.RED
        print(f" {status_cor}{resultado['Mensagem']} [{resultado['Status']}]")
        resultados.append(resultado)

    gerar_relatorio(resultados)
    print(Fore.CYAN + "Execução finalizada.")

if __name__ == "__main__":
    main()
