import os
import csv
import time
import socket
import pickle

def leer_numeros_csv(nombre_archivo):
    numeros = []
    try:
        with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                for valor in fila:
                    try:
                        numeros.append(int(valor))
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encuentra en el directorio actual.")
    return numeros

def enviar_tarea(ip, numeros):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, 5000))
        # Enviar datos
        serialized_data = pickle.dumps(numeros)
        s.sendall(len(serialized_data).to_bytes(4, 'big'))  # Enviar tamaño
        s.sendall(serialized_data)  # Enviar datos
        # Recibir respuesta
        data_size = int.from_bytes(s.recv(4), 'big')
        data = b""
        while len(data) < data_size:
            packet = s.recv(4096)
            if not packet:
                break
            data += packet
        return pickle.loads(data)

def main():
    archivo_csv = "numeros_aleatorios.csv"
    numeros = leer_numeros_csv(archivo_csv)
    
    # Dividir los números en tres partes para enviarlos a tres equipos diferentes
    mitad = len(numeros) // 3
    numeros_1 = numeros[:mitad]
    numeros_2 = numeros[mitad:mitad*2]
    numeros_3 = numeros[mitad*2:]
    
    # Direcciones IP de los tres equipos
    ip_equipo_1 = "172.20.20.159"
    ip_equipo_2 = "172.20.20.165"
    ip_equipo_3 = "172.20.20.185"
    
    inicio = time.time()
    primos_1 = enviar_tarea(ip_equipo_1, numeros_1)
    primos_2 = enviar_tarea(ip_equipo_2, numeros_2)
    primos_3 = enviar_tarea(ip_equipo_3, numeros_3)
    
    primos = primos_1 + primos_2 + primos_3
    fin = time.time()
    
    print(f"Se encontraron {len(primos)} números primos en {fin - inicio:.4f} segundos.")

if __name__ == "__main__":
    main()
