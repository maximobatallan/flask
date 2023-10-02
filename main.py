from flask import Flask, jsonify, request
import requests
import json
import chatopenai

app = Flask(__name__)


def peticion(mensaje):

    openai.api_key = "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"

    carta_del_restaurante = {
        "Asado": 10.99,
        "Vacio": 12.99,
        "Cuadril": 9.99,
        "Mollejas": 6.99,
    }



    prompt = """
    Sos un asistente de la parrilla 'El Gran Retobao':

    Aquí tienes la carta del restaurante con los precios:

    {carta_del_restaurante}


    tu objetivo es recolectar del cliente la siguiente informacion:

    1) Dirección de entrega:

    2) Lista de comidas y cantidades (por ejemplo, "2 hamburguesas, 1 pizza, 3 refrescos"):


    Al finalizar brindaras un Resumen del Pedido:
    1) Dirección de Entrega: [Dirección proporcionada por el usuario]
    2) Detalle:
    - [Cantidad] x [Comida] = [Precio] x [Cantidad]
    - [Cantidad] x [Comida] = [Precio] x [Cantidad]
    - [Cantidad] x [Comida] = [Precio] x [Cantidad]
    [Continuar con la lista de comidas y cantidades]

    Total del Pedido: [Calcular el total basado en los precios de las comidas y las cantidades]

    ¡Muchas gracias su pedido estara listo dentro de los 45 minutos!

    """

    context = {"role": "system",
                "content": prompt}
    messages = [context]

    while True:

        content = mensaje
        
        if content =="exit":
            break
        
        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)

        response_content = response.choices[0].message.content

        messages.append({"role": "assistant", "content": response_content})
        
        url = "https://graph.facebook.com/v17.0/137446296107512/messages"
        
        payload = json.dumps({
          "messaging_product": "whatsapp",
          "recipient_type": "individual",
          "to": "54111523965421",
          "type": "text",
          "text": {
            "preview_url": False,
            "body": response_content
          }
        })
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer EAAVzJc6WKFUBOZCF0DldZBipUtdMbjZAqxFOptTQW6vXekWEr4O8Q5P8jKJkumX4NLMnXdAfjJWQzDZBdyoG8uj3kxXEqmTI4O8CkPnLPZAZCZBbP1kVCMpm8dHOhcWA2WBewkNCh4K18bJ2aB2MlHVzsBX39Oe3CzmRgLyX38LoxgJ6cVAPNiUtW00Xl2VqB5gRNwQhLjWTlsipZAEzvkRCvjGcu3gZD'
        }
        response = requests.post(url, data=payload, headers=headers)
        
        
    return response


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
        peticion(mensaj)
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
