FROM python:3.7
EXPOSE 80

# manual installation
RUN pip install fastapi uvicorn

# copy whole installation (minus dockerignore)
COPY ./app /app

# install additional dependencies (might have duplicates?)
# (was pipenv previously but had problems with alpine)
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# set workdir to have subscripts in scope
WORKDIR ./app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
