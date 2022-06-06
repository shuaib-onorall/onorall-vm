# # syntax=docker/dockerfile:1
FROM python:3.10.2
#for see the result in terminals
ENV PYTHONUNBUFFERED=1   

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

CMD ["python3" , "manage.py" , "runserver" , "0.0.0.0:8000"]






# # syntax=docker/dockerfile:1
# FROM python:3.10.2
# #for see the result in terminals
# WORKDIR /usr/src/app
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1   

# RUN pip install --upgrade pip

# COPY ./requirements.txt .
# RUN pip install -r requirements.txt


# # COPY ./entrypoint.sh .
# # RUN sed -i 's/\r$//g' /usr/src/onorall-backend/entrypoint.sh
# # RUN chmod +x /usr/src/onorall-backend/entrypoint.sh

# # copy project
# COPY . .

# # run entrypoint.sh


