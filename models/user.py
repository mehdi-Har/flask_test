from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any

class User(ABC):
    def __init__(self, cin: str, nom: str, email: str, telephone: str):
        self.cin = cin
        self.nom = nom
        self.email = email
        self.telephone = telephone
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]):
        pass
