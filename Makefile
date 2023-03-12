start-local:
	uvicorn evento.main:app --reload

start-db:
	docker-compose up -d postgres

start:
	docker-compose up -d

migration-create:
	alembic revision --autogenerate -m "$(name)"

migration-run:
	alembic upgrade head

enter-db:
	docker exec -it postgres psql -U postgres startup