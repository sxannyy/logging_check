import time
from loguru_logger import logger
import paho.mqtt.client as mqtt_client
import random
import requests

broker = "broker.emqx.io"

try:
    unique_token = requests.get('http://127.0.0.1:8000/get_token').json()[0]
    logger.info("Уникальный токен для автора выдан успешно!")
except requests.exceptions.ConnectionError:
    logger.error("Сервер упал полежать или вовсе не вставал...")

client = mqtt_client.Client(
   mqtt_client.CallbackAPIVersion.VERSION1, 
   unique_token
)

logger.info("Подключаемся к брокеру...")
client.connect(broker)
client.loop_start()
logger.info("Автор пишет-пишет... публикует...")

for i in range(4):
    state = "on" if random.randint(0, 1) == 0 else "off"
    state = state + " ну... ну... блин..."
    print(f"State is {state}")
    client.publish("lab/leds/hello/state", state)
    time.sleep(2)

logger.warning("У автора устали писать руки... Он устал, он мухожук...")
client.disconnect()
client.loop_stop()
