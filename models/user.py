from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any
import re

class Specialite(Enum):
    CARDIOLOGIE = "cardiologie"
    DERMATOLOGIE = "dermatologie"
    NEUROLOGIE = "neurologie"
    PEDIATRIE = "pediatrie"
    GYNECOLOGIE = "gynecologie"
    ORTHOPEDI = "orthopedi"
    PSYCHIATRIE = "psychiatrie"
    RADIOLOGIE = "radiologie"
    ANESTHESIE = "anesthesie"
    CHIRURGIE = "chirurgie"

class User(ABC):
    def __init__(self, cin: str, nom: str, email: str, telephone: str):
        self.cin = cin
        self.nom = nom
        self.email = email
        self.telephone = telephone
    
    def validate(self) -> bool:
        """Valide les données de base de l'utilisateur"""
        # Validation CIN (format marocain : 8 caractères)
        if not self.cin or len(self.cin) != 8:
            return False
        
        # Validation nom
        if not self.nom or len(self.nom.strip()) < 2:
            return False
        
        # Validation email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            return False
        
        # Validation téléphone (format marocain)
        phone_pattern = r'^(\+212|0)[5-7][0-9]{8}$'
        if not re.match(phone_pattern, self.telephone):
            return False
        
        return True
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]):
        pass

class Patient(User):
    def __init__(self, cin: str, nom: str, email: str, telephone: str):
        super().__init__(cin, nom, email, telephone)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "cin": self.cin,
            "nom": self.nom,
            "email": self.email,
            "telephone": self.telephone,
            "type": "patient"
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            cin=data["cin"],
            nom=data["nom"],
            email=data["email"],
            telephone=data["telephone"]
        )

class Doctor(User):
    def __init__(self, cin: str, nom: str, email: str, telephone: str, specialite: Specialite):
        super().__init__(cin, nom, email, telephone)
        self.specialite = specialite
    
    def validate(self) -> bool:
        """Valide les données du docteur incluant la spécialité"""
        if not super().validate():
            return False
        
        # Validation spécialité
        if not isinstance(self.specialite, Specialite):
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "cin": self.cin,
            "nom": self.nom,
            "email": self.email,
            "telephone": self.telephone,
            "specialite": self.specialite.value,
            "type": "doctor"
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            cin=data["cin"],
            nom=data["nom"],
            email=data["email"],
            telephone=data["telephone"],
            specialite=Specialite(data["specialite"])
        )