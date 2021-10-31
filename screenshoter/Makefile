help:
	@echo "make dev: start the development environment in docker"

dev:
	docker build -t screenshoter-dev . --target dev && \
	docker run -it --security-opt seccomp=chromium.json -p 8080:8080 -v $$PWD:/dev_mount screenshoter-dev /bin/sh -c "cd /dev_mount; /bin/sh"

test_case:
	curl 'localhost:8080/v1/screenshot?url=http:%2F%2Fexample.com' | jq ".image" -r | base64 -d | display
