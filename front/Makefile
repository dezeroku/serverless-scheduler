help:
	@echo "make dev: start the development environment in docker" && \
	echo "make mock_api: start the mock_api in docker and expose it" && \
	echo "make mock_api_stop: stop the mock_api (no check)"

dev:
	docker run -it -p 3000:3000 -v $$PWD:/dev_mount node:16.5.0 /bin/bash -c "cd /dev_mount; /bin/sh"

build:
	docker run --user $(shell id -u) -v $$PWD:/dev_mount node:16.5.0 /bin/bash -c "cd /dev_mount; npm install && npm run build && npm run prepare-dist"

mock_api: .mock_api_container_id

mock_api_stop:
	docker stop $$(cat .mock_api_container_id) && rm .mock_api_container_id

.mock_api_container_id:
	docker run -d -p 8000:8000 -v $$PWD/mock-api:/mock-api node:12.9.1-alpine /bin/sh -c "cd /mock-api; npm install; npx json-server --watch src/db.json --port 8000 --host 0.0.0.0 --routes routes.json" > .mock_api_container_id

.PHONY: build
