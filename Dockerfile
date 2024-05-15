FROM python:3.12-slim

RUN apt-get update
RUN apt-get install -y build-essential python-dev-is-python3


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN pip install --upgrade pip \
    && pip install six \
    && pip install "poetry==1.8.3" \
    && poetry config virtualenvs.create false\
    && apt-get update\
    && apt-get -y install gcc

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --no-dev

COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]