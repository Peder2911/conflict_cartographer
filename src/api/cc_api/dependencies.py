
from . import db

def database():
    try:
        session = db.Session()
        yield session
    finally:
        session.close()
