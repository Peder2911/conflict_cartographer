from toolz.functoolz import curry,reduce

def _check_feature_ownership(user,feature):
    try:
        assert feature["properties"]["author"] == user
    except KeyError:
        return True
    except AssertionError:
        return False
    else:
        return True

def check_geojson_ownership(geojson,user):
    check = curry(_check_feature_ownership,user)

    if geojson["type"] == "FeatureCollection":
        if len(geojson["features"]) == 0:
            return True
        else:
            return reduce(lambda a,b: a and b, [check(f) for f in geojson["features"]])
    elif geojson["type"] == "Feature":
        return check(geojson)
    else:
        raise ValueError("Not feature or featurecollection")
