from fastapi import Depends, FastAPI, UploadFile
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from db import crud, models, schemas
from db.database import SessionLocal, engine

import pandas as pd
import csv
import codecs
from sklearn.metrics import roc_auc_score

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

Y = pd.read_pickle('./lib/result.pkl')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/upload/', response_model=schemas.Answer)
async def create_upload_file(file: UploadFile, operated_by: str, db: Session = Depends(get_db)):
    csv_reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    temp = pd.DataFrame(list(csv_reader), dtype=float)

    if 'lead_id' not in temp.columns:
        return {'error_info': 'Can\' find lead_id in your answer.'}
    if 'y_pred' not in temp.columns:
        return {'error_info': 'please use column named y_pred in your answer.'}

    eval = pd.merge(left=Y, right=temp, how='left', on='lead_id')

    if eval['y_pred'].isna().sum() != 0:
        return {'error_info': 'Looks lead_id is wrong in your answer.'}

    auc_score = roc_auc_score(eval['y'], eval['y_pred'])

    answer = schemas.Answer(operated_at=int(pd.Timestamp.now(tz='Asia/Shanghai').timestamp() * 1000),
                            operated_by=operated_by,
                            auc=auc_score)

    await crud.created_answer(db=db, answer=answer)

    answer.operated_at = pd.Timestamp(answer.operated_at, unit='ms', tz='Asia/Shanghai').strftime('%Y-%m-%d %H:%M:%S')

    return answer


@app.get('/rank/')
async def select_rank():
    res = pd.read_sql(
        """
        SELECT
            operated_by AS name,
            operated_at,
            auc
        FROM
            answer
        ORDER BY
            auc DESC
        LIMIT 10
        """, engine)
    res['operated_at'] = pd.to_datetime(res['operated_at'], unit='ms',
                                        utc=True).dt.tz_convert('Asia/Shanghai').dt.strftime('%Y-%m-%d %H:%M:%S')

    return [v for v in res.T.to_dict().values()]



if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="172.18.1.35", port=8000, reload=True)
