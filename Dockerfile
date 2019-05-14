FROM python:3.7
EXPOSE 80

# install additional dependencies (might have duplicates?)
# (was pipenv previously but had problems with alpine)
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy whole installation (minus dockerignore)
COPY ./app /app

# set workdir to have subscripts in scope
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
