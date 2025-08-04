﻿# -*- coding: utf-8 -*-
import grpc
from cryptography.fernet import Fernet
import sys
sys.path.append('/home/fedoras/noticias_consorcio/cliente')
import suscripciones_noticias_pb2 as pb2
import suscripciones_noticias_pb2_grpc as pb2_grpc

CLAVE_FERNET = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='
cifrador = Fernet(CLAVE_FERNET)

def run():
    channel = grpc.insecure_channel("localhost:50055")
    stub = pb2_grpc.SuscripcionesNoticiasStub(channel)

    # while True:
    #     entrada = input("Ingresá su número de documento: ").strip()
    #     if entrada.isdigit():
    #         id_cliente = int(entrada)  #Lo transoformo a entero
    #         break
    #     else:
    #         print("Ingresá un número de documento válido.")
    password = "prueba"
    password_cifrado = cifrador.encrypt(password.encode())

    # area = input("Ingrese el nuevo area\n")
    # resp1 = stub.SubscribirCliente(pb2.ClienteArea(
    #     cliente_id=41460004,
    #     area=area,
    #     password=password_cifrado
    # ))
    # print("SubscribirCliente:", resp1.mensaje)

    area = input("Ingrese el area a desuscribir\n")
    resp2 = stub.BorrarSuscripcion(pb2.ClienteArea(
        cliente_id=41460004,
        area=area,
        password=password_cifrado
    ))
    print("BorrarSuscripcion:", resp2.mensaje)

    # lista = stub.ObtenerClientesPorArea(pb2.area(nombre="Deportiva"))
    # print("Clientes en Deportiva:", lista.clientes)

    # area = input("Ingrese el area a desuscribir\n")
    # noticias = stub.ObtenerNoticiasDeArea(pb2.ClienteArea(
    #     cliente_id=41460004,
    #     area=area,
    #     password=password_cifrado
    # ))
    # print("noticias:",noticias)
    # for n in noticias.noticias:
    #     print(f"[{n.fecha}] {n.titulo}: {n.contenido}")

if __name__ == "__main__":
    run()
