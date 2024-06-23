FROM python:3.12.3-alpine3.20
LABEL maintainer="Joao"

RUN pip install flask

WORKDIR /app
RUN git clone https://github.com/joaoleau/devops.git \
    && cp -r devops/dev_projetos/flaska/* . \
    && rm -rf devops

ARG PORT
ARG BACKGROUND_COLOR
ENV PORT=${PORT:-3000}
ENV BACKGROUND_COLOR $BACKGROUND_COLOR

EXPOSE $PORT

CMD ["python", "app.py"]