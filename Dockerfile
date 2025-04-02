FROM python:3.9

WORKDIR /Mybits2

COPY . .


RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

#CMD ["gunicorn", "--bind", "0.0.0.0:8002", "--workers", "3", "Mybits2.wsgi:application"]
#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]