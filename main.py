from flask import Flask, request
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

STORE_INFO = """
أنت مساعد ذكي لخدمة عملاء المتجر.
أجب على أسئلة العملاء بشكل مهذب واحترافي باللغة العربية.
إذا لم تعرف الإجابة قل للعميل أنك ستحول سؤاله للمسؤول.
"""

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.form
    message = data.get("Body", "")
    sender = data.get("From", "")
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=STORE_INFO,
        messages=[{"role": "user", "content": message}]
    )
    
    reply = response.content[0].text
    
    from twilio.twiml.messaging_response import MessagingResponse
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

@app.route("/")
def home():
    return "WhatsApp AI Agent is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
