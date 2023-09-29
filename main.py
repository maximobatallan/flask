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

        # Imprime el contenido
    print(data)
    url = "https://graph.facebook.com/v17.0/137446296107512/messages"

    payload = json.dumps({
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": "54111523965421",
      "type": "text",
      "text": {
        "preview_url": False,
        "body": "River"
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer EAAVzJc6WKFUBO2AfQ2BXqrPXJufQZBJL7xCi0yNzcJLZBJE7D7o8350LDsDP635XjZARjBcRN7ZB6TCzbBCUPHAQZB3aTYuiM1Ut9C4SAmJxbAftrZAkRenrzQLqDoYpnNi7LqdI3kHsbrt7smAvRqxdyGqmSqRsWyMsnia9ErF0zfzZBDdBDd8NuUzTTGZB15VFOwSsef1Hi1QKSsKYC80hCygFCsgZD'
    }
    response = requests.post(url, data=payload, headers=headers)
    #response = requests.request("POST", url, headers=headers, data=payload)
    print('esta aca')
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run()
