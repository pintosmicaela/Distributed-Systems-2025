import grpc
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
from concurrent import futures
from cryptography.fernet import Fernet
import logging
import suscribecat_pb2
import suscribecat_pb2_grpc
import signal
import sys

def manejar_ctrl_c(signal, frame):
    logger.info("Se ha presionado Ctrl+C. Finalizando el programa...")
    sys.exit(0)

signal.signal(signal.SIGINT, manejar_ctrl_c)

logger = logging.getLogger(__name__)

CLAVE = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='

class SuscribeServicer(suscribecat_pb2_grpc.SuscribeServicer):
    def SuscribeCategoria(self, request, context):

        cifrador = Fernet(CLAVE)
        password = cifrador.decrypt(request.passw.encode())
        passwString = password.decode("utf-8")

        try:
            cnx = connection.MySQLConnection(
                host="mysql",
                user="root",
                password="admin",
                database="consorcio"
                )

            logger.info("Solicitud de ultimas noticias realizada por usuario con id {}".format(request.client))
            noticias = ""
            nombreUsuario = ""
            if cnx and cnx.is_connected():

                with cnx.cursor() as cursor:

                    cursor.execute("SELECT nombre FROM clientes WHERE id_cliente = '{}' AND password_cliente = MD5('{}');".format(request.client, passwString))
                    for (nombre) in cursor:
                        nombreUsuario = nombre[0]

                    if nombreUsuario=="":
                        logger.info("El usuario con id {} es inválido.".format(request.client))
                        return suscribecat_pb2.Response(news="Usuario invalido")
                    else:
                        logger.info("El usuario con id {} se llama {}.".format(request.client,nombreUsuario))

                    cnx.autocommit = True
                    id_cat = ""
                    cursor.execute("SELECT id_categoria FROM categorias WHERE nombre = '{}';".format(request.seccion.capitalize()))
                    for (id_categoria) in cursor:
                        id_cat = id_categoria[0]
                    
                    if id_cat=="":
                        logger.info("El area {} no se encuentra regitrada.".format(request.seccion))
                        return suscribecat_pb2.Response(response="Nombre de categoria no registrado")

                    args = [request.client,id_cat]
                    cursor.callproc("suscribir_cliente_categoria", args)

            cnx.close()
            logger.info("Solicitud de {} Ejecutada correctamente".format(nombreUsuario))
            return suscribecat_pb2.Response(response="Suscripcion agregada correctamente")
        
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.info("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.info("Database does not exist")
            else:
                logger.info(err)

def iniciar_servidor():
    logging.basicConfig(filename='suscribeCategoria.log', level=logging.INFO)
    logger.info('Started')
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    suscribecat_pb2_grpc.add_SuscribeServicer_to_server(
        SuscribeServicer(), servidor
    )
    logger.info("Servidor gRPC escuchando en el puerto 50056...")
    servidor.add_insecure_port('[::]:50056')
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()