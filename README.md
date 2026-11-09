# Portal de noticias distribuido (Consorcio)

Proyecto de la materia **Sistemas Distribuidos** (UNS, 2025). Consiste en un portal de noticias construido como un conjunto de **microservicios en Python que se comunican por gRPC**, con persistencia en **MySQL** y despliegue en contenedores **Docker** orquestados con **Docker Swarm**.

**Stack:** Python · gRPC / Protocol Buffers · MySQL 8.4 · Docker · Docker Compose / Swarm

## Arquitectura

Un servicio **agente** actúa como punto de entrada: recibe las solicitudes de los clientes y las reenvía por gRPC al servicio que corresponde. Cada servicio corre en su propio contenedor y puede replicarse de forma independiente.

```
                        ┌───────────────┐
   Cliente (gRPC) ───▶  │    agente     │  :50052
                        └──────┬────────┘
        ┌───────────┬──────────┼─────────────┬───────────────┐
        ▼           ▼          ▼             ▼               ▼
    lastnews    adminareas   tareas     enviarnoticia    suscribecat
     :50053       :50054     :50055        :50056          :50057
        └───────────┴──────────┴─────────────┴───────────────┘
                               ▼
                         MySQL (consorcio)
```

| Servicio | Puerto | Responsabilidad |
|---|---|---|
| `agente` | 50052 | Punto de entrada; enruta las solicitudes a los demás servicios |
| `lastnews` | 50053 | Consulta de las últimas noticias |
| `adminareas` | 50054 | Alta, baja y consulta de categorías (áreas) |
| `tareas` | 50055 | Login de clientes y gestión de noticias |
| `enviarnoticia` | 50056 | Publicación de noticias |
| `suscribecat` | 50057 | Suscripción y baja de suscripción a categorías |
| `mysql` | 3306 | Base de datos `consorcio` |

Los contratos de los servicios están definidos con Protocol Buffers (por ejemplo `agente/agente.proto` y `tareas/tareas.proto`).

## Funcionalidades

- Login de clientes.
- Enviar una noticia.
- Obtener las últimas noticias y las de las últimas 24 horas.
- Agregar y borrar una categoría.
- Suscribirse y desuscribirse de una categoría; ver las categorías a las que se está suscripto.

## Base de datos

El esquema se crea con `base-de-datos/init.sql` e incluye las tablas `clientes`, `categorias`, `noticias`, `cliente_categoria`, `cliente_noticia` y `noticia_categoria`.

## Estructura del repositorio

```
.
├── docs/                  # Enunciado e informe del proyecto (PDF)
└── estructura-swarn/
    ├── docker-compose.yml # Definición del stack (Swarm)
    ├── base-de-datos/     # init.sql y compose de MySQL
    ├── agente/
    ├── adminAreas/
    ├── last-news/
    ├── tareas/
    ├── enviar-noticia/
    └── suscribecat/
```

## Cómo ejecutarlo

Requisitos: Docker (con Swarm habilitado).

```bash
cd estructura-swarn

# 1. Construir las imágenes de cada servicio
docker build -t agente         ./agente
docker build -t lastnews       ./last-news
docker build -t adminareas     ./adminAreas
docker build -t tareas         ./tareas
docker build -t enviarnoticia  ./enviar-noticia
docker build -t suscribecat    ./suscribecat

# 2. Generar una clave de cifrado (Fernet) y exportarla como variable de entorno
export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

# 3. Inicializar Swarm (una sola vez) y desplegar el stack
docker swarm init
docker stack deploy -c docker-compose.yml consorcio

# 4. Verificar los servicios
docker service ls
```

La clave de cifrado no está en el repositorio: se lee de la variable de entorno `FERNET_KEY`, que deben compartir los servicios y el cliente (`adminAreas/cliente.py`).

Para escalar un servicio (por ejemplo, el agente):

```bash
docker service scale consorcio_agente=3
```

Cada servicio también puede levantarse de forma individual; ver el `Readme.md` dentro de `adminAreas/` y `last-news/`.

## Documentación

En la carpeta [`docs/`](docs/) están el enunciado (`SegundoProyecto-2025.pdf`) y el informe (`Informe.pdf`).

## Autora

**Micaela Luján Pintos** · [LinkedIn](https://linkedin.com/in/mlpintos) · [GitHub](https://github.com/pintosmicaela)
