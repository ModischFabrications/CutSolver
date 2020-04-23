# this size should be irrelevant
FROM python:3.7 as build
# exporting here is a lot safer than depending on the dev, it's worth the additional minute
COPY ./Pipfile /Pipfile
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt

# caches are useless in containers, user needed to make installation portable
# httpie allows healthchecks with tiny installation size (#37)
RUN pip install --user --no-cache-dir --no-warn-script-location -r requirements.txt httpie

FROM python:3.7-slim
# https://github.com/opencontainers/image-spec/blob/master/annotations.md
LABEL "org.opencontainers.image.title"="CutSolver"
LABEL "org.opencontainers.image.version"=$(TRAVIS_TAG)
LABEL "org.opencontainers.image.vendor"="modisch.fabrications@gmail.com"
LABEL "org.opencontainers.image.source"="https://github.com/ModischFabrications/CutSolver/"
LABEL "org.opencontainers.image.licenses"="LGPL-3.0"

# copy over the pip installation with all dependencies
COPY --from=build /root/.local /root/.local

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

# only the application is relevant for the container
COPY ./app /app

EXPOSE 80
HEALTHCHECK --interval=5m --timeout=5s CMD http --check-status http://localhost:80/ || exit 1

# This could be python3 app/main.py, a choice was made against it to keep dev and prod ports different.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
