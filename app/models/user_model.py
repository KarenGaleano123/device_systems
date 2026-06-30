from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base # O como tengas tu Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Nuevos campos de seguridad requeridos por la guía
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False) # admin, support, user
    is_active = Column(Boolean, default=True, nullable=False)

    # Relaciones existentes (ejemplo)
    loans = relationship("Loan", back_populates="user")