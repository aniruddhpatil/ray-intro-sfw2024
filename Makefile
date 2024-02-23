SHELL=/bin/bash -Eeuo pipefail

DOCKER_COMPOSE_PATH=./docker/docker-compose.yml
DOCKER_CMD=docker-compose -f ${DOCKER_COMPOSE_PATH}

.PHONY: install
install:
	poetry lock
	poetry export --without-hashes --format=requirements.txt > ./docker/requirements.txt

.PHONY: build
build:
	${DOCKER_CMD} build


.PHONY: up
up:
	${DOCKER_CMD} up || true


.PHONY: down
down:
	${DOCKER_CMD} down --volumes --remove-orphans

.PHONY: all
all: build up
