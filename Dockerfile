FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./Pipfile ./Pipfile

COPY ./Pipfile.lock ./Pipfile.lock

RUN pip install --no-cache-dir --upgrade pip pipenv

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy

COPY ./ /app/
