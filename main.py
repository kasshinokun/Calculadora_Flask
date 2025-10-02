import os

from flask import Flask, send_from_directory, session

from src.routes.user import user_bp
from src.routes.calculator import calculator_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'your_key_database_api'

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(calculator_bp, url_prefix='/api')

# uncomment if you need to use database
# Database configuration removed as per user request to store data in runtime only

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

