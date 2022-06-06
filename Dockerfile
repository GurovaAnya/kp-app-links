FROM python:3.9
WORKDIR /app

COPY api/requirements.txt ./
RUN pip install -r ./requirements.txt
COPY api ./
ENV FLASK_ENV production

EXPOSE $PORT
CMD gunicorn -b :$PORT app:app
