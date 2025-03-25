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

def manejar_conexion(conexion):
    # Recibir los datos del cliente
    data_size = int.from_bytes(conexion.recv(4), 'big')
    data = b""
    
    while len(data) < data_size:
        packet = conexion.recv(4096)
        if not packet:
            break
        data += packet

    # Procesar los números recibidos
    numeros = pickle.loads(data)
    primos = [n for n in numeros if es_primo(n)]
    
    # Enviar la respuesta al cliente
    response_data = pickle.dumps(primos)
    conexion.sendall(len(response_data).to_bytes(4, 'big'))  # Enviar tamaño
    conexion.sendall(response_data)  # Enviar datos

    conexion.close()

def iniciar_servidor():
    host = "0.0.0.0"  # Escuchar en todas las interfaces
    puerto = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((host, puerto))
        servidor.listen()
        print(f"Servidor escuchando en el puerto {puerto}...")
        
        while True:
            conexion, _ = servidor.accept()
            print("Conexión recibida")
            manejar_conexion(conexion)

if __name__ == "__main__":
    iniciar_servidor()
