FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /covid
WORKDIR /covid
COPY requirements.txt /covid/
RUN pip install -r requirements.txt
COPY . /covid/