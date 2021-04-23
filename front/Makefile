help:
	@echo "make dev: start the development environment in docker"

dev:
	docker run -it -p 3000:3000 -v $$PWD:/dev_mount node:12.9.1-alpine /bin/sh -c "cd /dev_mount; /bin/sh"
