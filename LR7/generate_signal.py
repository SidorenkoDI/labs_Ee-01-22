import csv
import math
import numpy as np


CSV_FILE = "signal.csv" #наша синусоида

POINTS_COUNT = 200 #кол-во точек сигнала
FREQUENCY = 1.0 # 1 полный период за 1 сек
AMPLITUDE = 1.0
PHASE = 0.0


def main():
    time_values = np.linspace(0, 2, POINTS_COUNT)   #задается 200 точек времени в диапазоне 0 - 2

    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        #newline я использую, чтобы не было лишних пустых строк
        writer = csv.writer(file) #обьект, умеющий записывать строки в SCV файлик
        writer.writerow(["time", "value"]) #записывает заголовок в scvшнике с time value

        for t in time_values:
            y = AMPLITUDE * math.sin(2 * math.pi * FREQUENCY * t + PHASE) #значение синусоиды в момент t
            writer.writerow([round(t, 5), round(y, 5)]) #записывает строку в scv файлик с округлением до 5 знаков

    print("Файл signal.csv с синусоидой создан")


if __name__ == "__main__":
    main()