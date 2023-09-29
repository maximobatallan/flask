from flask import Flask, jsonify, request
import requests
import json
app = Flask(__name__)
#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
def handle_message():
    # Parse requests body in json format
    url = "https://graph.facebook.com/v17.0/137446296107512/messages"

    payload = json.dumps({
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": "54111523965421",
      "type": "text",
      "text": {
        "preview_url": False,
        "body": "qqqq"
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer EAAVzJc6WKFUBO8FqpQZCLOxMZAY7Qvioxv1jFx2p5jEyMXSKCg3RC2ngZBg9MRbSdFeSfGhpDpMBBfqWTcCECvpzj27exeMashZAD2ZA6b24YBRwW9t3ZCiY0sfHn2pt2FvKHEmpUemhZAB78n8ezTjzkZAkDxZAZBVhdHGRvQfb2NTGxu5Gdfj67VjZBkOZCNwuqFG0IIzDFiSJUg71jGS48mqm12NhpEsZD'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    print('esta aca')
    return jsonify({"status": "success"}), 200


def verify(requests):
    # Parse params from the webhook verification requests
    mode = requests.args.get("hub.mode")
    token = requests.args.get("hub.verify_token")
    challenge = requests.args.get("hub.challenge")
    # Check if a token and mode were sent
    if requests.method == "GET":
        if mode and token:
            # Check the mode and token sent are correct
            if mode == "subscribe" and token == "Retobao":
                # Respond with 200 OK and challenge token from the requests
                print("WEBHOOK_VERIFIED")
                return challenge, 200
            else:
                # Responds with '403 Forbidden' if verify tokens do not match
                print("VERIFICATION_FAILED")
                return jsonify({"status": "error", "message": "Verification failed"}), 403
        else:
            # Responds with '400 Bad requests' if verify tokens do not match
            print("MISSING_PARAMETER")
            return jsonify({"status": "error", "message": "Missing parameters"}), 400
    data=requests.get_json()
    #EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
    mensaje="Telefono:"+data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    mensaje=mensaje+"|Mensaje:"+data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    #ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
    print(mensaje)
    #RETORNAMOS EL STATUS EN UN JSON
    return jsonify({"status": "success"}, 200)
    

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":    
        print('get')
        return verify(requests)
    elif request.method == "POST":
        print('post')
        return handle_message()


#INICIAMSO FLASK
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
