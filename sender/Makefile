help:
	@echo "make requirements.txt: get dependencies based on requirements.in content"
	@echo "make requirements_test.txt: get dependencies based on requirements_test.in content"

requirements.txt: deps_docker_image requirements.in
	docker run -v $$PWD:/workdir deps-image-docker

requirements_test.txt: deps_test_docker_image requirements_test.in requirements.txt
	docker run -v $$PWD:/workdir deps-test-image-docker

deps_docker_image: Dockerfile.deps
	docker build -t deps-image-docker -f ./Dockerfile.deps .

deps_test_docker_image: Dockerfile_test.deps
	docker build -t deps-test-image-docker -f ./Dockerfile_test.deps .
