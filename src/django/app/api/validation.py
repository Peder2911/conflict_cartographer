from typing import List,Union,Any,Optional,Literal

from pydantic import BaseModel

class CountryGeom(BaseModel):
    coordinates: Any 
    type: Literal["MultiPolygon","Polygon"]

class CountryProps(BaseModel):
    CNTRY_NAME: str # Restrict this?
    GWCODE: int
    ISO1AL2: Optional[str]

class CountryFeature(BaseModel):
    type: Literal["Feature"]
    geometry: CountryGeom
    properties: CountryProps

class CountryFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"]
    features: List[CountryFeature]
