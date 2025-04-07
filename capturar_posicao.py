import pyautogui
import time
import json
import os

ARQUIVO = "posicoes.json"

if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r") as f:
        posicoes = json.load(f)
else:
    posicoes = {}

while True:
    nome = input("Digite um nome para essa posição (ou 'sair' para encerrar): ").strip()
    if nome.lower() == "sair":
        break

    print("Você tem 5 segundos para posicionar o mouse...")
    time.sleep(5)
    x, y = pyautogui.position()
    posicoes[nome] = [x, y]
    print(f"Posição '{nome}' capturada: ({x}, {y})\n")

    with open(ARQUIVO, "w") as f:
        json.dump(posicoes, f, indent=4)

print("Todas as posições foram salvas com sucesso.")
