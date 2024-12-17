FROM peder2911/uvicorn-deployment:2.1.2 

COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./backend/ /backend/
ENV GUNICORN_APP backend.app:app
