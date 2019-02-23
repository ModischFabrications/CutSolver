FROM python:3.7-alpine

# documentation
LABEL maintainer="Modisch Fabrications <modisch.fabrications@gmail.com>"

# create user and dir
RUN adduser -D cutsolver
WORKDIR /home/cutsolver

# copy whole installation (minus dockerignore)
COPY . .
VOLUME /data

# install dependencies
RUN pip install pipenv
RUN pipenv install --system --deploy
# TODO: add correct deployment

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