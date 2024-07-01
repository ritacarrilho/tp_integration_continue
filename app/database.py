"""
Ce module configure la connexion à la bdd.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://taskuser:taskpassword@localhost/taskdb')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://taskuser:taskpassword@tasks-db/taskdb')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Obtient une session de base de données et garantit sa fermeture après utilisation.

    Returns:
        Generator[Session, None, None]: Un générateur de session de base de données.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
