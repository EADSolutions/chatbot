# app.py
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import openai
from twilio.rest import Client

app = Flask(__name__)
openai.api_key = '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'  # Replace with your OpenAI API key

# Twilio credentials
account_sid = 'AC19a7d41d17c22f7c9506bea05a1760ad'
auth_token = 'f2efcabe13c4bbfb3c4716bb703a2ae6'
twilio_phone_number = '+18886955541'
your_phone_number = '7708765321'

twilio_client = Client(account_sid, auth_token)

@app.route('/sms-webhook', methods=['POST'])
def sms_webhook():
    incoming_message = request.form['Body']

    # Call the function to interact with ChatGPT
    chatbot_response = get_chatbot_response(incoming_message)

    # Send the chatbot response back to the user
    send_sms(chatbot_response, request.form['From'])

    return '', 200

def get_chatbot_response(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        max_tokens=150
    )
    return response['choices'][0]['text']

def send_sms(message, to_phone_number):
    # Use Twilio to send SMS
    twilio_client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to_phone_number
    )

if __name__ == '__main__':
    app.run(debug=True)
