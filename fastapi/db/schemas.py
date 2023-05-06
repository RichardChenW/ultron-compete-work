from typing import Union

from pydantic import BaseModel


class Answer(BaseModel):
    operated_at: Union[int, str]
    operated_by: str
    auc: float

    class Config:
        orm_mode = True
