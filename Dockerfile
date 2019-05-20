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

# This is a middleway. Pytest requires source files to import from "app.model..",
# while having a WORKDIR in "/app" requires having just "model.." in scripts.
# Fixing pytest and working from inside "/app" would be the cleanest solution
# but fighting around with unittests has already cost me 3 hours I won't get back.

# This could be python3 app/main.py, a choice was made against it to keep dev and prod ports different.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
