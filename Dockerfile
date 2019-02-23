# use FastAPI quick-deploy
FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8

# copy whole installation (minus dockerignore)
COPY ./app /app
VOLUME /data

# install dependencies
RUN pip install pipenv
RUN pipenv install --system --deploy
# TODO: add correct deployment
