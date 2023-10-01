FROM python:3.10

COPY requirements.txt /temp/requirements.txt
COPY api_image /api_image

WORKDIR /api_image

# Устанавливаем зависимости через pip
RUN pip install -r /temp/requirements.txt

EXPOSE 8000

RUN adduser --disabled-password service-user

USER service-user
