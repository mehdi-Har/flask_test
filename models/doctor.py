from typing import Dict, Any
from .user import User
from .enumSpecialite import Specialite

class Doctor(User):
    def __init__(self, cin: str, nom: str, email: str, telephone: str, 
                 specialite: Specialite, cabinet: str = None, tarif: float = None):
        super().__init__(cin, nom, email, telephone)
        self.specialite = specialite
        self.cabinet = cabinet
        self.tarif = tarif
    
    def validate(self) -> bool:
        """Valide les données du docteur incluant la spécialité"""
        # Validation spécialité
        if not isinstance(self.specialite, Specialite):
            return False
            
        # Validation tarif si fourni
        if self.tarif is not None and self.tarif < 0:
            return False
            
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "cin": self.cin,
            "nom": self.nom,
            "email": self.email,
            "telephone": self.telephone,
            "specialite": self.specialite.value,
            "type": "doctor"
        }
        
        # Ajouter les champs optionnels s'ils existent
        if self.cabinet:
            data["cabinet"] = self.cabinet
        if self.tarif is not None:
            data["tarif"] = self.tarif
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            cin=data["cin"],
            nom=data["nom"],
            email=data["email"],
            telephone=data["telephone"],
            specialite=Specialite(data["specialite"]),
            cabinet=data.get("cabinet"),
            tarif=data.get("tarif")
        )
