import os
from flask import Flask, jsonify
from flask_cors import CORS
from routes.api import api_bp

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app, resources={r"/*": {"origins": "*"}})

# Health check route
@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "AI Research & Knowledge Assistant API is running live!"
    })

# Register Blueprint
app.register_blueprint(api_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)