FROM python:3.12.3-alpine3.20
LABEL maintainer="Joao"

WORKDIR /app

RUN git clone https://github.com/joaoleau/devops.git \
    && cp -r devops/dev_projetos/flaskapp-metrics/* . \
    && pip install -r requirements.txt \
    && rm -rf devops

EXPOSE $PORT

CMD ["python", "app.py"]
