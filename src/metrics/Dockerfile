FROM python:3.8
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY /cc_metrics /cc_metrics
COPY /alembic /alembic
COPY compute_metrics.py /compute_metrics.py
COPY alembic.ini /alembic.ini
CMD ["gunicorn","-b","0.0.0.0:80","-k","uvicorn.workers.UvicornWorker","--forwarded-allow-ips","*","--proxy-allow-from","*","cc_metrics.app:app"]
