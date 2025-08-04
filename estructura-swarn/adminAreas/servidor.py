import grpc
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
from concurrent import futures
from cryptography.fernet import Fernet
import logging
import areas_pb2
import areas_pb2_grpc
import signal
import sys

def manejar_ctrl_c(signal, frame):
    logger.info("Se ha presionado Ctrl+C. Finalizando el programa...")
    sys.exit(0)

signal.signal(signal.SIGINT, manejar_ctrl_c)

logger = logging.getLogger(__name__)

CLAVE = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='

class AdminAreasServicer(areas_pb2_grpc.AdminAreasServicer):
    def AddArea(self, request, context):

        cifrador = Fernet(CLAVE)
        password = cifrador.decrypt(request.passw.encode())
        passwString = password.decode("utf-8")
        areas = ""
        try:
            cnx = connection.MySQLConnection(
                host="mysql",
                user="root",
                password="admin",
                database="consorcio"
                )
        
            logger.info("Solicitud de agreagar Area {}, por usuario con id {}".format(request.area,request.client))
            nombreUsuario = ""
            if cnx and cnx.is_connected():

                with cnx.cursor() as cursor:

                    cursor.execute("SELECT nombre FROM clientes WHERE id_cliente = '{}' AND password_cliente = MD5('{}');".format(request.client, passwString))
                    for (nombre) in cursor:
                        nombreUsuario = nombre[0]
                    
                    if nombreUsuario=="":
                        logger.info("El usuario con id {} es inválido.".format(request.client))
                        return areas_pb2.Response(response="Usuario invalido")
                    else:
                        logger.info("El usuario con id {} se llama {}.".format(request.client,nombreUsuario))

                cnx.autocommit = True
                with cnx.cursor() as cursor:
                    args = [request.area.capitalize()]
                    cursor.callproc("agregar_categoria", args)
                    areas = show_categorias(cnx)

            cnx.close()
            logger.info("Solicitud de {} Ejecutada correctamente".format(nombreUsuario))
            return areas_pb2.Response(response=areas)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.info("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.info("Database does not exist")
            else:
                logger.info(err)

    def DeleteArea(self, request, context):

        cifrador = Fernet(CLAVE)
        password = cifrador.decrypt(request.passw.encode())
        passwString = password.decode("utf-8")
        areas = ""
        try:
            cnx = connection.MySQLConnection(
                host="mysql",
                user="root",
                password="admin",
                database="consorcio"
                )

            logger.info("Solicitud de eliminar Area {}, por usuario con id {}".format(request.area,request.client))
            nombreUsuario = ""
            if cnx and cnx.is_connected():

                with cnx.cursor() as cursor:

                    cursor.execute("SELECT nombre FROM clientes WHERE id_cliente = '{}' AND password_cliente = MD5('{}');".format(request.client, passwString))
                    for (nombre) in cursor:
                        nombreUsuario = nombre[0]
                    
                    if nombreUsuario=="":
                        logger.info("El usuario con id {} es inválido.".format(request.client))
                        return areas_pb2.Response(response="Usuario invalido")
                    else:
                        logger.info("El usuario con id {} se llama {}.".format(request.client,nombreUsuario))

                cnx.autocommit = True
                with cnx.cursor() as cursor:
                    args = [request.area]
                    cursor.callproc("eliminar_categoria", args)
                    areas = show_categorias(cnx)
            
            cnx.close()
            logger.info("Solicitud de {} Ejecutada correctamente".format(nombreUsuario))
            return areas_pb2.Response(response=areas)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.info("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.info("Database does not exist")
            else:
                logger.info(err)
    
    def ShowAreas(self, request, context):
        areas = ""
        cifrador = Fernet(CLAVE)
        password = cifrador.decrypt(request.passw.encode())
        passwString = password.decode("utf-8")
        logger.info("id: {}, password {}".format(request.client,passwString))

        try:
            cnx = connection.MySQLConnection(
                host="mysql",
                user="root",
                password="admin",
                database="consorcio"
                )
            
            logger.info("Solicitud de mostrar Areas por usuario con id {}".format(request.client))
            nombreUsuario = ""
            if cnx and cnx.is_connected():

                with cnx.cursor() as cursor:

                    cursor.execute("SELECT nombre FROM clientes WHERE id_cliente = '{}' AND password_cliente = MD5('{}');".format(request.client, passwString))
                    for (nombre) in cursor:
                        nombreUsuario = nombre[0]
                    
                    if nombreUsuario=="":
                        logger.info("El usuario con id {} es inválido.".format(request.client))
                        return areas_pb2.Response(respones="Usuario invalido")
                    else:
                        logger.info("El usuario con id {} se llama {}.".format(request.client,nombreUsuario))

                    areas = show_categorias(cnx)
        
            cnx.close()
            logger.info("Areas:",areas)
            return areas_pb2.Response(response=areas)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.exception("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.exception("Database does not exist")
            else:
                logger.error(err)

def show_categorias(cnx):
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            areas = "Areas:\n"
            cursor.execute("SELECT nombre_categoria FROM vista_categorias_disponibles;")
            for nombre_categoria in cursor:
                areas = areas + " - " + nombre_categoria[0] + "\n"
            return areas
    else:
        logger.info("No se pudo ejecutar la operacion, se perdio la conexión a la base de datos")
        return "No se pudo ejecutar la operacion, se perdio la conexión a la base de datos"

def iniciar_servidor():
    logging.basicConfig(filename='adminAreas.log', level=logging.INFO)
    logger.info('Started')
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    areas_pb2_grpc.add_AdminAreasServicer_to_server(
        AdminAreasServicer(), servidor
    )
    logger.info("Servidor gRPC escuchando en el puerto 50054...")
    servidor.add_insecure_port('[::]:50054')
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()