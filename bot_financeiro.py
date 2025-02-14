import time
import pyautogui
import pyperclip
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configurar acesso ao Google Sheets (substitua 'seu_arquivo.json' pelo nome do arquivo JSON da API)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("seu_arquivo.json", scope)
client = gspread.authorize(creds)

# Abrir planilha e selecionar abas
planilha = client.open("Controle Financeiro WhatsApp")
despesas = planilha.worksheet("Despesas")

# Função para extrair comandos do WhatsApp
def ler_mensagem():
    pyautogui.click(100, 200)  # Clica na barra de mensagem do WhatsApp Web (ajuste as coordenadas conforme necessário)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    time.sleep(1)
    return pyperclip.paste().strip()

# Função para enviar mensagens no WhatsApp
def enviar_mensagem(texto):
    pyperclip.copy(texto)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

# Função para registrar gastos na planilha
def adicionar_gasto(mensagem):
    partes = mensagem.split()
    if len(partes) < 3:
        return "Formato inválido! Use: 'gastei VALOR no CATEGORIA'"
    
    valor = partes[1]
    categoria = partes[-1]
    descricao = " ".join(partes[2:-1])
    
    despesas.append_row([datetime.now().strftime("%d/%m/%Y"), categoria, descricao, valor])
    return f"✅ Gasto de R$ {valor} em {categoria} salvo com sucesso!"

# Função para calcular total do dia
def total_do_dia():
    registros = despesas.get_all_values()
    hoje = datetime.now().strftime("%d/%m/%Y")
    total = sum(float(row[3]) for row in registros if row[0] == hoje)
    return f"📊 Total gasto hoje: R$ {total:.2f}"

# Loop principal do bot (escaneia mensagens e responde automaticamente)
while True:
    mensagem = ler_mensagem().lower()
    
    if "gastei" in mensagem:
        resposta = adicionar_gasto(mensagem)
    elif "total do dia?" in mensagem:
        resposta = total_do_dia()
    else:
        resposta = "Comando não reconhecido. Use:\n1️⃣ 'gastei 50 no mercado'\n2️⃣ 'total do dia?'"

    enviar_mensagem(resposta)
    time.sleep(5)  # Aguarda antes de ler a próxima mensagem
