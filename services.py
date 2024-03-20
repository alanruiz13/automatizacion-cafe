import requests
import pas
import json
import time


def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = pas.whatsapp_token
        whatsapp_url = pas.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data



def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def image_Message(number, image_url, caption):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "image",
            "image": {
                "link": image_url,
                "caption": caption
            }
        }
    )
    return data
  
  
intentos_no_entendidos = 0
def administrar_chatbot(text ,number , messageId, name):
  
    text = text.lower()  # Convertir el mensaje a minúsculas para facilitar la comparación
    # Crear una variable de seguimiento para contar cuántas veces el chatbot no ha entendido el mensaje
    global intentos_no_entendidos

    # Si el mensaje no ha sido entendido tres veces seguidas, ofrecer la opción de escribir a otro número
    if intentos_no_entendidos == 2:
        # Reiniciar el contador de intentos
        intentos_no_entendidos = 0
        textMessage = text_Message(number, "Lo siento, parece que no puedo entender tu mensaje. ¿Te gustaría hablar con una persona? Si es así, escribe ' Ayuda ' de lo contrario puedes decir 'Hola' para reiniciar el bot.")
        enviar_Mensaje_whatsapp(textMessage)
        return
      
    list = []
    print("mensaje del usuario: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)

    if "hola" in text:
        body = "¡Hola! 👋 Gracias por escribir a la tregua. ¿Cómo podemos ayudarte hoy?"
        footer = "Equipo de la tregua"
        options = ["Horarios", "Menú", "Eventos próximos","Promociones","Redes sociales","Ubicación"]

        replyListData = listReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyListData)
    elif "horarios" in text:
        textMessage = text_Message(number,"Claro que sí, nuestros horarios los días Lunes, Miércoles, Jueves, Sabado y Domingo es de 11:00 am a 09:00 pm")
        time.sleep(2)
        enviar_Mensaje_whatsapp(textMessage)
        
        textMessage = text_Message(number,"Los Martes y Viernes, de 03:00 pm a 09:00 pm.")
        time.sleep(1)
        enviar_Mensaje_whatsapp(textMessage)
        
        textMessage = text_Message(number,"Te esperamos pronto en la barra. Lindo día.")
        time.sleep(1)
        enviar_Mensaje_whatsapp(textMessage)
        
    elif "menú" in text: 
        textMessage = text_Message(number,"En un momento te comparto el menú")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        document = document_Message(number, pas.document_url, "Te esperamos pronto en la barra, ten un lindo día", "menuLaTregua0224.pdf")
        enviar_Mensaje_whatsapp(document)
        
    elif "eventos próximos" in text: 
        evento1 = document_Message(number, pas.evento1_url, "Te esperamos para nuestro trueque de libro, donde podras traer tus libros y cambiarlos por otros (no se aceptan en mal estado o libros escolares)", "evento1.mp4")
        enviar_Mensaje_whatsapp(evento1)
        time.sleep(1)
        
        evento2 = image_Message(number, pas.evento2_url, "El taller de introduccion a la acuarela tendra un enfoque pra poder pintar cosas botanicas como planatas y flores, te esperamos para un viernes lleno de café y pintura")
        enviar_Mensaje_whatsapp(evento2)
        time.sleep(1)
        
        evento3 = image_Message(number, pas.evento3_url, "Nuestra noche eclectica mensual es donde podras probar nuestos chais herbales, conocer un poco de su historia y jugar jeugos de mesa para convivir y platicar.")
        enviar_Mensaje_whatsapp(evento3)
        time.sleep(1)
        
        evento4 = image_Message(number, pas.evento4_url, "El ultimo evento del mes es la noche eclectia de café donde habran nuevas bebidas que se incluiran en el menú y puedes ser de las primeras personas en probar estas unicas bebidas refrescantes tomando como inspiracion la primavera")
        enviar_Mensaje_whatsapp(evento4)
        time.sleep(2)
        
        body = "¿Te gustaria inscribirte a alguno de estos eventos?"
        footer = ""
        options = ["Si, claro", "No, gracias"]

        replyListData = listReply_Message(number, options, body, footer, "sed2",messageId)
        replyReaction = replyReaction_Message(number, messageId, "❤️")
        list.append(replyReaction)
        list.append(replyListData)

    elif "no, gracias" in text:
        replyReaction = replyReaction_Message(number, messageId, "✌️")
        textMessage = text_Message(number,"Espero tengas un bonito día y que la informacion te haya servido.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"Te esperamos pronto en la barra.")
        enviar_Mensaje_whatsapp(textMessage)
    
    elif "si, claro" in text:
        body = "¿A cuál evento te gustaria inscribirte?"
        footer = ""
        options = ["Acuarela", "Noche Eclectica"]

        replyListData = listReply_Message(number, options, body, footer, "sed3",messageId)
        replyReaction = replyReaction_Message(number, messageId, "❤️")
        list.append(replyReaction)
        list.append(replyListData)
      
    elif "acuarela" in text:
        body = "Para inscribirte al curso de acuarela puedes apartar tu lugar depositando el 50% del valor del curso o puedes pasar a la barra a hacer el pago en efectivo o tarjeta. Puedo darte mas informacion dependiendo del metodo de pago que elijas"
        footer = ""
        options = ["Depositar", "En efectivo", "Solo queria info"]

        replyListData = listReply_Message(number, options, body, footer, "sed4",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🎨")
        list.append(replyReaction)
        list.append(replyListData)
        
    elif "noche eclectica" in text:
        body = "Para inscribirte a la Noche Eclectica puedes apartar tu lugar depositando el 50% del valor del evento o puedes pasar a la barra a hacer el pago en efectivo o tarjeta. Puedo darte mas informacion dependiendo del metodo de pago que elijas"
        footer = ""
        options = ["Depositar", "En efectivo", "Solo queria info"]

        replyListData = listReply_Message(number, options, body, footer, "sed4",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🌙")
        list.append(replyReaction)
        list.append(replyListData)
    
    elif "depositar" in text: 
        textMessage = text_Message(number,"Claro, te puedo compartir los datos de la cuenta donde puedes depositar el 50% para apartar tu lugar")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"La cuenta CLABE es del banco CitiBanamex:")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"002 650 904 775 040 690")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"A nombre de: ")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"Alan Ruiz")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"Cuando hagas el deposito puedes mandar una captura de pantalla, junto con tu nombre, al numero: +52 56 4898 3239 ")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"En menos de 24 hora te contestaremos confirmando tu deposito, o bien puedes escribirnos por instagram")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
    elif "en efectivo" in text:
        textMessage = text_Message(number,"Te invito a que nos visites en la tregua para que puedas hacer el pago y te anoten en la lista")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"La direccion es 2 oriente #203, San Andres Cholula, Puebla, México. (entre la 2 norte y la 4 norte) ")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1) 
        
        textMessage = text_Message(number,"Esta es la ubicación de la barra: https://maps.app.goo.gl/tX1Mfdz2WTXzcB558 ")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"Te esperamos en la barra, ten un lindo día.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
    elif "solo queria info" in text: 
        textMessage = text_Message(number,"Claro que sí, si necesitas ayuda en algo más, puedes decir Hola, para reiniciar el bot.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"De lo contrario, espero tengas un buen día.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
      
    elif "promociones" in text: 
        promo1 = image_Message(number, pas.lunes_url, "Los lunes te esperamos para comenzar con toda la actitud la semana.")
        enviar_Mensaje_whatsapp(promo1)
        time.sleep(1)
        
        
        promo2 = image_Message(number, pas.quack_url, "Todos los días te esperamos con este buen combo, así es, todos los días.")
        enviar_Mensaje_whatsapp(promo2)
        time.sleep(1)
        
        promo3 = image_Message(number, pas.pay_url, "Esta es la unica promoción que nunca sabemos cuando estará disponible, por eso te recomiendo que nos sigas en nuestras redes, generalmente avisamos en una story de instagram, es una sopresa para ustedes y para nosotros.")
        enviar_Mensaje_whatsapp(promo3)
        time.sleep(2)
        
        textMessage = text_Message(number,"Te esperamos pronto en la barra para poder disfrutar de estas promociones. Ten un buen dia.")
        enviar_Mensaje_whatsapp(textMessage)
        
    elif "redes sociales" in text:
        textMessage = text_Message(number,"En instagram nos encuentras como @la.tregua.cholula")
        enviar_Mensaje_whatsapp(textMessage)
        
        textMessage = text_Message(number,"Te dejo el link para que nos sigas https://www.instagram.com/la.tregua.cholula/")
        enviar_Mensaje_whatsapp(textMessage)
        
    elif "ubicación" in text:
        textMessage = text_Message(number,"Puedes encontrarnos en la 2 Oriente #203, San Andrés Cholula.")
        enviar_Mensaje_whatsapp(textMessage)
        
        textMessage = text_Message(number,"Te dejo el link para que puedas llegar más fácil https://maps.app.goo.gl/tX1Mfdz2WTXzcB558 ")
        enviar_Mensaje_whatsapp(textMessage)
        
    elif "gracias" in text:
        replyReaction = replyReaction_Message(number, messageId, "🥰")
        list.append(replyReaction)
        
        textMessage = text_Message(number,"Ay, nadie se habia interesado tanto por mi, soy un robot cuya función es ayudarte, pero el que me agradezcas esta bonito.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"Que bonita persona eres, 🥰")
        enviar_Mensaje_whatsapp(textMessage)
        
    elif "🍀" in text:
        replyReaction = replyReaction_Message(number, messageId, "🍀")
        list.append(replyReaction)
        
        textMessage = text_Message(number,"Entiendo, vienes por el acertijo")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"Si logras decifrar la prueba, podrás tener una rencompensa")
        enviar_Mensaje_whatsapp(textMessage)
        
        textMessage = text_Message(number,"La pregunta es simple, ¿Que especie de café tenemos en tolva?")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        textMessage = text_Message(number,"Es facil encontrar la respuesta solo tienes que prestar atención en la barra, ahi obtendras la información.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
                                   
        textMessage = text_Message(number,"Si te cuesta encontrarla, no dudes en preguntarle al barista en turno. Mucha suerte.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        #continuar el modo viajero 
                                   
    elif "lavado" in text:
        replyReaction = replyReaction_Message(number, messageId, "🍀")
        list.append(replyReaction)
        
        textMessage = text_Message(number,"Perfecto, encontraste la clave.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(1)
        
        descuento = image_Message(number, pas.cupon_url, "Aqui tienes tu rencompensa querido amigo, espero vuelvas pronto y la disfrutes. Aun nos quedan muchas aventuras por descubrir")
        enviar_Mensaje_whatsapp(descuento)
        time.sleep(1)
        
        textMessage = text_Message(number,"Espero lo disfriutes y te vaya muy bien. Te veo en la barra.")
        enviar_Mensaje_whatsapp(textMessage)
        
    elif "fight club" in text:
        textMessage = text_Message(number,"Recuerda, la primera regla del club de pelea, es que NADIE habla del club de la pelea.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(2)
        
        textMessage = text_Message(number,"Bienvenido a esta bella comunidad de gente especial para la tregua, como tu, que les gusta el cafe y quieren saber mas de cerca el progreso de la tregua.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(3)
        
        textMessage = text_Message(number,"Sigue el link para unirte al grupo de whatsapp y estar en esta bella comunidad.")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(2)
        
        textMessage = text_Message(number,"https://chat.whatsapp.com/L8WaIDbaeqy91m8LDdZRLz")
        enviar_Mensaje_whatsapp(textMessage)
        
        #mejorar o hacer mas largo este modo
    elif "ayuda" in text:
        textMessage = text_Message(number,"Entiendo que necesitas más ayuda que no te puedo brindar, para hablar con alguien, solo tienes que escribrir al: +52 56 4898 3239")
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(2)

    else :
        data = text_Message(number,"Lo siento, no entendí lo que dijiste. Para inciar el chatbot solo tienes que decir Hola ")
        intentos_no_entendidos += 1

        list.append(data)

    for item in list:
        enviar_Mensaje_whatsapp(item)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    number = s[3:]
    if s.startswith("521"):
        return "52" + number
    elif s.startswith("549"):
        return "54" + number
    else:
        return s
        