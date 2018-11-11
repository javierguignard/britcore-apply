FROM python:3.6.5-alpine3.7

LABEL maintainer="JAVIER GUIGNARD javierguignard@gmail.com"

RUN apk --update add \
      build-base python3-dev

RUN apk add gcc musl-dev libffi-dev openssl-dev

# We copy just the requirements.txt first to leverage Docker cache

COPY . /app

WORKDIR /app

RUN python3.6 -m pip install --no-cache-dir -r requirements.txt

RUN python3.6 manage.py db init; exit 0
RUN python3.6 manage.py db migrate; exit 0
RUN python3.6 manage.py db upgrade; exit 0


EXPOSE 5000

ENTRYPOINT [ "python3.6" ]

CMD [ "manage.py", "runserver", "--host", "0.0.0.0"]