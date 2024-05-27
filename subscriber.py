import datetime
import time
import paho.mqtt.client as mqtt_client
import requests
from loguru import logger

INACTIVITY_TIMEOUT_IN_SEC = 10

last_message_time = datetime.datetime.now()

broker = "broker.emqx.io"

def on_message(client, userdata, message):
    global last_message_time
    logger.debug("Сообщение было получено")
    last_message_time = datetime.datetime.now()
    data = str(message.payload.decode("utf-8"))
    print("received message =", data)

try:
    unique_token = requests.get('http://127.0.0.1:8000/get_token').json()[0]
    logger.info("Уникальный токен для пользователя выдан успешно!")
except requests.exceptions.ConnectionError:
    logger.error("Сервер упал полежать или вовсе не вставал...")

client = mqtt_client.Client(
   mqtt_client.CallbackAPIVersion.VERSION1, 
   unique_token
)
client.on_message = on_message

logger.info("Подключение к брокеру...")
client.connect(broker)
client.loop_start()
logger.info("Подписка была оформлена")
client.subscribe("lab/leds/state")

while True:
    try:
        logger.info("Логи записываются...")
        if (datetime.datetime.now() - last_message_time) >= datetime.timedelta(seconds=INACTIVITY_TIMEOUT_IN_SEC):
            logger.warning("Кажется, автору стало скучно...")
        time.sleep(5)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
        logger.critical("Запись была остановлена пользователем. Пользователю тоже стало скучно...")
        break