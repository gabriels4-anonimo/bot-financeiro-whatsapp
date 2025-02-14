from twilio.rest import Client
from flask import Flask, request

app = Flask(__name__)

# Credenciais do Twilio
ACCOUNT_SID = "SEU_TWILIO_SID"
AUTH_TOKEN = "SEU_TWILIO_AUTH_TOKEN"
TWILIO_NUMBER = "whatsapp:+14155238886"  # Número do Twilio (pode ser diferente)

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Rota para receber mensagens
@app.route("/bot", methods=["POST"])
def whatsapp_bot():
    msg = request.form.get("Body").lower()
    sender = request.form.get("From")

    if "gastei" in msg:
        response = f"✅ Gasto registrado: {msg}"
    elif "total do dia?" in msg:
        response = "📊 Você gastou R$ 150,00 hoje."  # Aqui vamos conectar com um banco de dados depois
    else:
        response = "Comando não reconhecido. Use:\n1️⃣ 'Gastei 50 no mercado'\n2️⃣ 'Total do dia?'"

    client.messages.create(
        from_=TWILIO_NUMBER,
        body=response,
        to=sender
    )

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

