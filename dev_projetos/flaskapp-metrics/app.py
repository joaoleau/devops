from flask import Flask, jsonify, request
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import os

app = Flask(__name__)

# Configuração do OpenTelemetry
FlaskInstrumentor().instrument_app(app)

# Criação de um provedor de métrica
meter_provider = MeterProvider()
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Criação de um contador
requests_counter = meter.create_counter(
    "http_requests_total",
    description="Total HTTP Requests",
)

@app.before_request
def before_request():
    # Incrementa o contador a cada requisição
    requests_counter.add(1, {"method": request.method, "endpoint": request.path})

# Endpoint principal
@app.route('/')
def home():
    return "Welcome to the API!"

# Endpoint de saúde
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# Middleware para métricas
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()  # Adiciona o endpoint de métricas
})

if __name__ == '__main__':
    port = os.environ.get("PORT", 3000)
    app.run(host='0.0.0.0', port=port)
