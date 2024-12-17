
from toolz.functoolz import curry
from . import tables

def optional_filter_by(model,column,op,value,query):
    get_model = lambda model: getattr(tables,model)

    if value is not None:
        column = get_model(model).c[column]
        query = query.filter(getattr(column,op)(value))
    return query

shape_start_date_gte = curry(optional_filter_by,"shapes","date","__ge__")
shape_end_date_lte = curry(optional_filter_by,"shapes","date","__le__")
shape_author_eq = curry(optional_filter_by,"shapes","author_id","__eq__")
shape_ctry_eq = curry(optional_filter_by,"shapes","country_id","__eq__")
