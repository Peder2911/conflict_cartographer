
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from cc_backend_lib import models

from .. import views, dependencies

router = APIRouter()

@router.get("/{year}/{quarter}/predictions")
def quarter_summary(
        year:       int,
        quarter:    int,
        by_country: bool = False,
        sess: Session = Depends(dependencies.database),
        )-> models.prediction.QuarterlyPredictionSummary:
    """
    Returns a quarterly summary of participation
    """
    def wrap(data: List[views.PredictionsSummary])->models.prediction.QuarterlyPredictionSummary:
        return {
                "year": year,
                "quarter": quarter,
                "data": data
            }

    return (views.quarterly_prediction_summary(sess, year, quarter, by_country)
            .maybe(wrap([]),wrap)
            )
