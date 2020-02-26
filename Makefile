.PHONY: venv deps-no-venv test test-in-venv

venv:
	@python3 -m venv venv
	@source venv/bin/activate
	@pip install -r requirements.txt

deps-no-venv:
	@python3 -m pip install -r requirements.txt

test:
	@pytest

test-in-venv:
	@venv/bin/python3 -m pytest test
