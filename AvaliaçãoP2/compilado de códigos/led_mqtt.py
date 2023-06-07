import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import sys
from time import sleep

GPIO.setmode(GPIO.BCM)
led = 40 

GPIO.setup(led, GPIO.OUT)

Broker = "test.mosquitto.org"
PortaBroker = 1883
KeepAliveBroker = 60
TopicoSubscribe = "finotidelta1705"

# Função de conexão com o Broker
def on_connect(client, userdata, flags, rc):
  print('[STATUS] Conectando ao Broker.')
  # Inscrever no tópico configurado
  client.subscribe(TopicoSubscribe)

# Função para recebimento das mensagens
def on_message(client, userdata, msg):
  MensagemRecebida = str(msg.payload)
  ligar_led(MensagemRecebida)

# Funcionalidade do MQTT
def ligar_led(codigo):
  if codigo == "b'1'":
    GPIO.output(led, True)
    print("LED ACESO!")
  elif codigo == "b'0'":
    GPIO.output(led, False)
    print("LED DESLIGADO!")

try:
    print("[STATUS] Inicializando MQTT...")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect (Broker, PortaBroker, KeepAliveBroker)
    client.loop_forever()   

except KeyboardInterrupt:
  print("Saindo")
  sys.exit(0)
