"""
Ce module définit les schémas de données utilisés par l'application.
"""

from typing import Optional
from pydantic import BaseModel

class TaskBase(BaseModel):
    """
    Schéma de base pour une tâche.
    
    Attributes:
        title (str): Le titre de la tâche.
        description (Optional[str]): La description de la tâche, optionnelle.
        completed (bool): Indique si la tâche est terminée.
    """
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    """
    Schéma pour la création d'une tâche.
    """

class Task(TaskBase):  # pylint: disable=too-few-public-methods
    """
    Schéma pour une tâche avec ID.
    
    Attributes:
        id (int): L'identifiant unique de la tâche.
    """
    id: int

    class Config:  # pylint: disable=too-few-public-methods
        """
        Configuration pour utiliser les objets ORM.
        """
        orm_mode = True
