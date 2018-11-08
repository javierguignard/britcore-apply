FROM python:3.6.5-alpine3.7

LABEL maintainer="JAVIER GUIGNARD javierguignard@gmail.com"

RUN apk --update add \
      build-base python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN python manage.py db init
RUN python manage.py db migrate
RUN python manage.py db upgrade

ENTRYPOINT [ "python" ]

CMD [ "manage.py", "runserver" ]