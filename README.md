### Autores do projeto 

- Wallysson Sousa 
- Luan Barros

# Assistente Virtual Automatizado

Projeto em Python que executa tarefas automáticas simulando ações humanas como clicar, digitar e esperar. As instruções vêm de um arquivo `.csv` e são executadas com `pyautogui`.

## Funcionalidades

- Leitura de tarefas via `tarefas.csv`
- Execução de ações: `click`, `texto`, `tecla`, `espera`
- Posições mapeadas com `capturar_posicoes.py`
- Relatório gerado automaticamente em Excel

## Arquivos

- `ass_virtual.py` → script principal
- `tarefas.csv` → lista de tarefas
- `posicoes.json` → posições dos cliques
- `relatorio_execucao_*.xlsx` → relatório gerado
- `capturar_posicoes.py` → captura coordenadas do mouse

## Como usar

1. Execute `capturar_posicoes.py` para mapear posições na tela
2. Edite `tarefas.csv` com suas ações
3. Execute `ass_virtual.py` para rodar o assistente

## Requisitos

Instale com:

```bash
pip install pyautogui pandas openpyxl colorama
