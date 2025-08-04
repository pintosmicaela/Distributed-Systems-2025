from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClienteArea(_message.Message):
    __slots__ = ("cliente_id", "area", "password")
    CLIENTE_ID_FIELD_NUMBER: _ClassVar[int]
    AREA_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    cliente_id: int
    area: str
    password: str
    def __init__(self, cliente_id: _Optional[int] = ..., area: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class Respuesta(_message.Message):
    __slots__ = ("mensaje", "exito")
    MENSAJE_FIELD_NUMBER: _ClassVar[int]
    EXITO_FIELD_NUMBER: _ClassVar[int]
    mensaje: str
    exito: bool
    def __init__(self, mensaje: _Optional[str] = ..., exito: bool = ...) -> None: ...

class Noticia(_message.Message):
    __slots__ = ("titulo", "contenido", "fecha")
    TITULO_FIELD_NUMBER: _ClassVar[int]
    CONTENIDO_FIELD_NUMBER: _ClassVar[int]
    FECHA_FIELD_NUMBER: _ClassVar[int]
    titulo: str
    contenido: str
    fecha: str
    def __init__(self, titulo: _Optional[str] = ..., contenido: _Optional[str] = ..., fecha: _Optional[str] = ...) -> None: ...

class ListaNoticias(_message.Message):
    __slots__ = ("noticias",)
    NOTICIAS_FIELD_NUMBER: _ClassVar[int]
    noticias: _containers.RepeatedCompositeFieldContainer[Noticia]
    def __init__(self, noticias: _Optional[_Iterable[_Union[Noticia, _Mapping]]] = ...) -> None: ...
