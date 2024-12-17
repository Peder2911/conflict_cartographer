
from environs import Env

env = Env()
env.read_env()

DB_HOST     = env.str("DB_HOST")
DB_USER     = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_NAME     = env.str("DB_NAME")

BLOB_STORAGE_CONNECTION_STRING = env.str("BLOB_STORAGE_CONNECTION_STRING")
GENERAL_CACHE_CONTAINER_NAME = env.str("GENERAL_CACHE_CONTAINER_NAME")
