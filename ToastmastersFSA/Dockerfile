FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY . .

RUN python manage.py collectstatic --noinput || true

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "gunicorn" ]