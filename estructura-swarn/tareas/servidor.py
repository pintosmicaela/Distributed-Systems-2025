import grpc
from concurrent import futures
import mysql.connector
import tareas_pb2
import tareas_pb2_grpc
import hashlib
import time
from cryptography.fernet import Fernet
import hashlib

clave = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='
cifrador = Fernet(clave)


class TareasService(tareas_pb2_grpc.TareasServiceServicer):
    def __init__(self):
        print(f"Intentando conectar a MySQL")
        connected = False
        while not connected:
            try:
                self.conn = mysql.connector.connect(
                    host="mysql",
                    user="root",
                    password="admin",
                    database="consorcio",
                    port=3306
                )
                self.cursor = self.conn.cursor(dictionary=True)
                self.conn.autocommit = True
                connected = True
            except Exception as e:
                print(f"No se pudo conectar a MySQL, reintentando en 3s... Error: {e}")
                time.sleep(3)
        print(f"Se pudo conectar a MySQL")

    def Login(self, request, context):
        query = "SELECT password_cliente FROM clientes WHERE id_cliente=%s"
        self.cursor.execute(query, (request.cliente,))
        user = self.cursor.fetchone()

        if user:
            password_md5_db = user['password_cliente']
            try:
                # 🔓 Paso 1: Descifrar la contraseña recibida
                password_plana = cifrador.decrypt(request.password.encode()).decode()

                # 🔐 Paso 2: Hashear con MD5
                password_md5 = hashlib.md5(password_plana.encode()).hexdigest()

                # ✅ Paso 3: Comparar con la almacenada
                if password_md5 == password_md5_db:
                    return tareas_pb2.LoginResponse(success=True, mensaje_a_mostrar="Logueado")
                else:
                    return tareas_pb2.LoginResponse(success=False, mensaje_a_mostrar="Error en la contrasenia")
            except Exception as e:
                return tareas_pb2.LoginResponse(success=False, mensaje_a_mostrar="Error al procesar contraseña")
        else:
            return tareas_pb2.LoginResponse(success=False, mensaje_a_mostrar="Error en la contrasenia y/o usuario")

    def GetNews (self, request, context):
        query = "SELECT * FROM vista_obtener_noticia_reciente"
        self.cursor.execute(query,)
        new = self.cursor.fetchone()

        if new:
            return tareas_pb2.GetNewsResponse(
                titulo=new['titulo'],
                contenido=new['contenido'],
                hora=str(new['hora'])
            )
        else:
            return tareas_pb2.GetNewsResponse(
                titulo="Sin noticias recientes",
                contenido=" ",
                hora=" "
            )

    def DeleteNewNews (self, request, context):
        args_delete = [request.cliente, 0]
        result = self.cursor.callproc('eliminar_noticia_creada_recientemente', args_delete)
        print("Resultado ",result)
        eliminado = result['eliminar_noticia_creada_recientemente_arg2']

        self.conn.commit()
        

        return tareas_pb2.DeleteNewNewsResponse(
                success=bool(eliminado), 
                mensaje_a_mostrar="Noticia eliminada" if eliminado else "No se pudo eliminar"
        )   

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tareas_pb2_grpc.add_TareasServiceServicer_to_server(TareasService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print("Servidor gRPC corriendo en el puerto 50055...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
