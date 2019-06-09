FROM python:3.7

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system

COPY src .

RUN python manage.py collectstatic

EXPOSE 5000
CMD daphne -b 0.0.0.0 -p 5000 carrots.asgi:application
