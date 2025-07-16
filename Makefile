dev:
	PYTHONPATH=src poetry run uvicorn pushorpay.main:app --reload

test:
	poetry run pytest

format:
	poetry run black src

lint:
	poetry run ruff src