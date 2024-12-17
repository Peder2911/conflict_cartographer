import logging

from sqlalchemy import Table,MetaData
from azure_blob_storage_cache import BlobCache
from azure_blob_storage_cache.exceptions import NotCached
from . import db, settings

logger = logging.getLogger(__name__)

cache = BlobCache(settings.BLOB_STORAGE_CONNECTION_STRING, settings.GENERAL_CACHE_CONTAINER_NAME)

try:
    meta = cache["api-db-reflection"]
except NotCached:
    meta = MetaData()

    shapes = Table("api_shape",meta,autoload_with=db.engine)
    countries = Table("api_country",meta,autoload_with=db.engine)
    users = Table("auth_user",meta,autoload_with=db.engine)
    nonanswers = Table("api_nonanswer",meta,autoload_with=db.engine)
    evaluation_metrics = Table("evaluation_metric",meta,autoload_with=db.engine)
    profile = Table("api_profile",meta,autoload_with=db.engine)
    profile_countries = Table("api_profile_countries",meta,autoload_with=db.engine)

    cache["api-db-reflection"] = meta
else:
    shapes = meta.tables["api_shape"]
    countries = meta.tables["api_country"]
    users = meta.tables["auth_user"]
    nonanswers = meta.tables["api_nonanswer"]
    evaluation_metrics = meta.tables["evaluation_metric"]
    profile = meta.tables["api_profile"]
    profile_countries = meta.tables["api_profile_countries"]
