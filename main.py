from flask import Flask, jsonify, request
import json
import request
app = Flask(__name__)
#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    #SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "Retobao" and request.args.get("hub.mode") == "subscribe":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
          return "Error de autentificacion."
    #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
    
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
      'Authorization': 'Bearer EAAVzJc6WKFUBO8FqpQZCLOxMZAY7Qvioxv1jFx2p5jEyMXSKCg3RC2ngZBg9MRbSdFeSfGhpDpMBBfqWTcCECvpzj27exeMashZAD2ZA6b24YBRwW9t3ZCiY0sfHn2pt2FvKHEmpUemhZAB78n8ezTjzkZAkDxZAZBVhdHGRvQfb2NTGxu5Gdfj67VjZBkOZCNwuqFG0IIzDFiSJUg71jGS48mqm12NhpEsZD'
    }
    response = requests.post(url, data=payload, headers=headers)
    #response = requests.request("POST", url, headers=headers, data=payload)
    print('esta aca')
    return jsonify({"status": "success"}), 200

#INICIAMSO FLASK
if __name__ == "__main__":
  app.run(debug=True)
