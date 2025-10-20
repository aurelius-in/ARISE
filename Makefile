.PHONY: setup run ui api test lint docker-up docker-down

setup:
	pip install -r requirements.txt

run:
	streamlit run src/ui/app.py

ui:
	streamlit run src/ui/app.py

api:
	uvicorn src.api.app:app --reload

test:
	pytest -q

docker-up:
	docker compose -f software/docker-compose.yml up --build -d

docker-down:
	docker compose -f software/docker-compose.yml down

