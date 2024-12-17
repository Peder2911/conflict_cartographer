
from typing import Optional, List
import datetime

from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends
from toolz.functoolz import compose
from cc_backend_lib import models

from .. import tables, filters, dependencies

router = APIRouter()


# list view?
@router.get("/")
def countries(
        only_active:        Optional[bool]          = None,
        with_contributions: Optional[bool]          = None,
        start_date:         Optional[datetime.date] = None,
        end_date:           Optional[datetime.date] = None,
        user:               Optional[int]           = None,
        sess: Session = Depends(dependencies.database),
        ) -> List[models.country.CountryIdentity]:
    resp = sess.query(tables.countries.c.name,tables.countries.c.gwno)
    if with_contributions:
        resp = compose(
                filters.shape_author_eq(user),
                filters.shape_end_date_lte(end_date),
                filters.shape_start_date_gte(start_date),
                lambda q: q.join(tables.shapes),
                )(resp)

    if only_active:
        resp = resp.filter(tables.countries.c.active.is_(True))
    return [models.country.CountryIdentity(name=name,gwno=gwno) for name,gwno in resp.distinct().all()]

@router.get("/{gwno:int}")
def country(gwno: int, sess: Session = Depends(dependencies.database)) -> models.country.Country:
    data = (sess
            .query(
                tables.countries.c.gwno,
                tables.countries.c.name,
                tables.countries.c.iso2c,
                tables.countries.c.shape)
            .filter(tables.countries.c.gwno == gwno)
        ).first()

    if data is None:
        return Response(status_code = 404)
    else:
        return models.country.Country.from_row(*data)
