# —— Inspired by ———————————————————————————————————————————————————————————————
# https://www.strangebuzz.com/en/snippets/the-perfect-makefile-for-symfony

# Setup ————————————————————————————————————————————————————————————————————————

# Parameters
SHELL         = bash
ME            = $(shell whoami)

# Image
IMAGE_NAME := $${CI_REGISTRY_IMAGE:-"nabla/nabla-hooks"}
IMAGE_TAG := $${IMAGE_TAG:-"latest"}
IMAGE_NEXT_TAG := $${CI_COMMIT_REF_SLUG:-"1.0.3"}
IMAGE := $(IMAGE_NAME):$(IMAGE_TAG)

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Executables: local only
DOCKER        = docker

# Misc
.DEFAULT_GOAL = build
.PHONY       =  # Not needed here, but you can put your all your targets to be sure
	            # there is no name conflict between your files and your targets.

## —— 🐝 The Strangebuzz Docker Makefile 🐝 ———————————————————————————————————
help: ## Outputs this help screen
	@grep -E '(^[a-zA-Z0-9_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}{printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

## —— All 🎵 ———————————————————————————————————————————————————————————————
.PHONY: all
all: down clean build up test

## —— Clean Docker 🧹🐳 ———————————————————————————————————————————————————————————————
.PHONY: clean-docker
clean-docker:
	@echo "=> Cleaning image..."
	docker rmi $(IMAGE)

## —— Clean 🧹 ———————————————————————————————————————————————————————————————
.PHONY: clean
clean: clean-docker

## —— Docker Train 🐳🚂 ————————————————————————————————————————————————————————————————
.PHONY: build-docker-train
build-docker-train:  ## Build train container with docker
	@echo "=> Building train image..."
	envsubst '$${CI_PIP_GITLABJUSMUNDI_TOKEN}' < etc/pip.conf > pip.conf
	docker build -t $(IMAGE) --secret id=pip.conf,src=pip.conf --squash -f Dockerfile.train .

## —— Docker 🐳 ————————————————————————————————————————————————————————————————
.PHONY: build-docker
build-docker:  ## Build container with docker
	@echo "=> Building image..."
	envsubst '$${CI_PIP_GITLABJUSMUNDI_TOKEN}' < etc/pip.conf > pip.conf
	docker build -t $(IMAGE) --secret id=pip.conf,src=pip.conf --squash .

## —— Buildah Docker 🐶🐳 ————————————————————————————————————————————————————————————————
.PHONY: build-buildah-docker
build-buildah-docker: ## Build container with buildah
	@echo "=> Building image..."
	buildah bud -t $(IMAGE) .

## —— Build 🚀 —————————————————————————————————————————————————————————————————
.PHONY: build
build: build-docker

## —— Up Docker ✅🐳 —————————————————————————————————————————————————————————————————
.PHONY: up-docker
up-docker:
	@echo "up docker"
	docker run -it -u 1000:1000 $(IMAGE)

## —— Up Python ✅🐍 —————————————————————————————————————————————————————————————————
.PHONY: up-python
up-python:
	@echo "up python http://0.0.0.0:8000/ping"
	python main.py

## —— Up ✅ —————————————————————————————————————————————————————————————————
.PHONY: up
up: up-docker # Serve up (uvicorn)

.PHONY: down
down:
	@echo "down"

.PHONY: run
run: down up

.PHONY: doc
doc: ## Documentation
	@echo "=> Doc..."
	sphinx-build ./docs _build --color -W -bhtml

.PHONY: flake8
flake8: ## Linter flake8
	@echo "=> Linter flake8..."
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

## —— Debug 📜🐳 —————————————————————————————————————————————————————————————————
.PHONY: debug
debug: ## Enter container
	@echo "=> Debuging image..."
	docker run -it -u 1000:1000 -v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro -v /var/run/docker.sock:/var/run/docker.sock --entrypoint /bin/bash $(IMAGE)

## —— Project 🐝🐳 ———————————————————————————————————————————————————————————————
.PHONY: exec
exec: ## Run container
	@echo "=> Executing image..."
	docker run -it -u 1000:1000 -v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

## —— Tests Dive 🧪🐳🚨 —————————————————————————————————————————————————————————————————
.PHONY: test-dive
test-dive: ## Run Dive image tests
	@echo "=> Testing Dive image..."
	@echo "CI=true dive --ci --highestUserWastedPercent 0.1 --lowestEfficiency 0.9 --json docker-dive-stats.json $(IMAGE) 1>docker-dive.log 2>docker-dive-error.log"
	CI=true docker run --rm -it \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v  "$(pwd)":"$(pwd)" \
      -w "$(pwd)" \
      -v "$(pwd)/.dive.yaml":"$(pwd)/.dive.yaml" \
      wagoodman/dive:latest --ci --json docker-dive-stats.json $(IMAGE)

## —— Tests Dive CI 🧪🐳🚨 —————————————————————————————————————————————————————————————————
.PHONY: test-dive-ci
test-dive-ci: ## Run Dive image tests for CI
	@echo "=> Testing Dive image..."
	CI=true dive --ci --highestUserWastedPercent 0.1 --lowestEfficiency 0.9 --json docker-dive-stats.json $(IMAGE)

## —— Tests Codeclimate 🧪🤖 —————————————————————————————————————————————————————————————————
.PHONY: test-codeclimate
test-codeclimate:
	@echo "=> Testing Codeclimate image..."
	codeclimate analyze

## —— Tests Semgrep 🧪👽 —————————————————————————————————————————————————————————————————
.PHONY: test-semgrep
test-semgrep:
	@echo "=> Testing Semgrep image..."
	semgrep --config auto .

## —— Tests Tox 🧪 —————————————————————————————————————————————————————————————————
.PHONY: test-tox
test-tox:
	@echo "=> Testing python..."
	@echo "=> tox --notest"
	tox py38

## —— Tests 🧪 —————————————————————————————————————————————————————————————————
.PHONY: test
test: test-tox test-dive test-codeclimate test-semgrep

## —— Deploy Docker 💾🐳 ———————————————————————————————————————————————————————————————
.PHONY: deploy-docker
deploy-docker: ## Push to registry
	@echo "=> Tagging image..."
	docker tag $(IMAGE) $(IMAGE_NAME):$(IMAGE_NEXT_TAG)
	@echo "=> aws ecr get-login-password --region \$${AWS_REGION:-"eu-west-3"} | docker login --username AWS --password-stdin \$${OCI_REGISTRY:-\"783876277037.dkr.ecr.eu-west-3.amazonaws.com\"} "
	@echo "=> Pushing image..."
	@echo "=> TODO => docker push $(IMAGE_NAME):$(IMAGE_NEXT_TAG)"
	@echo "=> TODO => docker push $(IMAGE_NAME):latest"

## —— Deploy 💾👑 ———————————————————————————————————————————————————————————————
.PHONY: deploy
deploy: deploy-docker ## Push to registry
