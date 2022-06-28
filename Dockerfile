# # syntax=docker/dockerfile:1
FROM python:3.10.2
#for see the result in terminals
ENV PYTHONUNBUFFERED=1   

RUN mkdir /app
WORKDIR /app
RUN python3 -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /app/
RUN /opt/venv/bin/python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/









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



