from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    category = Column(String(50), nullable=False)
    budget = Column(String(50), nullable=False)

    preferences = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=False)

    created_at = Column(
        String(50),
        nullable=False
    )

    user = relationship("User")