import grpc
import agente_pb2
import agente_pb2_grpc

import lastnews_pb2
import lastnews_pb2_grpc

import tareas_pb2
import tareas_pb2_grpc

import areas_pb2
import areas_pb2_grpc

import enviarnoticia_pb2
import enviarnoticia_pb2_grpc

import suscribecat_pb2
import suscribecat_pb2_grpc

from concurrent import futures

# Implementación del servicio Servicio_Agente
class ServicioAgenteServicer(agente_pb2_grpc.Servicio_AgenteServicer):
    def EnviarNoticia(self, request, context):
        print(f"Solicitud de enviar una nueva noticia por parte del cliente {request.cliente_id} con titulo {request.titulo}")
        with grpc.insecure_channel('enviarnoticia:50056') as channel:
            stub = enviarnoticia_pb2_grpc.EnviarNoticiaStub(channel)
            # Crear el mensaje de solicitud
            requestEnviarNoticia = enviarnoticia_pb2.ClientRequest(
                client=request.cliente_id,
                passw=request. password ,
                titulo=request.titulo,
                contenido=request.contenido,
                seccion=request.area,
            )
            # Llamar al método SendNews
            response = stub.SendNews(requestEnviarNoticia)
            return agente_pb2.RespuestaEnviarNoticia(respuesta=response.response)
            

    def ObtenerNoticiasUltimas24hs(self, request, context):
        print(f"Solicitud de noticias delas ultimas 24hs recibida de usuario: {request.nombre_usuario}")
        with grpc.insecure_channel('lastnews:50053') as channel:    
            stubLastNews = lastnews_pb2_grpc.LastNewsStub(channel)
            requestLastNews = lastnews_pb2.ClientRequest(client=request.nombre_usuario,passw=request.password)
            responseLastNews = stubLastNews.InformLastNews(requestLastNews)
            return agente_pb2.noticiasInfo(mensaje=responseLastNews.news)
    
    def Login(self, request,context):
        print(f"Solicitud de Login recibida de usuario: {request.dni}")
        channel = grpc.insecure_channel('tareas:50055') 
        stub = tareas_pb2_grpc.TareasServiceStub(channel)
        response = stub.Login(tareas_pb2.LoginRequest(cliente=request.dni, password=request.password))
        return agente_pb2.ResultadoLogin(resultado=response.success)

    def AgregarCategoria(self, request, context):
        print(f"Se solicito la agregacion de una categoria por parte del usuario {request.cliente_id}")
        with grpc.insecure_channel('adminareas:50054') as channel:
            stub = areas_pb2_grpc.AdminAreasStub(channel)
            requestAddArea = areas_pb2.ClientRequest(
                client=request.cliente_id,
                passw=request.password,
                area=request.area
                )
            response = stub.AddArea(requestAddArea)
            return  agente_pb2.ResultadoAgregarCategoria(respuesta = response.response)

    def VerCategoriasInscripto(self, request, context):
        print(f"Se solicito ver categorias a las que esta inscripto por parte del usuarioÑ {request.cliente_id}")
        with grpc.insecure_channel('adminareas:50054') as channel:
            stub = areas_pb2_grpc.AdminAreasStub(channel)
            requestShowAreas = areas_pb2.AreasRequest(
                client=request.cliente_id,
                passw=request.password
                )
            response = stub.ShowAreas(requestShowAreas)
            return  agente_pb2.RespuestaCategoriaInscripto(respuesta = response.response)
    
    def BorrarArea(self, request, context):
        print(f"Se solicito borrar la categoria {request.area} por parte del cliente {request.cliente_id}")
        with grpc.insecure_channel('adminareas:50054') as channel:
            stub = areas_pb2_grpc.AdminAreasStub(channel)
            requestDeleteArea = areas_pb2.ClientRequest(
                client=request.cliente_id,
                passw=request.password,
                area = request.area
                )
            response = stub.DeleteArea(requestDeleteArea)
            return  agente_pb2.RespuestaCategoriaInscripto(respuesta = response.response)

    def SuscribirNuevaCategoria(self, request, context):
        print(f"Se solicito la suscripcion a una suscripcion a la categoria {request.area} del usuario {request.cliente_id} ")
        with grpc.insecure_channel('suscribecat:50057') as channel:
            stub = suscribecat_pb2_grpc.SuscribeStub(channel) 
            peticion = suscribecat_pb2.ClientRequest(client=request.cliente_id,passw=request.password,seccion=request.area)   
            respuesta = stub.SuscribeCategoria(peticion)
            return agente_pb2.noticiasInfo(mensaje=respuesta.response)
    
    def ObtenerUltimasNoticias(self, request, context):
        print(f"Se solicitaron las ultimas noticias de la categoria {request.area} por parte del usuario {request.cliente_id}")
        channel = grpc.insecure_channel('tareas:50055') 
        stub = tareas_pb2_grpc.TareasServiceStub(channel)
        response = stub.GetNews(tareas_pb2.GetNewsRequest(cliente=request.cliente_id))
        noticia_str = f"Título: {response.titulo}\nContenido: {response.contenido}\nHora: {response.hora}"
        return agente_pb2.noticiasInfo(mensaje=noticia_str)

def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agente_pb2_grpc.add_Servicio_AgenteServicer_to_server(ServicioAgenteServicer(), server)
    server.add_insecure_port('[::]:50052')  # Aquí definís el puerto del servidor agente
    server.start()
    print("Servidor Servicio_Agente escuchando en el puerto 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    servir()
