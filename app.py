from flask import Flask, jsonify
from patients.routes import patients_bp
from doctors.routes import doctors_bp

app = Flask(__name__)

# Configuration
app.config['JSON_AS_ASCII'] = False  # Pour supporter les caractères français

# Enregistrement des blueprints
app.register_blueprint(patients_bp, url_prefix="/patients")
app.register_blueprint(doctors_bp, url_prefix="/doctors")

@app.route("/")
def home():
    return jsonify({
        "message": "API de Gestion Médicale",
        "endpoints": {
            "patients": "/patients",
            "doctors": "/doctors",
            "specialites": "/doctors/specialites"
        }
    })

if __name__ == "__main__":
    app.run(debug=True)