
from sqlalchemy.orm import Session
import datetime

from fastapi import APIRouter, Depends
from cc_backend_lib import models

from .. import tables, db, dependencies

router = APIRouter()

@router.get("/")
def nonanswers(
        user:       int           = None,
        country:    int           = None,
        start_date: datetime.date = None,
        end_date:   datetime.date = None,
        sess: Session = Depends(dependencies.database)):
    resp = (sess
            .query(*[tables.nonanswers.c[c] for c in models.prediction.NonAnswer.Meta.QUERY_ORDER])
        )

    if user is not None:
        resp = (resp
                .filter(tables.nonanswers.c.author_id == user)
            )

    if country is not None:
        resp = (resp
                .filter(tables.nonanswers.c.country_id == country)
            )

    if start_date is not None:
        resp = (resp
                .filter(tables.nonanswers.c.date >= start_date)
            )

    if end_date is not None:
        resp = (resp
                .filter(tables.nonanswers.c.date <= end_date)
            )

    return [models.prediction.NonAnswer.from_row(*r) for r in resp.all()]
