import sys
import io
import os
import json
import openai
import pydub
import requests
import soundfile as sf
import speech_recognition as sr
from flask import Flask, jsonify, request

app = Flask(__name__)


# OpenAi API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Access token for your WhatsApp business account app
whatsapp_token = os.environ.get("WHATSAPP_TOKEN")

# Verify Token defined when configuring the webhook
verify_token = os.environ.get("VERIFY_TOKEN")

# Message log dictionary to enable conversation over multiple messages
message_log_dict = {}


# language for speech to text recoginition
# TODO: detect this automatically based on the user's language
LANGUGAGE = "en-US"


# get the media url from the media id
def get_media_url(media_id):
    '''headers = {
        "Authorization": f"Bearer {whatsapp_token}",
    }
    url = f"https://graph.facebook.com/v16.0/{media_id}/"
    response = requests.get(url, headers=headers)
    print(f"media id response: {response.json()}")
    return response.json()["url"]'''
    nopermite = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    return nopermite


# download the media file from the media url
def download_media_file(media_url):
    '''headers = {
        "Authorization": f"Bearer {whatsapp_token}",
    }
    response = requests.get(media_url, headers=headers)
    print(f"first 10 digits of the media file: {response.content[:10]}")
    return response.content'''
    nopermite = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    return nopermite


# convert ogg audio bytes to audio data which speechrecognition library can process
def convert_audio_bytes(audio_bytes):
    nopermite = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    return nopermite
    
    
    



# run speech recognition on the audio data
def recognize_audio(audio_bytes):
    recognizer = sr.Recognizer()
    audio_text = recognizer.recognize_google(audio_bytes, language=LANGUGAGE)
    return audio_text


# handle audio messages
def handle_audio_message(audio_id):
    audio_url = get_media_url(audio_id)
    audio_bytes = download_media_file(audio_url)
    #audio_data = convert_audio_bytes(audio_bytes)
    #audio_bytes = download_media_file(audio_url)
    audio_data = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    
    audio_text = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    message = audio_text
    return message


# send the response as a WhatsApp message back to the user
def send_whatsapp_message(body, message):
    value = body["entry"][0]["changes"][0]["value"]
    phone_number_id = value["metadata"]["phone_number_id"]
    from_number = value["messages"][0]["from"]
    
    url = "https://graph.facebook.com/v17.0/" + phone_number_id + "/messages"
        
    payload = json.dumps({
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": '54111523965421',
      "type": "text",
      "text": {
        "preview_url": False,
        "body": message
      }
    })
    headers = {
      'Content-Type': 'application/json',
      "Authorization": f"Bearer {whatsapp_token}",
    }
    
    response = requests.post(url, data=payload, headers=headers)
  
    response.raise_for_status()


# create a message log for each phone number and return the current message log

