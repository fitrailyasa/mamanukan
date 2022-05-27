# Dockerfile, Image, Container
FROM python:3.10

ADD main.py .

ADD ./asset .

RUN pip install pygame

CMD [ "python", "./main.py" ]