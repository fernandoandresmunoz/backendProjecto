FROM python:3.12

RUN apt-get update && rm -rf /var/lib/apt/lists/* 
ENV TZ=America/Santiago
ENV ENVIRONMENT=production
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 
RUN pip install --no-cache-dir gunicorn  
COPY . .
RUN mkdir -p /data
CMD ["gunicorn", "backend.wsgi", "--preload", "-b", "0.0.0.0:8000"]