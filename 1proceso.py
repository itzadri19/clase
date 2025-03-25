import os
import csv
import math
import time
import socket
import pickle

def es_primo(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

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
        s.sendall(pickle.dumps(numeros))
        data = pickle.loads(s.recv(4096))
    return data

def main():
    archivo_csv = "numeros_aleatorios.csv"
    numeros = leer_numeros_csv(archivo_csv)
    mitad = len(numeros) // 2
    
    numeros_1 = numeros[:mitad]
    numeros_2 = numeros[mitad:]
    
    inicio = time.time()
    primos_1 = enviar_tarea("172.20.20.159", numeros_1)
    primos_2 = enviar_tarea("172.20.20.165", numeros_2)
    primos = primos_1 + primos_2
    fin = time.time()
    
    print(f"Se encontraron {len(primos)} números primos en {fin - inicio:.4f} segundos.")

if __name__ == "__main__":
    main()
