.PHONY: install run test lint format docker-build compose-up kind-up image-load k8s-apply helm-install tf-init tf-apply clean

install:        ## Install app + dev dependencies
	pip install -e ".[dev]"

run:            ## Run the API locally (SQLite)
	uvicorn app.main:app --reload

test:           ## Run tests with coverage gate
	pytest

lint:           ## Lint + type-check
	ruff check .
	ruff format --check .
	mypy app

format:         ## Auto-format
	ruff format .

docker-build:   ## Build the container image
	docker build -t urlshortener:latest .

compose-up:     ## Run app + Postgres + Prometheus + Grafana locally
	docker compose up --build

kind-up:        ## Create a local Kubernetes cluster
	kind create cluster --name flagship

image-load:     ## Load the local image into kind
	kind load docker-image urlshortener:latest --name flagship

k8s-apply:      ## Deploy raw manifests
	kubectl apply -f k8s/

helm-install:   ## Deploy via Helm
	helm upgrade --install urlshortener ./helm/urlshortener -n urlshortener --create-namespace

tf-init:        ## Initialise Terraform
	cd terraform && terraform init

tf-apply:       ## Deploy via Terraform (Helm provider)
	cd terraform && terraform apply

clean:          ## Delete the kind cluster
	kind delete cluster --name flagship
