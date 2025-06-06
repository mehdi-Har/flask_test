from typing import Dict, Any
from models.doctor import Doctor
from configs.atlas_config import db

class DoctorService:
    def __init__(self):
        self.collection = db["doctors"]
    
    def create(self, doctor: Doctor) -> Dict[str, Any]:    
        if self.collection.find_one({"cin": doctor.cin}):
            return {"error": "Docteur existe déjà", "status": 409}
        
        self.collection.insert_one(doctor.to_dict())
        return {"message": "Docteur créé avec succès", "status": 201}
    
    def get_by_cin(self, cin: str) -> Dict[str, Any]:
        doctor_data = self.collection.find_one({"cin": cin}, {"_id": 0})
        if not doctor_data:
            return {"error": "Docteur non trouvé", "status": 404}
        return {"data": doctor_data, "status": 200}
    
    def update(self, cin: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        # Ne pas permettre la modification du CIN
        if "cin" in update_data:
            del update_data["cin"]
        
        result = self.collection.update_one({"cin": cin}, {"$set": update_data})
        if result.matched_count == 0:
            return {"error": "Docteur non trouvé", "status": 404}
        return {"message": "Docteur mis à jour", "status": 200}
    
    def delete(self, cin: str) -> Dict[str, Any]:
        result = self.collection.delete_one({"cin": cin})
        if result.deleted_count == 0:
            return {"error": "Docteur non trouvé", "status": 404}
        return {"message": "Docteur supprimé", "status": 200}
    
    def get_all(self) -> Dict[str, Any]:
        doctors = list(self.collection.find({}, {"_id": 0}))
        return {"data": doctors, "status": 200}