FROM python:3.11-slim

WORKDIR /app

COPY flask_app/ /app/flask_app/
COPY models/vectorizer.pkl /app/models/vectorizer.pkl

RUN pip install --no-cache-dir -r flask_app/requirements.txt

RUN python -m nltk.downloader stopwords wordnet

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "1", "--preload", "flask_app.app:app"]