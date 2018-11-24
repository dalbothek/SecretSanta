FROM grahamdumpleton/mod-wsgi-docker:python-3.5

MAINTAINER Simon Marti <simon@marti.email>

WORKDIR /app

EXPOSE 80

ENV FLASK_INSTANCE_PATH=/data

COPY requirements.txt ./
RUN mod_wsgi-docker-build

COPY static/ ./static/
COPY templates/ ./templates/
COPY secretsanta.wsgi *.py ./

ENTRYPOINT ["mod_wsgi-docker-start"]
CMD ["secretsanta.wsgi", "--access-log"]
