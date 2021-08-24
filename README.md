# ChatbotRoberto
## Table of Contents
1. [Objetivo](#objetivo)
2. [Librerías utilizadas](#librerías-utilizadas)
3. [Estructura del código](#estructura-del-código)
4. [Uso](#uso)
5. [Peticiones posibles](#peticiones-posibles)

## Objetivo
El objetivo de este proyecto es el de la creación de una inteligencia virtual que pueda entender peticiones en lenguaje natural relativas a un centro médico.

## Librerías utilizadas
El código se ha realizado en python-3.9.5 utilizando, principalmente, las siguientes librerías:
- [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/): Version 3.7.9
- [ChatterBot](https://pypi.org/project/ChatterBot/): Version 1.0.4
- [framework de flask](https://pypi.org/project/Flask/): Version 2.0.1

## Estructura del código
Existen dos ficheros principales ejecutables dentro del proyecto: [app.py](app.py) y [main.py](src/main.py), dentro de la carpeta src. La diferencia entre ambos se encuentra en la forma que se vaya a desplegar el bot, ya que [app.py](app.py) está implementado junto a flask para que pueda ser desplegado en la nube sin demasiada complicación y [main.py](src/main.py) está pensado para desplegarlo en local, necesitando crear una carpeta config que contenga un archivo auth.py junto con el token de telegram.

Por otro lado podemos encontrarnos el método de entrenamiento general dentro de la carpeta src, llamado [trainning.py](src/trainning.py), que al ejecutarse "entrena" al bot declarado en el archivo [roberto.py](src/roberto.py), y que este a su vez genera un archivo dentro de la carpeta db, llamado [database.db](src/db/database.db), que contiene todas las conversaciones utilizadas por el archivo de entrenamiento y las nuevas conversaciones que se vayan generando. Así mismo, los ficheros .yml utilizados durante los entrenamientos se encuentran en la ruta [./src/train/spanish](src/train/spanish).

<p align="center">
  <img src="https://user-images.githubusercontent.com/56036551/130678439-4233b0c3-8356-4fd0-b297-91eb5fcf3577.png">
</p>

## Instalación 
La instalación local del proyecto es bastante sencilla, solamente requiere de la instalación de los archivos y de los paquetes utilizados.
- Primero clonamos el repositorio en la ruta que queramos:
```
$ git clone https://example.com
```
- Después accedemos al directorio principal del proyecto e instalamos los paquetes que aparecen en el requirements.txt:
```
$ cd ../ChatbotRoberto
$ pip install -r requirements.txt
```
- Creamos una carpeta config dentro de src y dentro creamos un archivo que contenga el token de nuestro bot.
-  Y por último, tenemos que ejecutar el archivo main.py que se encuentra dentro de la carpeta src:
```
$ cd ../ChatbotRoberto/src
$ python3 main.py
```

## Uso
El código del bot se encuentra desplegado en el servicio de cloud de [Microsoft Azure](https://azure.microsoft.com/es-es/services/cloud-services/) y se puede utilizar a través del siguiente enlace: [http://t.me/RobertoMSBot](http://t.me/RobertoMSBot), o introduciendo en el buscador de telegram "RobertoMSBot".


## Peticiones posibles
Actualmente el asistente puede responder a las siguientes peticiones:

| Localización | Horarios | Información general | COVID19 |
|:--------------|:-------------:|:-------------:|--------------:|
| Centro médico | Apertura del centro médico | Materiales para analíticas | Vacunas |
| Urgencias | Entrega de resultados | Recogida de radiografías | Pruebas |
| Sala de espera | Consultas | Medios de contacto con el centro |  |
| Aseos | Resultados de analíticas |  |  |
| Ala de especialidades |  |  |  |
| Pediatria |  |  |  |
| Zona de radiografías |  |  |  |
| Laboratorio de analíticas |  |  |  |
