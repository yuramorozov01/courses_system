FROM python:3.9
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./courses_run.bash ./
RUN chmod +x ./courses_run.bash

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./src ./src

CMD ["python3", "./src/manage.py", "runserver", "0.0.0.0:8000"]
