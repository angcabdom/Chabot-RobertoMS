import telebot
from roberto import bot_roberto
from config.auth import token

bot_teleg = telebot.TeleBot(token) # Se le inserta el token del bot

bot_teleg.delete_webhook() # Elimina el webhook para poder utilizar sin problema el metodo getUpdate

@bot_teleg.message_handler(commands=['start']) # Comando de presentacion del bot
def cmd_start(message):
    bot_teleg.send_message(message.chat.id, "Bienvenido al asistente personal del centro medico")
    bot_teleg.send_message(message.chat.id, "Puede realizar las consultas que necesite escribiendolas de manera clara")

@bot_teleg.message_handler(commands=['horario']) # Comando de horarios del bot
def cmd_horario(message):
    items = ["horario del centro", "horario de los resultados de los analisis clinicos", "horario de las consultas medicas"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(message.chat.id, "Seleccione la categoria de la que quiere obtener el horario:", reply_markup=keyboard)

@bot_teleg.message_handler(commands=['local']) # Comando de localizaciones del bot
def cmd_local(message):
    items = ["localizacion del centro", "localizacion de urgencias", "localizacion de sala de espera", "localizacion de los aseos", "localizacion de las zonas de especialidad", "localizacion de pediatria", "localizacion de la zona de las radiografias", "localizacion de los laboratorios de analiticas"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(message.chat.id, "Seleccione la categoria de la que quiere obtener la localizacion", reply_markup=keyboard)

@bot_teleg.message_handler(commands=['info']) # Comando de informacion del bot
def cmd_info(message):
    items = ["materiales para analitica", "recogida de las radiografias", "medios de contacto con el centro"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(message.chat.id, "Seleccione la categoria de la que quiere obtener informacion", reply_markup=keyboard)

@bot_teleg.message_handler(commands=['ayuda']) # Comando de ayuda del bot
def cmd_ayuda(message):
    bot_teleg.send_message(message.chat.id,"Si tiene una peticion que no le puedo resolver, por favor contacte con nuestro personal de manera directa de alguna de las siguientes formas:")
    bot_teleg.send_message(message.chat.id,"-> Telefono de atencion: 634122222, horario de atencion: 8:00 a 23:30")
    bot_teleg.send_message(message.chat.id,"-> Correo de atencion: prueba@gmail.com")
    bot_teleg.send_message(message.chat.id,"-> Telefono de urgencias: 123456789")
    bot_teleg.send_message(message.chat.id,"-> Localizacion del centro: Av. Reina Mercedes s/n, 41012 Sevilla. Google Maps -> https://n9.cl/rok3q")

@bot_teleg.message_handler(commands=['atajos']) # Comando de atajos del bot
def cmd_atajos(message):
    items = ["/horario", "/local", "/info", "/covid"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(message.chat.id,"Si tiene dificultades para resolver su consulta, intente utilizar uno de siguientes atajos:")
    bot_teleg.send_message(message.chat.id,"/horario -> Permite acceder a los horarios que son considerados como los mas relevantes para el centro")
    bot_teleg.send_message(message.chat.id,"/local -> Permite conocer las ubicaciones que son considerados como los mas relevantes para el centro")
    bot_teleg.send_message(message.chat.id,"/info -> Permite conocer informacion que es considerada como relevantes para el centro")
    bot_teleg.send_message(message.chat.id,"/covid -> Permite conocer informacion relacionada con el COVID19 relevantes para el centro")
    bot_teleg.send_message(message.chat.id, "Seleccione el atajo que quiere utilizar del teclado", reply_markup=keyboard)
    bot_teleg.send_message(message.chat.id,"O tambien puede escribir una peticion para que se deshabilite el teclado")

@bot_teleg.message_handler(commands=['comandos']) # Comando de comandos del bot
def cmd_comandos(message):
    items = ["/start", "/ayuda", "/atajos"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(message.chat.id,"A continuación se le mostraran todos los comandos disponibles:")
    bot_teleg.send_message(message.chat.id,"/start -> Presentacion del asistente")
    bot_teleg.send_message(message.chat.id,"/ayuda -> Proporciona informacion para contactar directamente con el centro")
    bot_teleg.send_message(message.chat.id,"/atajos -> Permite utilizar atajos para acceder rapidamente a informacion")
    bot_teleg.send_message(message.chat.id, "Seleccione el comando que quiere utilizar del teclado", reply_markup=keyboard)
    bot_teleg.send_message(message.chat.id,"O tambien puede escribir una peticion para que se deshabilite el teclado")

@bot_teleg.message_handler(commands=['covid'])# Comando de informacion sobre el COVID del bot
def cmd_covid(chat_id): 
    items = ["donde se realizan las pruebas del COVID19", "tipos de pruebas del COVID19", "donde vacunan del COVID19", "tipos de vacunas del COVID19"]
    keyboard = build_keyboard(items)
    bot_teleg.send_message(chat_id, "Seleccione la categoria relacionada con el COVID19 de la que quiere obtener informacion", reply_markup=keyboard)

def build_keyboard(items): # Construye un teclado personalizado
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    for item in items:
        itembtn = telebot.types.KeyboardButton(item)
        keyboard.add(itembtn)
    return keyboard

def handle_messages(messages): # Funcion que genera una respuesta a las peticiones
    for message in messages:
        if message.text is None: # Comprueba que en el mensaje hay texto
            bot_teleg.reply_to(message, "Por favor, realice las solicitudes en formato escrito")
        elif message.text.startswith('/'): # Comprueba que no es un comando
            continue
        else:
            bot_response = bot_roberto.get_response(message.text.casefold()) 
            markup = telebot.types.ReplyKeyboardRemove(selective=False) # Cerramos teclado

            bot_teleg.send_message(message.chat.id, bot_response, reply_markup=markup)


bot_teleg.set_update_listener(handle_messages) # Introduce la funcion que que se encarga de responder a las actualizaciones

bot_teleg.polling() # Mantiene el bot en funcionamiento y obtiene las actualizaciones mediante el metodo getUpdate