import paho.mqtt.client as mqtt
import random
import time
import json

# MQTT Configuration
MQTT_ip = "82.78.81.188"  # Server
MQTT_port = 1883 
MQTT_topic = "/training/device/traianis-eftenoiu"  # Topic
reconnect = True

# Speed generator
def generate_motor_data():
    motor_id = "motor1"
    speed = random.randint(1000, 4000)  # Random speed
    data = {
        "motor_id": motor_id,
        "speed": speed
    }
    return data

# Publish function
def publish_data(client, topic, data):
    payload = json.dumps(data)
    client.publish(topic, payload)

# on_disconnect function
def on_disconnect(client, userdata, rc):
    if reconnect:
        print("Disconnected, attempting to reconnect...")
        while True:
            try:
                client.reconnect()
                print("Reconnected")
                break
            except:
                print("Reconnect failed, retrying in 5 seconds...")
                time.sleep(5)

# Client configuration
client = mqtt.Client()
client.on_disconnect = on_disconnect  # Set the on_disconnect callback
client.connect(MQTT_ip, MQTT_port)

# Publishing the data
try:
    while True:
        motor_data = generate_motor_data()
        print(f"Publishing data: {motor_data}")
        publish_data(client, MQTT_topic, motor_data)
        time.sleep(10)  # Sleep 10 sec
except KeyboardInterrupt:
    print("Finished")
    reconnect = False
    client.disconnect()
