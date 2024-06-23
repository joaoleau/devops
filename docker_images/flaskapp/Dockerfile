FROM python:3.12.3-alpine3.20
LABEL maintainer="Joao"

RUN pip install flask

WORKDIR /app
COPY app.py .

ARG PORT
ARG BACKGROUND_COLOR
ENV PORT=${PORT:-3000}
ENV BACKGROUND_COLOR $BACKGROUND_COLOR

EXPOSE $PORT

CMD ["python", "app.py"]