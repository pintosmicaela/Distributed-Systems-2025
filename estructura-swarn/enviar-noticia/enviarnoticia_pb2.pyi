from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ClientRequest(_message.Message):
    __slots__ = ("client", "passw", "titulo", "contenido", "seccion")
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    PASSW_FIELD_NUMBER: _ClassVar[int]
    TITULO_FIELD_NUMBER: _ClassVar[int]
    CONTENIDO_FIELD_NUMBER: _ClassVar[int]
    SECCION_FIELD_NUMBER: _ClassVar[int]
    client: int
    passw: str
    titulo: str
    contenido: str
    seccion: str
    def __init__(self, client: _Optional[int] = ..., passw: _Optional[str] = ..., titulo: _Optional[str] = ..., contenido: _Optional[str] = ..., seccion: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...
