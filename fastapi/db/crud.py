from sqlalchemy.orm import Session

from . import models, schemas


async def created_answer(db: Session, answer: schemas.Answer):
    db_answer = models.Answer(operated_at=answer.operated_at, operated_by=answer.operated_by, auc=answer.auc)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer
