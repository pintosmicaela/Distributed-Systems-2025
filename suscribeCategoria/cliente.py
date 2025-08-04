import grpc
import suscribecat_pb2
import suscribecat_pb2_grpc
from cryptography.fernet import Fernet

def ejecutar_cliente():
    # Crear un canal inseguro al servidor
    with grpc.insecure_channel('localhost:50056') as channel:
        # Crear un stub (cliente)
        stub = suscribecat_pb2_grpc.SuscribeStub(channel)

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
        seccion = input("Ingrese la contraseña donde se quiere suscribir\n")
        peticion = suscribecat_pb2.ClientRequest(client=cliente,passw=password,seccion=seccion)

        # Realizar la llamada RPC
        try:
            respuesta = stub.SuscribeCategoria(peticion)
            print(f"Respuesta del servidor: \n{respuesta.response}")
        except grpc.RpcError as e:
            print(f"Error en la llamada RPC: {e.code()}: {e.details()}")

if __name__ == '__main__':
    ejecutar_cliente()