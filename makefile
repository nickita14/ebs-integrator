APPS_SCHEMA = https
APPS_DOMAIN := ${APPS_DOMAIN}

compile_api:
	docker run --rm -w /work -v `pwd`:/work --user `id -u`:`id -g` django/binance python backend/manage.py spectacular -v 2 --file backend/openapi.yml
	docker run --rm -w /work -v `pwd`:/work --user `id -u`:`id -g` openapitools/openapi-generator-cli:v6.6.0 generate -i /work/backend/openapi.yml -o /work/frontend/src/services/api -g typescript-axios --server-variables schema=$(APPS_SCHEMA) --server-variables hostname=$(APPS_DOMAIN)
	rm backend/openapi.yml
