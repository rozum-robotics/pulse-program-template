.PHONY: venv deps-no-venv test test-in-venv ci-test

venv:
	@python3 -m venv venv
	@source venv/bin/activate
	@pip install -r requirements.txt

deps-novenv:
	@python3 -m pip install -r requirements.txt -i https://pip.rozum.com/simple

test-novenv:
	@pytest

test-invenv:
	@venv/bin/python3 -m pytest test

ci-test: deps-novenv test-novenv
