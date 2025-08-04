import grpc
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
from concurrent import futures
from cryptography.fernet import Fernet
import logging
import enviarnoticia_pb2
import enviarnoticia_pb2_grpc
import signal
import sys

def manejar_ctrl_c(signal, frame):
    logger.info("Se ha presionado Ctrl+C. Finalizando el programa...")
    sys.exit(0)

signal.signal(signal.SIGINT, manejar_ctrl_c)

logger = logging.getLogger(__name__)

CLAVE = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='

class EnviarNoticiaServicer(enviarnoticia_pb2_grpc.EnviarNoticiaServicer):
    def SendNews(self, request, context):

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
        
            logger.info("Solicitud de agreagar Area {}, por usuario con id {}".format(request.seccion,request.client))
            nombreUsuario = ""
            result = False
            if cnx and cnx.is_connected():

                with cnx.cursor() as cursor:

                    cursor.execute("SELECT nombre FROM clientes WHERE id_cliente = '{}' AND password_cliente = MD5('{}');".format(request.client, passwString))
                    for (nombre) in cursor:
                        nombreUsuario = nombre[0]
                    
                    if nombreUsuario=="":
                        logger.info("El usuario con id {} es inválido.".format(request.client))
                        return enviarnoticia_pb2.Response(response="Usuario invalido")
                    else:
                        logger.info("El usuario con id {} se llama {}.".format(request.client,nombreUsuario))

                cnx.autocommit = True
                with cnx.cursor() as cursor:
                    id_cat = ""
                    cursor.execute("SELECT id_categoria FROM categorias WHERE nombre = '{}';".format(request.seccion))
                    for (id_categoria) in cursor:
                        id_cat = id_categoria[0]
                    
                    if id_cat=="":
                        logger.info("El area {} no se encuentra regitrada.".format(request.client))
                        return enviarnoticia_pb2.Response(response="Nombre de categoria no registrado")

                    args = [request.client,id_cat,request.titulo,request.contenido,0]
                    result = cursor.callproc("crear_noticia", args)

                    cnx.close()
                    logger.info("Solicitud de {} ejecutada".format(nombreUsuario))
                    if result[4]==1:
                        return enviarnoticia_pb2.Response(response="Noticia creada correctamente.")
                    else:
                        return enviarnoticia_pb2.Response(response="La noticia no se pudo crear.")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.info("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.info("Database does not exist")
            else:
                logger.info(err)

def iniciar_servidor():
    logging.basicConfig(filename='enviarNoticia.log', level=logging.INFO)
    logger.info('Started')
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    enviarnoticia_pb2_grpc.add_EnviarNoticiaServicer_to_server(
        EnviarNoticiaServicer(), servidor
    )
    logger.info("Servidor gRPC escuchando en el puerto 50055...")
    servidor.add_insecure_port('[::]:50055')
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()