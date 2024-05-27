import time
import datetime
import board
import adafruit_dht
import csv
from os.path import expanduser
import matplotlib.pyplot as plt
import mpld3

# Sensor data pin is connected to GPIO 4
# sensor = adafruit_dht.DHT22(board.D4)
# Uncomment for DHT11
sensor = adafruit_dht.DHT11(board.D23)

# Lista de tuplas para almacenar datos
data_list = []

tiempo_inicio = time.time()
tiempo_maximo = 20  # segundos

while (time.time() - tiempo_inicio) < tiempo_maximo:
    try:
        # Obtener datos del sensor
        temperatura_c = sensor.temperature
        temperatura_f = temperatura_c * (9 / 5) + 32
        humedad = sensor.humidity
        
        # Obtener fecha y hora actual
        fecha_hora_actual = datetime.datetime.now()
        
        # Almacenar datos en la lista de tuplas
        data_list.append((fecha_hora_actual, temperatura_c, temperatura_f, humedad))
        
        print("Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humedad={2:0.1f}%".format(temperatura_c, temperatura_f, humedad))

    except RuntimeError as error:
        # Los errores son comunes, los DHT son difíciles de leer, continúa
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(3.0)

# Guardar los datos en un archivo CSV
nombre_archivo = expanduser("~/Desktop/datos_sensor.csv")

with open(nombre_archivo, mode='w', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(['Fecha y Hora', 'Temperatura (ºC)', 'Temperatura (ºF)', 'Humedad (%)'])
    for data in data_list:
        writer.writerow(data)

print("Datos guardados en:", nombre_archivo)

# Función para filtrar los datos por día
def filter_by_day(day):
    filtered_data = [data for data in data_list if data[0].date() == day]
    return filtered_data

# Función para filtrar los datos por hora
def filter_by_hour(hour):
    filtered_data = [data for data in data_list if data[0].hour == hour]
    return filtered_data

# Graficar los datos
plt.plot([data[0] for data in data_list], [data[1] for data in data_list], label='Temperatura (ºC)')
plt.plot([data[0] for data in data_list], [data[3] for data in data_list], label='Humedad (%)')
plt.xlabel('Tiempo')
plt.ylabel('Valor')
plt.title('Datos del sensor DHT11 durante {} segundos'.format(tiempo_maximo))
plt.legend()
plt.grid(True)

# Convertir la figura de matplotlib a un objeto HTML para mostrar en el navegador
grafico_html = mpld3.fig_to_html(plt.gcf())

# Guardar el HTML en un archivo
nombre_html = expanduser("~/Desktop/grafico_sensor.html")
with open(nombre_html, "w") as f:
    f.write(grafico_html)

# Abrir el archivo HTML en el navegador predeterminado
import webbrowser
webbrowser.open("file://" + nombre_html)
