# —— Inspired by ———————————————————————————————————————————————————————————————
# https://www.strangebuzz.com/en/snippets/the-perfect-makefile-for-symfony

# Setup ————————————————————————————————————————————————————————————————————————

# Parameters
SHELL         = bash
ME            = $(shell whoami)

# Image
APP_NAME     = nabla-hooks
# 783876277037.dkr.ecr.eu-west-3.amazonaws.com
OCI_REGISTRY = nabla
AWS_REGION   = eu-west-3
OCI_IMAGE := $(OCI_REGISTRY)/$(APP_NAME)
OCI_TAG := $${OCI_TAG:-"latest"}
IMAGE_NEXT_TAG := $${OCI_IMAGE_TAG:-"1.0.7"}
IMAGE := $(OCI_IMAGE):$(OCI_TAG)

TRIVY_VULN_TYPE = "os,library"
TRIVY_SECURITY_CHECKS = "vuln,config,secret"
TRIVY_GLOBAL_SECURITY_CHECKS = --security-checks ${TRIVY_SECURITY_CHECKS} --vuln-type ${TRIVY_VULN_TYPE}
TRIVY_ARGS = --skip-dirs .direnv --skip-dirs .venv --skip-dirs ./node_modules --skip-dirs /usr/local/lib/python3.8/dist-packages/ansible/galaxy/ --skip-dirs /home/ubuntu/.local/lib/python3.8/site-packages/awscli/ --skip-dirs /home/ubuntu/.local/share/virtualenvs/ --skip-dirs /home/ubuntu/.local/lib/python3.8/site-packages/rsa/ --skip-dirs /home/ubuntu/.local/lib/python3.8/site-packages/botocore/data/ --skip-dirs /usr/lib/node_modules/ --skip-files /usr/local/bin/container-structure-test
CS_SEVERITY_REPORT_THRESHOLD = "HIGH,CRITICAL"

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = build

# Executables: local only
DOCKER        = docker

# Misc
.DEFAULT_GOAL = build
.PHONY       =  # Not needed here, but you can put your all your targets to be sure
	            # there is no name conflict between your files and your targets.

## —— 🐝 The Strangebuzz Docker Makefile 🐝 ———————————————————————————————————
.PHONY: help Makefile
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

## —— Clean Docker 🧹🐳💩 ———————————————————————————————————————————————————————————————
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
	envsubst '$${CI_PIP_GITLABNABLA_TOKEN}' < etc/pip.conf > pip.conf
	docker build -t $(IMAGE) --build-arg CI_PIP_GITLABNABLA_TOKEN=$${CI_PIP_GITLABNABLA_TOKEN} --squash -f Dockerfile.train .

## —— Docker 🐳 ————————————————————————————————————————————————————————————————
.PHONY: build-docker
build-docker:  ## Build container with docker
	@echo "=> Building image..."
	# envsubst '$${CI_PIP_GITLABNABLA_TOKEN}' < etc/pip.conf > pip.conf
	# --secret id=pip.conf,src=pip.conf
	docker build -t $(IMAGE) --squash .

## —— Buildah Docker 🐶🐳 ————————————————————————————————————————————————————————————————
.PHONY: build-buildah-docker
build-buildah-docker: ## Build container with buildah
	@echo "=> Building image..."
	buildah bud -t $(IMAGE) --build-arg CI_PIP_GITLABNABLA_TOKEN=$${CI_PIP_GITLABNABLA_TOKEN} .

## —— Buildah 🐶 ————————————————————————————————————————————————————————————————
.PHONY: build-buildah
build-buildah: ## Build container with buildah
	@echo "=> Building image..."
	./build-oci.sh

## —— Build 🚀 —————————————————————————————————————————————————————————————————
.PHONY: build
build: build-docker

## —— Up Docker ✅🐳 —————————————————————————————————————————————————————————————————
.PHONY: up-docker
up-docker:
	@echo "up docker"
	docker run -it $(IMAGE)

