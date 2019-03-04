# use FastAPI quick-deploy
FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8

# copy whole installation (minus dockerignore)
COPY ./app /app

# install additional dependencies
# (was pipenv previously but had problems with alpine)
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# entrypoints are managed by FastAPI
