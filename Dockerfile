# syntax=docker/dockerfile:1
FROM python:3.10.2
#for see the result in terminals
ENV PYTHONUNBUFFERED=1   

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

CMD ["python3" , "manage.py" , "runserver" , "0.0.0.0:8000"]