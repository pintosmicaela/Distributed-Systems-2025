FROM mysql:8.4

# Copia el script de inicialización al lugar correcto
COPY init.sql /docker-entrypoint-initdb.d/

# Asegurar que tenga permisos de lectura
RUN chmod 644 /docker-entrypoint-initdb.d/init.sql
