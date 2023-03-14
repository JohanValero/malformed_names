# Este archivo Docker utiliza una imagen de Python 3.10.5 slim bullseye como base.
# Luego, se crea un directorio llamado "wd" y se establece como directorio de trabajo actual.
# Se copia el archivo requirements.txt al directorio actual y se instalan todas las dependencias
# necesarias utilizando pip (instalador de libreias python).
# A continuación, se copian todos los archivos y directorios del contexto de construcción actual
# al directorio actual.
# Finalmente, se ejecuta el comando CMD que inicia la aplicación usando gunicorn (servidor web en python).
# La aplicación se ejecuta con M trabajadores y N subprocesos.
# La aplicación se une a la dirección IP del host y al puerto especificado en la variable de
# entorno $PORT (definida por Google Cloud Run), y utiliza el módulo principal llamado "app".

# Imagen base: Python 3.10.5 slim (basado en Debian Bullseye)
FROM python:3.10.5-slim-bullseye

# Crear un directorio de trabajo dentro del contenedor y definirlo como directorio de trabajo.
RUN mkdir wd
WORKDIR /wd

# Copiar el archivo requirements.txt al contenedor y ejecutar pip para instalar las dependencias.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar todo el contenido actual en el directorio de trabajo dentro del contenedor.
COPY ./ ./

# Iniciar la aplicación usando gunicorn con 4 workers y 2 threads, escuchando en el puerto
# especificado en la variable de entorno $PORT.
CMD exec gunicorn --workers=4 --threads=1 -b :$PORT main:app