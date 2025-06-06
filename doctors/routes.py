from flask import Blueprint, request, jsonify
from services.doctor_service import DoctorService
from models.doctor import Doctor, Specialite

doctors_bp = Blueprint("doctors", __name__)
doctor_service = DoctorService()

@doctors_bp.route("/", methods=["POST"])
def create_doctor():
    try:
        data = request.json
        required = ["cin", "nom", "email", "telephone", "specialite"]
        
        if not all(k in data for k in required):
            return jsonify({"error": "Champs requis manquants"}), 400
        
        # Validation de la spécialité
        try:
            specialite = Specialite(data["specialite"])
        except ValueError:
            valid_specialites = [s.value for s in Specialite]
            return jsonify({"error": f"Spécialité invalide. Options: {valid_specialites}"}), 400
        
        doctor = Doctor(
            cin=data["cin"],
            nom=data["nom"],
            email=data["email"],
            telephone=data["telephone"],
            specialite=specialite
        )
        
        result = doctor_service.create(doctor)
        return jsonify({
            "message" if result["status"] < 400 else "error": result.get("message", result.get("error"))
        }), result["status"]
    
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@doctors_bp.route("/", methods=["GET"])
def get_all_doctors():
    try:
        result = doctor_service.get_all()
        return jsonify(result["data"]), result["status"]
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@doctors_bp.route("/<cin>", methods=["GET"])
def get_doctor(cin):
    try:
        result = doctor_service.get_by_cin(cin)
        if result["status"] == 200:
            return jsonify(result["data"]), 200
        return jsonify({"error": result["error"]}), result["status"]
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@doctors_bp.route("/<cin>", methods=["PUT"])
def update_doctor(cin):
    try:
        data = request.json
        # Si une spécialité est fournie, la valider
        if "specialite" in data:
            try:
                Specialite(data["specialite"])
            except ValueError:
                valid_specialites = [s.value for s in Specialite]
                return jsonify({"error": f"Spécialité invalide. Options: {valid_specialites}"}), 400
        
        result = doctor_service.update(cin, data)
        return jsonify({
            "message" if result["status"] < 400 else "error": result.get("message", result.get("error"))
        }), result["status"]
    
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@doctors_bp.route("/<cin>", methods=["DELETE"])
def delete_doctor(cin):
    try:
        result = doctor_service.delete(cin)
        return jsonify({
            "message" if result["status"] < 400 else "error": result.get("message", result.get("error"))
        }), result["status"]
    
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500

@doctors_bp.route("/specialites", methods=["GET"])
def get_specialites():
    specialites = [{"value": s.value, "name": s.name} for s in Specialite]
    return jsonify(specialites), 200