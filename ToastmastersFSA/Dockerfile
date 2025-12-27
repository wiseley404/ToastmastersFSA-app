# Dockerfile for productio use

FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libgobject-2.0-0 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

CMD ["sh", "-c", "python manage.py migrate && gunicorn ToastmastersFSA.wsgi:application --bind 0.0.0.0:$PORT"]