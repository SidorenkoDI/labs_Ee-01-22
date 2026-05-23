import csv
import random
import time
from paho.mqtt import client as mqtt_client


TOPIC = "lab7/sine_signal"
CSV_FILE = "signal.csv"

BROKER = "broker.emqx.io"
PORT = 1883
CLIENT_ID = f"publisher-{random.randint(0, 10000)}"


def connect_mqtt():
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Издатель подключился к MQTT брокеру")
        else:
            print(f"Ошибка подключения, код: {reason_code}")

    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION2,
        # настройки версси callback функции, то есть функции, которая автоматом вызывается при соединении
        client_id=CLIENT_ID
    )
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def publish_signal(client): #функция которая читает scv и публикует данные в mqtt
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file) #читатель scv, обрабатывает первую строку как столбец
        #пример:time,value
         #0.0,0.0               -> {"time": "0.0", "value": "0.0"} {"time": "0.01", "value": "0.06311"}
        #0.01,0.06311


        for row in reader: #цикл по строкам scv
            message = f"{row['time']},{row['value']}"
            #row["time"] = "0.01"
            #row["value"] = "0.06311"          -> message = "0.01,0.06311", а это нужно для считывания
            # подписчиком, он там это значение будет разделять на t и y благодаря запятой
            result = client.publish(TOPIC, message, qos=1) #отправляется смс в топик; qos = 1 - доставить хотя бы 1 раз
            result.wait_for_publish() #ожидание публикации сообщения

            print(f"Отправлено: {message}")
            time.sleep(0.05)

def main():
    client = connect_mqtt()
    client.loop_start() #сетевой цикл запускается на фоне, чтобы было норм соединение


    time.sleep(0.05)
    publish_signal(client) #отправка данных

    client.loop_stop()
    client.disconnect()
    print("Публикация завершена")


if __name__ == "__main__": #запущен ли файл напрямую
    main()