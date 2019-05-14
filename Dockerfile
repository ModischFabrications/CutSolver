# alpine or small would be better but httptools is unable to build there.
# try switching again after 2019/10
FROM python:3.7
EXPOSE 80

# install additional dependencies
# (was pipenv previously but had problems with alpine)
COPY ./requirements.txt requirements.txt
# caches are useless in containers
RUN pip install --no-cache-dir -r requirements.txt

# only the application is relevant for the container
COPY ./app /app

# set workdir to have subscripts in scope
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
