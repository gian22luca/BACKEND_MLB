FROM python:3.12-alpine  


WORKDIR /app

RUN apk add --no-cache \
    build-base \
    mariadb-dev \
    jpeg-dev \
    zlib-dev \
    openjpeg-dev \
    curl
    
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

RUN mkdir -p /app/static_files /app/logs 

RUN adduser -D vixeluser


RUN chown -R vixeluser:vixeluser /app
RUN chmod -R 755 /app

USER vixeluser

EXPOSE 8000

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]


