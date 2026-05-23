import random
import matplotlib.pyplot as plt
from paho.mqtt import client as mqtt_client


BROKER = "broker.emqx.io" #Это адрес MQTT-брокера ! Брокер — сервер, через который проходят сообщения.
PORT = 1883
# "подключись к MQTT-серверу broker.emqx.io через порт 1883"
TOPIC = "lab7/sine_signal" #Топик, то есть тема/канал сообщений.

CLIENT_ID = f"subscriber-{random.randint(0, 10000)}" #создается случ имя клиента
#например у подписчика создается номер 3912, для чего это делается, да чтобы у клиентов не были
#одинаковык ID

time_values = []
signal_values = []

def connect_mqtt(): #Функция подключения к MQTT брокеру.
#нижняя функция подключения вызывается автоматически когда клиент подкл к брокеру
    def on_connect(client, userdata, flags, reason_code, properties):
        #функция-обработчик подключения к MQTT-брокеру, вызывает не сам
        #пользователь, а библ-ка paho-mqtt,когда брокер клиент подкл к брокеру
        #userdata - пользоват данные(доп инфа), flags - служебные флаги подкл, доп инфа о подкл
        #reason - рез-тат подкла, properties - доп свойства брокера
        if reason_code == 0:
            print("Подписчик подключился к MQTT брокеру")
            client.subscribe(TOPIC, qos=1) #программка подписывается на топик
            print(f"Подписка на топик: {TOPIC}")
        else:
            print(f"Ошибка подключения, код: {reason_code}")


#---Создание mqtt клиента с ID и сохранение его в переменную client---

    client = mqtt_client.Client( #создание MQTT клиента
#класс из библиотеки paho-mqt
        mqtt_client.CallbackAPIVersion.VERSION2,
        #настройки версси callback функции, то есть функции, которая автоматом вызывается при соединении
        client_id=CLIENT_ID #передали имя клиента
    )
    client.on_connect = on_connect #назначается функция которая сработает при подключении.
    client.connect(BROKER, PORT) #создался клиентик
    return client


def on_message(client, userdata, message):
#эта функция вызывается автоматически когда пришло новое сообщение
    text = message.payload.decode()
#достается текст из mqtt смс в виде байтов (например b"0.01,0.06311") и decode превращает это в стр "0.01,0.06311"
    t, y = text.split(",") #разделение строки по запятой, потому что
# у нас на выходе идет сообщение 0.01,0.06311, но это совокупность время + y, а нужно разделить
#0.01 = t и 0.06311 = y
# добавляем время и y в список
    time_values.append(float(t))
    signal_values.append(float(y))

    print(f"Получено: t={t}, y={y}")


def main():
    client = connect_mqtt() #подкл к брокеру
    client.on_message = on_message #назначение обработчика сообщений
    client.loop_start() #запуск клиента в фоновом режиме

    #подключаем интерактивный режим графика + создание окна графики
    plt.ion()
    fig, ax = plt.subplots()
    #fig - фигура целиком ax = область, где рисуется график

    try:
        while True: #запустил беск цикл обновления графика
            ax.clear()
            ax.plot(time_values, signal_values, color="blue")
            ax.set_title("Синусоида, полученная через MQTT")
            ax.set_xlabel("Время, с")
            ax.set_ylabel("Значение сигнала")
            ax.grid(True)
            plt.pause(0.2)
    #Ctrl + C = аккуратненько остановить программу
    except KeyboardInterrupt:
        print("Подписчик остановлен")
# остановка цикла
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()