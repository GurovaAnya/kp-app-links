FROM python:3.9
WORKDIR /app

COPY api/requirements.txt ./
RUN pip install -r ./requirements.txt
COPY api ./
ENV FLASK_ENV production

EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "app:app"]
