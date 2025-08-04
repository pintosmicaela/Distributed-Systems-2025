FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50055

# Comando para ejecutar tu servidor
CMD ["python", "miembro.py"]
