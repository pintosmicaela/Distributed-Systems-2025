import grpc
import enviarnoticia_pb2
import enviarnoticia_pb2_grpc
from cryptography.fernet import Fernet

def ejecutar_cliente():
    # Crear un canal inseguro al servidor
    with grpc.insecure_channel('localhost:50055') as channel:
        # Crear un stub (cliente)
        stub = enviarnoticia_pb2_grpc.EnviarNoticiaStub(channel)

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

        # AGREAGAR NOTICIA
        password = input("Ingrese su password\n")
        password = cifrador.encrypt(password.encode())
        area = input("Ingrese la seccion de la nueva noticia\n")
        titulo = input("Ingrese el titulo de la nueva noticia\n")
        contenido = input("Ingrese el contenido de la nueva noticia\n")
        peticion = enviarnoticia_pb2.ClientRequest(client=cliente,passw=password,titulo=titulo,contenido=contenido,seccion=area)

        # Realizar la llamada RPC
        try:
            respuesta = stub.SendNews(peticion)
            print(f"Respuesta del servidor: \n{respuesta.response}")
        except grpc.RpcError as e:
            print(f"Error en la llamada RPC: {e.code()}: {e.details()}")

if __name__ == '__main__':
    ejecutar_cliente()