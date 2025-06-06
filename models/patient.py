from typing import Dict, Any
from .user import User

class Patient(User):
    def __init__(self, cin: str, nom: str, email: str, telephone: str, 
                 date_naissance: str = None, adresse: str = None):
        super().__init__(cin, nom, email, telephone)
        self.date_naissance = date_naissance
        self.adresse = adresse
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "cin": self.cin,
            "nom": self.nom,
            "email": self.email,
            "telephone": self.telephone,
            "type": "patient"
        }
        
        if self.date_naissance:
            data["date_naissance"] = self.date_naissance
        if self.adresse:
            data["adresse"] = self.adresse
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            cin=data["cin"],
            nom=data["nom"],
            email=data["email"],
            telephone=data["telephone"],
            date_naissance=data.get("date_naissance"),
            adresse=data.get("adresse")
        )