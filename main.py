from flask import Flask, jsonify, request
import requests
import json


app = Flask(__name__)
#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    #SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "Retobao" and requests.args.get("hub.mode") == "suscribe":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
          return "Error de autentificacion."
    #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON


    data = request.data
    datos_serializados_str = data.decode('utf-8')
    
    
    mensaje = json.loads(datos_serializados_str)
    
    if 'body' in json.dumps(mensaje):


        

        
        mensaj = mensaje['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        print(mensaje)
        chatopenai.peticion(mensaj)
        print(mensaj)
        
        '''url = "https://graph.facebook.com/v17.0/137446296107512/messages"
        
        payload = json.dumps({
          "messaging_product": "whatsapp",
          "recipient_type": "individual",
          "to": "54111523965421",
          "type": "text",
          "text": {
            "preview_url": False,
            "body": mensaj
          }
        })
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer EAAVzJc6WKFUBOZCF0DldZBipUtdMbjZAqxFOptTQW6vXekWEr4O8Q5P8jKJkumX4NLMnXdAfjJWQzDZBdyoG8uj3kxXEqmTI4O8CkPnLPZAZCZBbP1kVCMpm8dHOhcWA2WBewkNCh4K18bJ2aB2MlHVzsBX39Oe3CzmRgLyX38LoxgJ6cVAPNiUtW00Xl2VqB5gRNwQhLjWTlsipZAEzvkRCvjGcu3gZD'
        }
        response = requests.post(url, data=payload, headers=headers)
        #response = requests.request("POST", url, headers=headers, data=payload)
    else:
        print(mensaje['entry'][0]['changes'][0]['value']['statuses'][0]['status'])
        print(mensaje)
      '''
        
    
        
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run()
