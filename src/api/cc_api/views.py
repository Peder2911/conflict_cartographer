"""
View queries, used to present summaries to the end user
"""
from typing import Optional
from pymonad.maybe import Maybe, Just, Nothing
from pydantic import BaseModel
from toolz.functoolz import curry
from sqlalchemy import Integer, Float, text, cast, func
from sqlalchemy.sql import extract
from sqlalchemy.orm import Session
from . import tables

shapes, users, metrics = (tables.meta.tables[k] for k in ("api_shape","auth_user","evaluation_metric"))

json_extract = lambda field,cast_to,col: cast(text(str(col) + f" ->> '{field}'"), cast_to)
get_quarter = curry(extract, "quarter")
get_year = curry(extract, "year")

class PredictionsSummary(BaseModel):
    confidence: float
    intensity: float
    accuracy: Optional[float]
    coverage: Optional[float]
    gwno: Optional[int]
    @property
    def evaluated(self):
        return self.accuracy is not None and self.coverage is not None


def metrics_query(session, kind: str):
    return (session
            .query(metrics.c.value, metrics.c.shape_id)
            .join(shapes)
            .filter(metrics.c.name == kind)
        )

def quarterly_prediction_summary(session: Session, year, quarter, by_country: bool = False) -> Maybe[PredictionsSummary]:
    """
    Returns a summary of predictions, optionally grouped by country
    """
    time_filter = lambda q: (q
            .filter(get_year(shapes.c["date"]) == year)
            .filter(get_quarter(shapes.c["date"]) == quarter)
        )

    intensity = curry(json_extract,"intensity",Integer)
    confidence = curry(json_extract,"confidence",Float)

    correct,coverage = (time_filter(metrics_query(session, nm)).subquery() for nm in ("correct","conflict_coverage"))

    names = ("n","intensity","confidence","accuracy","coverage")

    q = time_filter(session
            .query(
                func.count(shapes.c["id"]),
                func.avg(cast(intensity(shapes.c["values"]), Float)),
                func.avg(confidence(shapes.c["values"])),
                func.avg(correct.c.value),
                func.avg(coverage.c.value),
                )
            .select_from(shapes)
            .join(correct, isouter=True)
            .join(coverage, isouter=True)
            .group_by(get_quarter(shapes.c["date"]))
            .group_by(get_year(shapes.c["date"]))
            )

    if by_country:
        q = q.group_by(shapes.c.country_id).add_columns(shapes.c.country_id)
        names = names + ("gwno",)

    summaries = q.all()
    if len(summaries)>0:
        return Just([PredictionsSummary(**{k:v for k,v in zip(names, row)}) for row in summaries])
    else:
        return Nothing
