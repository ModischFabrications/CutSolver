# use FastAPI quick-deploy
FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8

# copy whole installation (minus dockerignore)
COPY ./app /app

# install additional dependencies
# (install pipenv first to reduce build time)
# TODO: somethings might be duplicated,
# using multistage or wheels might be better for
RUN pip install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system --deploy

# entrypoints & Co are managed by FastAPI
