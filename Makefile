# Meta
NAME := xbokeh


# Install dependencies
.PHONY: deps
deps:
	pip install -r requirements.txt


# Run all unit tests
.PHONY: test
test:
	pytest tests/* -s
