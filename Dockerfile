FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir pipenv==2026.10.3
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system && pip uninstall --yes pipenv

RUN useradd --create-home app
COPY --chown=app:app . .
USER app

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
