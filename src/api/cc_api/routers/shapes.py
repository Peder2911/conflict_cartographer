
import datetime

from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends
from toolz.functoolz import curry, compose
from cc_backend_lib import models

from .. import tables, filters, dependencies

router = APIRouter()

@router.get("/")
def shapes(
        user:       int           = None,
        country:    int           = None,
        start_date: datetime.date = None,
        end_date:   datetime.date = None,
        sess: Session = Depends(dependencies.database),
        ) -> models.prediction.PredFeatureCollection:
    """
    shapes
    ======

    Get all shapes matching the specified query parameters.
    """
    resp = compose(
            curry(filters.shape_ctry_eq,country),
            curry(filters.shape_author_eq,user),
            curry(filters.shape_end_date_lte,end_date),
            curry(filters.shape_start_date_gte,start_date),
            lambda q: q.query(tables.shapes),
        )(sess)
    return models.prediction.PredFeatureCollection.from_response(resp.all())

@router.get("/{id}/")
def shape_detail(id: int, sess: Session = Depends(dependencies.database))->models.prediction.PredictionFeature:
    """
    shape_detail
    ============

    Show details about an identified shape.
    """
    feature = (sess
            .query(tables.shapes)
            .filter(tables.shapes.c.id == id)
            .first()
        )
    if feature is None:
        return Response(status_code = 404)
    feature = models.prediction.PredictionFeature.from_row(**dict(feature))

    metrics = (sess
            .query(tables.evaluation_metrics)
            .filter(tables.evaluation_metrics.c.shape_id == id)
            .all()
        )
    if metrics:
        metrics = {row["name"]:row["value"] for row in metrics}
        feature.properties.update(metrics)

    return feature
