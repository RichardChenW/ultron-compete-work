from sqlalchemy import Column, Integer, String, BigInteger, DECIMAL

from .database import Base


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    operated_at = Column(BigInteger)
    operated_by = Column(String(256))
    auc = Column(DECIMAL(18, 6))
