from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

@app.route('/')
def hello():
    color = os.environ.get('BACKGROUND_COLOR', 'white')
    html_content = f"""
    <html>
        <head><title>Load Balancer Test</title></head>
        <body style="background-color: {color};">
            <h1>Background Color: {color}</h1>
        </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/health')
def health():
    return jsonify(message="ok"), 200

if __name__ == '__main__':
    port = os.environ.get("PORT", 3000)
    print(port)
    app.run(host='0.0.0.0', port=port)