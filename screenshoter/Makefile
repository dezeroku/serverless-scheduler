help:
	@echo "make requirements.txt: get dependencies based on requirements.in content"

requirements.txt: deps_docker_image requirements.in
	docker run -v $$PWD:/workdir deps-image-docker

deps_docker_image:
	docker build -t deps-image-docker -f ./Dockerfile.deps .
