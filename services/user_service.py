from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from models.user import User, Patient, Doctor, Specialite
from config import db

class UserService(ABC):
    def __init__(self, collection_name: str):  # Correction: __init__ au lieu de **init**
        self.collection = db[collection_name]
    
    @abstractmethod
    def create_user_instance(self, data: Dict[str, Any]) -> User:
        pass
    
    def create(self, user: User) -> Dict[str, Any]:
        if not user.validate():
            return {"error": "Données invalides", "status": 400}
        
        if self.collection.find_one({"cin": user.cin}):
            return {"error": "Utilisateur existe déjà", "status": 409}
        
        self.collection.insert_one(user.to_dict())
        return {"message": "Utilisateur créé avec succès", "status": 201}
    
    def get_by_cin(self, cin: str) -> Dict[str, Any]:
        user_data = self.collection.find_one({"cin": cin}, {"_id": 0})
        if not user_data:
            return {"error": "Utilisateur non trouvé", "status": 404}
        return {"data": user_data, "status": 200}
    
    def update(self, cin: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        # Ne pas permettre la modification du CIN
        if "cin" in update_data:
            del update_data["cin"]
        
        result = self.collection.update_one({"cin": cin}, {"$set": update_data})
        if result.matched_count == 0:
            return {"error": "Utilisateur non trouvé", "status": 404}
        return {"message": "Utilisateur mis à jour", "status": 200}
    
    def delete(self, cin: str) -> Dict[str, Any]:
        result = self.collection.delete_one({"cin": cin})
        if result.deleted_count == 0:
            return {"error": "Utilisateur non trouvé", "status": 404}
        return {"message": "Utilisateur supprimé", "status": 200}
    
    def get_all(self) -> Dict[str, Any]:
        users = list(self.collection.find({}, {"_id": 0}))
        return {"data": users, "status": 200}

class PatientService(UserService):
    def __init__(self):  # Correction: __init__ au lieu de **init**
        super().__init__("patients")
    
    def create_user_instance(self, data: Dict[str, Any]) -> Patient:
        return Patient.from_dict(data)

class DoctorService(UserService):
    def __init__(self):  # Correction: __init__ au lieu de **init**
        super().__init__("doctors")
    
    def create_user_instance(self, data: Dict[str, Any]) -> Doctor:
        return Doctor.from_dict(data)