def update_message_log(message, phone_number, role):
    carta_del_restaurante = {
        "Asado": 3800,
        "Vacio": 3800,
        "Cuadril": 3800,
        "Mollejas": 3000,
        "Bebidas": 950,
    }

    platodeldia = {
        "Filet con Pure": 2500,
        "Lentejas": 2500,
        "Cuadril": 3500,
        "Mollejas": 3500,
        "Bebidas 1.5L": 950,
    }
    if message == 'Disculpe, no puedo procesar audios, escribeme un mensaje':
        prompt = message
    else:
        carta_formateada = "Concepto          Precio\n----------------            ----------\n"

        for concepto, precio in carta_del_restaurante.items():
            carta_formateada += f"{concepto:<18} ${precio:.2f}\n"
    
            platodeldia_formateada = "Concepto          Precio\n----------------            ----------\n"
        for concepto, precio in platodeldia.items():
            platodeldia_formateada += f"{concepto:<18} ${precio:.2f}\n"
            
        '''prompt = f"""
        Soy un asistente de la parrilla 'El Gran Retobao'. Si el cliente saluda pero no proporciona información relevante, responderé con:
    
    👋 "Hola, Bienvenido a El Gran Retobao. Hoy, el plato del día es {platodeldia_formateada}. Además, tenemos una carta de platos y precios que puedes consultar en cualquier momento: {carta_formateada}. Por favor, ten en cuenta que solo podemos servir los platos que están en nuestra carta."
    
    Mi objetivo principal es recolectar la siguiente información importante de tu parte:
    
    1) Dirección de entrega: [Por favor, proporciona tu dirección de entrega 🏠]
       Es esencial que nos des tu dirección de entrega para procesar tu pedido. No podremos continuar sin esta información.
    
    2) Lista de comidas y cantidades: [Por favor, indícame qué platos deseas y la cantidad de cada uno 🍔🍟]
       Necesitamos saber qué platos y cuántos de cada uno deseas pedir. Esto nos ayudará a calcular el precio total de tu pedido.
    
    Una vez que hayas proporcionado esta información, te proporcionaré un resumen de tu pedido:
    
    Resumen del Pedido:
    1) Dirección de Entrega: [Dirección proporcionada por el usuario 🏠]
    
    2) Detalle del Pedido:
       - [Cantidad] x [Comida] = [Calcular el total basado en la cantidad y el precio de la comida 💰]
       - [Cantidad] x [Comida] = [Calcular el total basado en la cantidad y el precio de la comida 💰]
       - [Cantidad] x [Comida] = [Calcular el total basado en la cantidad y el precio de la comida 💰]
    
       [Continuar con la lista de comidas y cantidades 🍔🍟]
    
    Total del Pedido: [Calcular el total basado en los precios de las comidas y las cantidades 💰]
    
    ¡Gracias por tu pedido! Tu comida estará lista en un plazo máximo de 45 minutos. Esperamos que disfrutes de tu experiencia con El Gran Retobao. 😊🍽️
    
    

    """  '''
   
    initial_log = {
        "role": "system",
        "content": f"Instrucciones iniciales para el Asistente Virtual de El Gran Retobao:\n\n- El asistente está configurado exclusivamente para ayudarte a realizar pedidos de comida en El Gran Retobao.\n\n- El objetivo principal es recopilar información para el pedido, que incluye la dirección de entrega y la lista de platos con cantidades.\n\n- Si el cliente solicita la carta de platodeldia, se le mostrará {platodeldia_formateada}. De lo contrario, no se mostrará de forma predeterminada.\n\n- El asistente no proporcionará respuestas a preguntas o temas no relacionados con el proceso de pedido de comida.\n\n- El asistente no confirmará el pedido hasta que se haya proporcionado la dirección de entrega.\n\nPor favor, comienza proporcionando los detalles necesarios para tu pedido. ¡Estamos aquí para ayudarte!\n\nLa carta de El Gran Retobao es la siguiente:\n\n{carta_formateada}"
    }




    if phone_number not in message_log_dict:
        message_log_dict[phone_number] = [initial_log]
    message_log = {"role": role, "content": message}
    message_log_dict[phone_number].append(message_log)
    return message_log_dict[phone_number]


# remove last message from log if OpenAI request fails
def remove_last_message_from_log(phone_number):
    message_log_dict[phone_number].pop()


# make request to OpenAI
def make_openai_request(message, from_number):
  
    try:
        message_log = update_message_log(message, from_number, "user")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_log,
            temperature=0.7,
        )
        response_message = response.choices[0].message.content
        print(f"openai response: {response_message}")
        update_message_log(response_message, from_number, "assistant")
    except Exception as e:
        print(f"openai error: {e}")
        response_message = "Sorry, the OpenAI API is currently overloaded or offline. Please try again later."
        remove_last_message_from_log(from_number)
    return response_message


# handle WhatsApp messages of different type
def handle_whatsapp_message(body):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    if message["type"] == "text":
        message_body = message["text"]["body"]
        response = make_openai_request(message_body, message["from"])
    else:
        response = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    
    send_whatsapp_message(body, response)


# handle incoming webhook messages
def handle_message(request):
    # Parse Request body in json format
    
    body = request.get_json()
    

    try:
        # info on WhatsApp text message payload:
        # https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
        if body.get("object"):
            if (
                body.get("entry")
                and body["entry"][0].get("changes")
                and body["entry"][0]["changes"][0].get("value")
                and body["entry"][0]["changes"][0]["value"].get("messages")
                and body["entry"][0]["changes"][0]["value"]["messages"][0]
            ):
                handle_whatsapp_message(body)
            return jsonify({"status": "ok"}), 200
        else:
            # if the request is not a WhatsApp API event, return an error
            return (
                jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
                404,
            )
    # catch all other errors and return an internal server error
    except Exception as e:
        print(f"unknown error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# Required webhook verifictaion for WhatsApp
# info on verification request payload:
# https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
def verify(request):
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == verify_token:
            # Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            print("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        print("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400


# Sets homepage endpoint and welcome message
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp OpenAI Webhook is listening!"


# Accepts POST and GET requests at /webhook endpoint
@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        
        return verify(request)
    elif request.method == "POST":
        
        return handle_message(request)


# Route to reset message log
@app.route("/reset", methods=["GET"])
def reset():
    global message_log_dict
    message_log_dict = {}
    return "Message log resetted!"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
