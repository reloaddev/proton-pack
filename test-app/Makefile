.PHONY: up down logs psql reset
up:
	docker compose up -d --build
down:
	docker compose down
logs:
	docker compose logs -f db
psql:
	docker compose exec db psql -U sw -d starwars
reset:     ## nuke data
	docker compose down -v
