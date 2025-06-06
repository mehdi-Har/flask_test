from typing import Dict, Any
from models.patient import Patient
from configs.atlas_config import db

class PatientService:
    def __init__(self):
        self.collection = db["patients"]
    
    def create(self, patient: Patient) -> Dict[str, Any]:
        if self.collection.find_one({"cin": patient.cin}):
            return {"error": "Patient existe déjà", "status": 409}
        
        self.collection.insert_one(patient.to_dict())
        return {"message": "Patient créé avec succès", "status": 201}
    
    def get_by_cin(self, cin: str) -> Dict[str, Any]:
        patient_data = self.collection.find_one({"cin": cin}, {"_id": 0})
        if not patient_data:
            return {"error": "Patient non trouvé", "status": 404}
        return {"data": patient_data, "status": 200}
    
    def update(self, cin: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        # Ne pas permettre la modification du CIN
        if "cin" in update_data:
            del update_data["cin"]
        
        result = self.collection.update_one({"cin": cin}, {"$set": update_data})
        if result.matched_count == 0:
            return {"error": "Patient non trouvé", "status": 404}
        return {"message": "Patient mis à jour", "status": 200}
    
    def delete(self, cin: str) -> Dict[str, Any]:
        result = self.collection.delete_one({"cin": cin})
        if result.deleted_count == 0:
            return {"error": "Patient non trouvé", "status": 404}
        return {"message": "Patient supprimé", "status": 200}
    
    def get_all(self) -> Dict[str, Any]:
        patients = list(self.collection.find({}, {"_id": 0}))
        return {"data": patients, "status": 200}