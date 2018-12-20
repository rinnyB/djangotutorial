FROM python:3.6.0-alpine
RUN apk update --no-cache && apk add gcc musl-dev postgresql-dev --no-cache
ENV PYTHONBUFFERED 1
RUN mkdir -p app
COPY requirements.txt /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY ./code/ /app/
COPY init.sh /app/
RUN chmod 750 init.sh
ENTRYPOINT ["/app/init.sh"]

