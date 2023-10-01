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
    print ('mensaje')
    if 'body' in json.dumps(mensaje):
        
        print ('mensaje')
        url = "https://graph.facebook.com/v17.0/137446296107512/messages"
        print('estamosaca')
        payload = json.dumps({
          "messaging_product": "whatsapp",
          "recipient_type": "individual",
          "to": "54111523965421",
          "type": "text",
          "text": {
            "preview_url": False,
            "body": 'Somos los Pibes que Alentamos a River Plate'
          }
        })
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer EAAVzJc6WKFUBO8Y1LyfTDbQZBF9ZBsqT8BN1qIFOPZCZBf5wxVMJRP2kZAaZBsrHWwf3hSeeTTZANwmVMR3EVitlgEXwSZCTysPx4IsrfcY9RbNZCocDW5N1Y9UOhtjwVsFKrnfCXJlJ4UvPoG6qWQf1qp27msMtGTdi94Kp9dPSvYbSJGy1iZCsBIfNz6Oh2YGl1tWFotwSO6y3ewBtCJi7Ldrq9PA8YZD'
        }
        response = requests.post(url, data=payload, headers=headers)
        #response = requests.request("POST", url, headers=headers, data=payload)
    else:
        print("La clave 'body' no está en el JSON.")
      
        
    
        
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run()
