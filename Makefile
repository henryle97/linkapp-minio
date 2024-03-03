format:
	bash scripts/format_code.sh

deploy:
	docker-compose -f docker-compose.dev.yml  up --build