# Only the static Docker CLI binary is taken from this stage; it runs on
# the Debian-based runtime below.
FROM docker:cli AS docker-cli

FROM python:3.12-slim

# --docker compilation shells out to the Docker CLI and reaches the host
# daemon through the socket mounted in docker-compose.yml.
COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker

WORKDIR /app
COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir .

EXPOSE 14159

ENTRYPOINT ["tinyleaf"]
