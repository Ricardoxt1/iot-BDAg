import Adafruit_DHT as dht
import time as t 
import requests
import paho.mqtt.client as mqtt
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

pino_sensor = 25

# Definições / Configurações
Broker = "test.mosquitto.org"
PortaBroker = 1883
KeepAliveBroker = ""
TopicoSubscribe = "finotidelta1705"

# Funcionalidade do MQTT
def funcaoMqtt(codigo):
  if codigo == "b'1'":
    print("Ligar")
  elif codigo == "b'0'":
    print("Desligar")
    
# Função de conexão com o Broker
def on_connect(client, userdata, flags, rc):
  print('[STATUS] Conectando ao Broker. Resultado da Conexão: '+str(rc))
  # Inscrever no tópico configurado
  client.subscribe(TopicoSubscribe)

# Função para recebimento das mensagens
def on_message(client, userdata, msg):
  MensagemRecebida = str(msg.payload)
  print("[MSG RECEBIDA] Topico: "+msg.topic+" / Mensagem: "+MensagemRecebida)
  funcaoMqtt(MensagemRecebida)

# Configurações do ThingSpeak
URL = 'https://api.thingspeak.com/update?api_key=HA6C0KPBFWKMZQJK&field1='
URL2 = 'https://api.thingspeak.com/update?api_key=HA6C0KPBFWKMZQJK&field2='
URL_twitter = 'https://api.thingspeak.com/apps/thingtweet/1/statuses/update'

try:
    print("[STATUS] Inicializando o MQTT...")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Conexão Propriamente dita
    client.connect(Broker, PortaBroker, KeepAliveBroker)
    client.loop_forever()
    
    while True:        
        umid, temp = dht.read_retry(dht.DHT11, pino_sensor)
        print('Temp: {0:.1f}    Umida: {1:.1f}'.format(temp, umid))
        t.sleep(5)

        requests.get(URL + str(temp))
        requests.get(URL2 + str(umid))

        # Tweet os valores para o Twitter
        if temp > 37:
            # Tweet apenas se a temperatura for maior que 37
            requests.post(URL_twitter, data={"api_key":"7BUK0GHQAAM4VY8X", "status":"Alerta: temperatura alta! Temperatura atual: {0:.1f}%".format(temp)})
        t.sleep(1)

except KeyboardInterrupt:
    print("Programa encerrado pelo usuário!")
