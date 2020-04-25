import RPi.GPIO as GPIO
import time
import math
import paho.mqtt.client as mqtt
import datetime
import ssl
import json

OPEN_TIME = 6
CLOSE_TIME = 20
GATE_OPEN_CLOSE_SECONDS = 3

OPEN = False
FIRE_DETECTED = False
CHICKENS_MAGNETOMETER_VALUE = False
CHICKENS_IN_BED_MAGNITUDE = 50000

#mqtt data
host          = "node02.myqtthub.com"
port          = 1883
clean_session = True
client_id     = "gate"
user_name     = "bravogate@yopmail.com"
password      = "8sLBIaF9-m5OvAlEA"

def on_connect (client, userdata, flags, rc):
    """ Callback called when connection/reconnection is detected """
    print ("Connect %s result is: %s" % (host, rc))

    # With Paho, always subscribe at on_connect (if you want to
    # subscribe) to ensure you resubscribe if connection is
    # lost.
    client.subscribe("aberdeen/animalhouse/chicken/1/air")
    client.subscribe("aberdeen/animalhouse/chicken/1/magnetometers")

    if rc == 0:
        client.connected_flag = True
        print ("connected OK")
        return

    print ("Failed to connect to %s, error was, rc=%s" % rc)
    # Handle error here
    sys.exit (-1)

def on_message(client, userdata, msg):
    """ Callback called for every PUBLISH received """
    jsonStr = str(message.payload.decode("UTF-8"))
    print("Message received " + jsonStr)
    jsonStr = json.loads(jsonStr)
    FIRE_DETECTED = jsonStr.get("fire")
    CHICKENS_MAGNETOMETER_VALUE = jsonStr.get("value")



# Define clientId, host, user and password
client = mqtt.Client (client_id = client_id, clean_session = clean_session)
client.username_pw_set (user_name, password)

client.on_connect = on_connect
client.on_message = on_message

# Configure TLS connection
client.tls_set (cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set (False)
port = 8883

# Connect using secure MQTT with keepalive 60
client.connect (host, port, keepalive = 60)
client.connected_flag = False
while not client.connected_flag:
    client.loop()
    time.sleep (1)

#motor
Motor1A = 17
Motor1B = 27
Motor1E = 22

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor1A, GPIO.OUT)
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor1E, GPIO.OUT)

#test method
def loop():
    #forwards
    open()
    time.sleep(2)

    #backwards
    close()
    time.sleep(2)

def open():
    print("opening")

    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)

    time.sleep(GATE_OPEN_CLOSE_SECONDS)

    GPIO.output(Motor1E, GPIO.LOW)

    OPEN = True

def close():
    print("closing")

    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)

    time.sleep(GATE_OPEN_CLOSE_SECONDS)

    GPIO.output(Motor1E, GPIO.LOW)

    OPEN = False

def destroy():
    GPIO.cleanup()

# Check MQTT every mqtt_check_time seconds
mqtt_check_time = 10

if __name__ == '__main__':
    setup()
    try:
        while True :
            if ((datetime.datetime.now().hour >= OPEN_TIME and OPEN == False) and (datetime.datetime.now().hour < OPEN_TIME + 1 and OPEN == False)) or FIRE_DETECTED
                open()
            else ((datetime.datetime.now().hour >= CLOSE_TIME and OPEN == True) and (datetime.datetime.now().hour < CLOSE_TIME + 1 and OPEN == True)) and abs(CHICKENS_MAGNETOMETER_VALUE) > CHICKENS_IN_BED_MAGNITUDE
                close()
        time.sleep(mqtt_check_time)
    except KeyboardInterrupt:
        destroy()
