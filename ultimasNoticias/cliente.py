import grpc
import lastnews_pb2
import lastnews_pb2_grpc
from cryptography.fernet import Fernet

def ejecutar_cliente():
    # Crear un canal inseguro al servidor
    with grpc.insecure_channel('localhost:50053') as channel:
        # Crear un stub (cliente)
        stub = lastnews_pb2_grpc.LastNewsStub(channel)

        # Crear una petición
        clave = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='
        cifrador = Fernet(clave)
        while True:
            entrada = input("Ingresá su número de documento: ").strip()
            if entrada.isdigit():
                cliente = int(entrada)  #Lo transoformo a entero
                break
            else:
                print("Ingresá un número de documento válido.")

        password = input("Ingrese su password\n")
        password = cifrador.encrypt(password.encode())
        peticion = lastnews_pb2.ClientRequest(client=cliente,passw=password)

        # Realizar la llamada RPC
        try:
            respuesta = stub.InformLastNews(peticion)
            print(f"Respuesta del servidor: \n{respuesta.news}")
        except grpc.RpcError as e:
            print(f"Error en la llamada RPC: {e.code()}: {e.details()}")

if __name__ == '__main__':
    ejecutar_cliente()