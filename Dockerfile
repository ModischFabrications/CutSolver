FROM python:3.7-alpine

# create user and dir
RUN adduser -D cutsolver
WORKDIR /home/cutsolver

# copy whole installation (minus dockerignore)
COPY . .

# install dependencies
RUN pip install pipenv
RUN pipenv install --system --deploy
# TODO: add gunicorn

# make everything executable
RUN chmod +rx boot.sh

# prepare user
RUN chown -R cutsolver:cutsolver ./
USER cutsolver

# flask port
EXPOSE 5000

# serve application
ENV FLASK_APP app.py
ENTRYPOINT ./boot.sh