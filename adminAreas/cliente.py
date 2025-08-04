import grpc
import areas_pb2
import areas_pb2_grpc
from cryptography.fernet import Fernet

def ejecutar_cliente():
    # Crear un canal inseguro al servidor
    with grpc.insecure_channel('localhost:50054') as channel:
        # Crear un stub (cliente)
        stub = areas_pb2_grpc.AdminAreasStub(channel)

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

        # AGREAGAR AREA
        password = input("Ingrese su password\n")
        password = cifrador.encrypt(password.encode())
        area = input("Ingrese el nombre la nueva Area\n")
        peticion = areas_pb2.ClientRequest(client=cliente,passw=password,area=area)

        # Realizar la llamada RPC
        try:
            respuesta = stub.AddArea(peticion)
            print(f"Respuesta del servidor: \n{respuesta.response}")
        except grpc.RpcError as e:
            print(f"Error en la llamada RPC: {e.code()}: {e.details()}")
        
        # # ELIMINAR AREA
        # password = input("Ingrese su password\n")
        # password = cifrador.encrypt(password.encode())
        # area = input("Ingrese el nombre del Area a eliminar\n")
        # peticion = areas_pb2.ClientRequest(client=cliente,passw=password,area=area)

        # # Realizar la llamada RPC
        # try:
        #     respuesta = stub.DeleteArea(peticion)
        #     print(f"Respuesta del servidor: \n{respuesta.response}")
        # except grpc.RpcError as e:
        #     print(f"Error en la llamada RPC: {e.code()}: {e.details()}")
        
        # # MOSTRAR AREAS
        # password = input("Ingrese su password\n")
        # password = cifrador.encrypt(password.encode())
        # peticion = areas_pb2.ClientRequest(client=cliente,passw=password)

        # Realizar la llamada RPC
        # try:
        #     respuesta = stub.ShowAreas(peticion)
        #     print(f"Respuesta del servidor: \n{respuesta.response}")
        # except grpc.RpcError as e:
        #     print(f"Error en la llamada RPC: {e.code()}: {e.details()}")

if __name__ == '__main__':
    ejecutar_cliente()