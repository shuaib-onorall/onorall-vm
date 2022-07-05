
#FROM python:3.10.2
#for see the result in terminals
# FROM python:3.10.2-alpine

FROM python:3.10.2 as python
ENV PYTHODONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1   

RUN mkdir /app
WORKDIR /app
RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /app/
RUN /opt/venv/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt



RUN pip install -U 'Twisted[tls,http2]'

# # only for development environment - for checking webserver
# RUN pip install websocket
# RUN pip install websocket-client

COPY . /app/
# may be use ADD . /app/ instead of COPY . /app/

# COPY ./entrypoint.sh / 
# ENTRYPOINT [ "sh" , "/entrypoint.sh" ]











# # syntax=docker/dockerfile:1
# FROM python:3.10.2
# #for see the result in terminals
# ENV PYTHONUNBUFFERED=1   

# RUN mkdir /app
# WORKDIR /app
# RUN python3 -m venv /opt/venv
# # Enable venv
# ENV PATH="/opt/venv/bin:$PATH"

# COPY requirements.txt /app/
# RUN /opt/venv/bin/python3 -m pip install --upgrade pip
# RUN pip install -r requirements.txt
# COPY . /app/


# COPY ./entrypoint.sh / 
# ENTRYPOINT [ "sh" , "/entrypoint.sh" ]



