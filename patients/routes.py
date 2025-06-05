from flask import Blueprint, request, jsonify
from services.user_service import PatientService
from models.user import Patient

patients_bp = Blueprint("patients", __name__)  # Correction: __name__ au lieu de **name**
patient_service = PatientService()

@patients_bp.route("/", methods=["POST"])
def create_patient():
    try:
        data = request.json
        required = ["cin", "nom", "email", "telephone"]
        if not all(k in data for k in required):
            return jsonify({"error": "Champs requis manquants"}), 400
        
        patient = Patient(
            cin=data["cin"],
            nom=data["nom"],
            email=data["email"],
            telephone=data["telephone"]
        )
        
        result = patient_service.create(patient)
        return jsonify({"message" if result["status"] < 400 else "error": result.get("message", result.get("error"))}), result["status"]
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@patients_bp.route("/", methods=["GET"])
def get_all_patients():
    try:
        result = patient_service.get_all()
        return jsonify(result["data"]), result["status"]
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@patients_bp.route("/<cin>", methods=["GET"])
def get_patient(cin):
    try:
        result = patient_service.get_by_cin(cin)
        if result["status"] == 200:
            return jsonify(result["data"]), 200
        return jsonify({"error": result["error"]}), result["status"]
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@patients_bp.route("/<cin>", methods=["PUT"])
def update_patient(cin):
    try:
        data = request.json
        result = patient_service.update(cin, data)
        return jsonify({"message" if result["status"] < 400 else "error": result.get("message", result.get("error"))}), result["status"]
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@patients_bp.route("/<cin>", methods=["DELETE"])
def delete_patient(cin):
    try:
        result = patient_service.delete(cin)
        return jsonify({"message" if result["status"] < 400 else "error": result.get("message", result.get("error"))}), result["status"]
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500