## —— Up Python ✅🐍 —————————————————————————————————————————————————————————————————
.PHONY: up-python
up-python:
	@echo "up python http://0.0.0.0:8080/health"
	python -m serve

## —— Up Python ✅🦄 —————————————————————————————————————————————————————————————————
.PHONY: up-uvicorn
up-uvicorn:
	@echo "up uvicorn http://0.0.0.0:8080/v1/ping"
	@echo ".venv/bin/uvicorn nabla.main:app --reload --workers 1 --host 0.0.0.0 --port 8080"
	.venv/bin/uvicorn serve:app --reload --workers 1 --host 0.0.0.0 --port 8080

## —— Up ✅ —————————————————————————————————————————————————————————————————
.PHONY: up
up: up-uvicorn # Serve up (uvicorn)

.PHONY: down
down:
	@echo "down"

.PHONY: run
run: down up

## —— Doc 📜 —————————————————————————————————————————————————————————————————
.PHONY: doc
doc: ## Documentation
	@echo "=> Doc..."
	sphinx-build ./docs ./docs/_build --color -W -bhtml

## —— Lint 🧪 —————————————————————————————————————————————————————————————————
.PHONY: flake8
flake8: ## Linter flake8
	@echo "=> Linter flake8..."
	flake8 ./hooks/ tests  --config .flake8 --count --exit-zero --max-line-length=88 --max-complexity=12 --statistics

## —— Debug 📜🐳 —————————————————————————————————————————————————————————————————
.PHONY: debug
debug: ## Enter container
	@echo "=> Debuging image..."
	docker run -it -u 0 --entrypoint /bin/bash --env CI_PIP_GITLABNABLA_TOKEN=$${CI_PIP_GITLABNABLA_TOKEN} $(IMAGE)

## —— Project 🐝🐳 ———————————————————————————————————————————————————————————————
.PHONY: start
start: ## Run container
	@echo "=> Executing image..."
	docker run -it -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

## —— Tests Dive 🧪🐳🚨 —————————————————————————————————————————————————————————————————
.PHONY: test-dive
test-dive: ## Run Dive image tests
	@echo "=> Testing Dive image..."
	@echo "CI=true dive --ci --highestUserWastedPercent 0.1 --lowestEfficiency 0.9 --json docker-dive-stats.json $(IMAGE) 1>docker-dive.log 2>docker-dive-error.log"
	CI=true docker run --rm -it \
	    -v /var/run/docker.sock:/var/run/docker.sock \
	    -v "$(CURDIR)":"$(CURDIR)" \
	    -w "$(CURDIR)" \
	    -v "$(CURDIR)/.dive.yaml":"$(CURDIR)/.dive.yaml" \
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
	@echo "codeclimate analyze"
	docker run \
	  --interactive --tty --rm \
	  --env CODECLIMATE_CODE="$(CURDIR)" \
	  --volume "$(CURDIR)":/code \
	  --volume /var/run/docker.sock:/var/run/docker.sock \
	  --volume /tmp/cc:/tmp/cc \
	  codeclimate/codeclimate analyze

## —— Tests Semgrep 🧪👽 —————————————————————————————————————————————————————————————————
.PHONY: test-semgrep
test-semgrep:
	@echo "=> Testing Semgrep image..."
	semgrep --config auto .

## —— Tests Nox 🧪⛓️ —————————————————————————————————————————————————————————————————
.PHONY: test-nox
test-nox:
	@echo "=> Testing python..."
	@echo "=> python -m pytest --cov=hooks --cov-fail-under=70"
	nox

## —— Tests Tox 🧪 —————————————————————————————————————————————————————————————————
.PHONY: test-tox
test-tox:
	@echo "=> Testing python..."
	@echo "=> tox --notest"
	tox py312

## —— Tests CST 🧪🕳️ —————————————————————————————————————————————————————————————————
.PHONY: test-cst
test-cst:
	@echo "=> Testing CST image..."
	@echo "/usr/local/bin/container-structure-test test --save -v info --image $(IMAGE) --config ./config.yaml"
	/usr/local/bin/container-structure-test test --image $(IMAGE) --config ./config.yaml

