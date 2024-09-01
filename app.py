from flask import Flask, request, jsonify
from twilio.rest import Client
from googletrans import Translator
import os

app = Flask(__name__)

# Set up Twilio client
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Set up Google Translator
translator = Translator()

@app.route('/')
def index():
    return "Welcome to the Voice and Text Communication API!"

@app.route('/sms', methods=['POST'])
def sms_reply():
    """Respond to incoming SMS with a translated message."""
    incoming_message = request.form.get('Body')
    to_number = request.form.get('From')
    
    # Translate incoming message to English
    translated_message = translator.translate(incoming_message, dest='en').text

    # Send response
    response_message = f"Received and translated message: {translated_message}"
    client.messages.create(
        body=response_message,
        from_=TWILIO_PHONE_NUMBER,
        to=to_number
    )
    return jsonify({"status": "Message received and response sent"}), 200

@app.route('/call', methods=['POST'])
def call_reply():
    """Handle incoming voice calls and respond with a translation."""
    from_number = request.form.get('From')
    call_sid = request.form.get('CallSid')

    # Respond with a simple message
    response_message = "Your call has been received and will be processed shortly."

    call = client.calls(call_sid).update(
        twiml=f"<Response><Say>{response_message}</Say></Response>"
    )

    return jsonify({"status": "Call response updated"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
