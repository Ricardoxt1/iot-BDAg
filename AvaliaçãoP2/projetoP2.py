# Bibliotecas necessárias para o código
import Adafruit_DHT as dht
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import requests
import sys
import time as t 

# Configuração do raspiberry
GPIO.setmode(GPIO.BOARD)
led = 21
pino_sensor = 25

# Configurações do ThingSpeak
URL = 'https://api.thingspeak.com/update?api_key=HA6C0KPBFWKMZQJK&field1='
URL_twitter = 'https://api.thingspeak.com/apps/thingtweet/1/statuses/update'

Broker = "test.mosquitto.org"
PortaBroker = 1883
KeepAliveBroker = 60
TopicoSubscribe = "finotidelta1705"

def on_connect(client, userdata, flags, rc):
    print('[STATUS] Conectando ao Broker.')
    # Inscrever no tópico configurado
    client.subscribe(TopicoSubscribe)

def on_message(client, userdata, msg):
    MensagemRecebida = str(msg.payload)
    ligar_led(MensagemRecebida)

def ligar_led(codigo):
    if codigo == "b'1'":
        GPIO.output(led, HIGH)
        print("BOMBA LIGADA!")
    elif codigo == "b'0'":
        GPIO.output(led, LOW)
        print("BOMBA DESLIGADA!")

try:
    print("[STATUS] Inicializando MQTT...")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(Broker, PortaBroker, KeepAliveBroker)
    client.loop_start()

    while True:
        temp, umid = dht.read_retry(dht.DHT11, pino_sensor)
        print("Temp: {0:.1f}".format(temp))

        requests.get(URL + str(temp))

        if temp > 23:
            client.publish(TopicoSubscribe, "1")
            # Tweet apenas se a temperatura for maior que 23
            requests.post(URL_twitter, data={"api_key":"7BUK0GHQAAM4VY8X", "status":"Alerta: temperatura alta! Temperatura atual: {0:.1f}%".format(temp)})
        else:
            client.publish(TopicoSubscribe, "0")

        t.sleep(5)

except KeyboardInterrupt:
    print("Programa encerrado pelo usuário!")
    client.disconnect()
    client.loop_stop()