## —— Tests 🧪 —————————————————————————————————————————————————————————————————
.PHONY: test
test: test-tox test-dive test-codeclimate test-semgrep test-cst

## —— Tests Sast Docker 👮😈🐳 —————————————————————————————————————————————————————————————————
.PHONY: sast-docker
sast-docker:
	@echo "=> Scanning trivy image..."
	time trivy image --exit-code 1 --severity $(CS_SEVERITY_REPORT_THRESHOLD) $(TRIVY_GLOBAL_SECURITY_CHECKS) $(TRIVY_ARGS) --format table --output scan-report.md $(IMAGE) 1>docker-trivy.log 2>docker-trivy-error.log

## —— Tests Sast Fs Docker 👮😈️🐳 —————————————————————————————————————————————————————————————————
.PHONY: sast-fs-docker
sast-fs-docker:
	@echo "=> Scanning trivy filesystem..."
	time trivy filesystem --exit-code 2 --severity $(CS_SEVERITY_REPORT_THRESHOLD) $(TRIVY_GLOBAL_SECURITY_CHECKS) $(TRIVY_ARGS) --format table --output scan-report-fs.md . 1>docker-trivy-fs.log 2>docker-trivy-fs-error.log

## —— Tests Sast Buildah 👮😈🐶 —————————————————————————————————————————————————————————————————
.PHONY: sast-buildah
sast-buildah:
	@echo "=> Scanning trivy image..."
	rm -Rf "./archive/" || true
	mkdir "./archive/" || true
	buildah push $(IMAGE) docker-archive:./archive/built-with-buildah.tar:latest
	time trivy image --exit-code 1 --severity $(CS_SEVERITY_REPORT_THRESHOLD) $(TRIVY_GLOBAL_SECURITY_CHECKS) $(TRIVY_ARGS) --format table --output scan-report.md --input ./archive/built-with-buildah.tar 1>docker-trivy.log 2>docker-trivy-error.log

## —— Tests Sast 👮😈 —————————————————————————————————————————————————————————————————
.PHONY: sast
sast: sast-fs-docker ## Run Trivy sast

## —— Deploy Docker 💾🐳 ———————————————————————————————————————————————————————————————
.PHONY: deploy-docker
deploy-docker: ## Push to registry
	@echo "=> Tagging image..."
	docker tag $(IMAGE) $(OCI_IMAGE):$(IMAGE_NEXT_TAG)
	@echo "=> docker login registry.gitlab.com --username \$${GITLAB_PRIVATE_USERNAME} --password \$${GITLAB_FULL_PRIVATE_TOKEN}"
	@echo "=> aws ecr get-login-password --region \$${AWS_REGION:-"eu-west-3"} | docker login --username AWS --password-stdin \$${OCI_REGISTRY:-\"783876277037.dkr.ecr.eu-west-3.amazonaws.com\"} "
	@echo "=> Pushing image..."
	@echo "=> By Hand 👊 => docker push $(OCI_IMAGE):$(IMAGE_NEXT_TAG)"
	@echo "=> By Hand ✌ => docker push $(OCI_IMAGE):latest"

## —— Deploy Buildah 💾🐶 ———————————————————————————————————————————————————————————————
.PHONY: deploy-buildah
deploy-buildah: ## Push to registry
	@echo "=> Tagging image..."
	buildah tag $(IMAGE) $(OCI_IMAGE):$(IMAGE_NEXT_TAG)
	@echo "=> Pushing image..."
	@echo "=> TODO => buildah push $(OCI_IMAGE):$(IMAGE_NEXT_TAG)"
	@echo "=> TODO => buildah push $(OCI_IMAGE):latest"

## —— Deploy 💾👑 ———————————————————————————————————————————————————————————————
.PHONY: deploy
deploy: deploy-docker ## Push to registry
