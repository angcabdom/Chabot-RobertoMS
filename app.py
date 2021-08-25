import telebot
import os
from chatterbot import ChatBot
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

API_TOKEN = os.environ['API_TOKEN']
bot_teleg = telebot.TeleBot(API_TOKEN) # Se le inserta el token del bot

bot_teleg.remove_webhook()

SECRET_NUMBER = API_TOKEN

bot_teleg.set_webhook(url="https://robertomsbot.azurewebsites.net/{}".format(SECRET_NUMBER), max_connections=40, allowed_updates= ["message"]) #Se establece un webhook para recibir las consultas



bot_roberto = ChatBot(
    'Roberto',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            'default_response': 'Por favor, reformule su peticion',
            'maximum_similarity_threshold': 0.90
        }
        
    ],
    database_uri='sqlite:///src/db/database.db'
)

def cmd_start(chat_id, user): # Comando de presentacion del bot
    bot_teleg.send_message(chat_id, "Bienvenido al asistente personal del centro medico, " + user)
    bot_teleg.send_message(chat_id, "Puede realizar las consultas que necesite escribiendo de manera clara lo que necesita")

def cmd_horario(chat_id): # Comando de horarios del bot
    items = ["horario del centro", "horario de los resultados de los analisis clinicos", "horario de las consultas medicas"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(chat_id, "Seleccione la categoria de la que quiere obtener el horario:", reply_markup=keyboard)

def cmd_local(chat_id): # Comando de localizaciones del bot
    items = ["localizacion del centro", "localizacion de urgencias", "localizacion de sala de espera", "localizacion de los aseos", "localizacion de las zonas de especialidad", "localizacion de pediatria", "localizacion de la zona de las radiografias", "localizacion de los laboratorios de analiticas"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(chat_id, "Seleccione la categoria de la que quiere obtener la localizacion", reply_markup=keyboard)

def cmd_info(chat_id): # Comando de informacion del bot
    items = ["materiales para analitica", "recogida de las radiografias", "medios de contacto con el centro"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(chat_id, "Seleccione la categoria de la que quiere obtener informacion", reply_markup=keyboard)

def cmd_ayuda(chat_id): # Comando de ayuda del bot
    bot_teleg.send_message(chat_id,"Si tiene una peticion que no le puedo resolver, por favor contacte con nuestro personal de manera directa de alguna de las siguientes formas:")
    bot_teleg.send_message(chat_id,"-> Telefono de atencion: 634122222, horario de atencion: 8:00 a 23:30")
    bot_teleg.send_message(chat_id,"-> Correo de atencion: prueba@gmail.com")
    bot_teleg.send_message(chat_id,"-> Telefono de urgencias: 123456789")
    bot_teleg.send_message(chat_id,"-> Localizacion del centro: Av. Reina Mercedes s/n, 41012 Sevilla. Google Maps -> https://n9.cl/rok3q")

def cmd_atajos(chat_id): # Comando de atajos del bot
    items = ["/horario", "/local", "/info", "/covid"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(chat_id,"Si tiene dificultades para resolver su consulta, intente utilizar uno de siguientes atajos:")
    bot_teleg.send_message(chat_id,"/horario -> Permite acceder a los horarios que son considerados como los mas relevantes para el centro")
    bot_teleg.send_message(chat_id,"/local -> Permite conocer las ubicaciones que son considerados como los mas relevantes para el centro")
    bot_teleg.send_message(chat_id,"/info -> Permite conocer informacion que es considerada como relevantes para el centro")
    bot_teleg.send_message(chat_id,"/covid -> Permite conocer informacion relacionada con el COVID19 relevantes para el centro")
    bot_teleg.send_message(chat_id, "Seleccione el atajo que quiere utilizar del teclado", reply_markup=keyboard)
    bot_teleg.send_message(chat_id,"O tambien puede escribir una peticion para que se deshabilite el teclado")

def cmd_comandos(chat_id): # Comando de comandos del bot
    items = ["/start", "/ayuda", "/atajos"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(chat_id,"A continuación se le mostraran todos los comandos disponibles:")
    bot_teleg.send_message(chat_id,"/start -> Presentacion del asistente")
    bot_teleg.send_message(chat_id,"/ayuda -> Proporciona informacion para contactar directamente con el centro")
    bot_teleg.send_message(chat_id,"/atajos -> Permite utilizar atajos para acceder rapidamente a informacion")
    bot_teleg.send_message(chat_id, "Seleccione el comando que quiere utilizar del teclado", reply_markup=keyboard)
    bot_teleg.send_message(chat_id,"O tambien puede escribir una peticion para que se deshabilite el teclado")

def cmd_covid(chat_id): # Comando de informacion sobre el COVID del bot
    items = ["donde se realizan las pruebas del COVID19", "tipos de pruebas del COVID19", "donde vacunan del COVID19", "tipos de vacunas del COVID19"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(chat_id, "Seleccione la categoria relacionada con el COVID19 de la que quiere obtener informacion", reply_markup=keyboard)

def build_keyboard(items): # Construye un teclado personalizado
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    for item in items:
        itembtn = telebot.types.KeyboardButton(item)
        keyboard.add(itembtn)
    return keyboard

last_update_id = None
last_update_time = None

def reset_last_update_id(): # Verificacion de necesidad de reiniciar el contador de tiempo si pasa una semana
    global last_update_time
    if last_update_time == None:
        last_update_time = datetime.now()
    else:
        days = (datetime.now() - last_update_time).days
        if days >= 7:
            global last_update_id
            last_update_id = None
        last_update_time = datetime.now()

@app.route('/{}'.format(SECRET_NUMBER), methods=["POST"]) # La funcion se activa cada vez que recibe una consulta del bot
def telegram_webhook(): # Funcion que obtiene la respuesta a la peticion
    update = request.get_json()
    if update != None:
        update_id = update["update_id"]

        reset_last_update_id()
        global last_update_id
        if last_update_id == None or last_update_id < update_id:
            last_update_id = update_id
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                if "text" in update["message"]:
                    text = update["message"]["text"]
                    text_str = str(text.casefold())
                    if text_str.startswith("/"): # Comprobacion de comandos
                        if text_str == "/start":
                            user = update["message"]["from"]["first_name"]
                            cmd_start(chat_id, user) 
                        elif text_str == "/horario":
                            cmd_horario(chat_id) 
                        elif text_str == "/local":
                            cmd_local(chat_id) 
                        elif text_str == "/info":
                            cmd_info(chat_id) 
                        elif text_str == "/ayuda":
                            cmd_ayuda(chat_id) 
                        elif text_str == "/atajos":
                            cmd_atajos(chat_id) 
                        elif text_str == "/comandos":
                            cmd_comandos(chat_id)  
                        elif text_str == "/covid":
                            cmd_covid(chat_id)  
                        else:
                            bot_teleg.send_message(chat_id, "Por favor, utilice uno de los comandos disponibles")
                    else:
                        bot_response = bot_roberto.get_response(str(text.casefold())) 
                        markup = telebot.types.ReplyKeyboardRemove(selective=False) # Cerramos teclado

                        bot_teleg.send_message(chat_id, bot_response, reply_markup=markup)
                else:
                    bot_teleg.send_message(chat_id, "Por favor, realice las solicitudes en formato escrito")
    return 'ok'

@app.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux"
