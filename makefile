env:
	#Show information about environment
	which python3
	python3 --version
	which pytest
	which pylint

lint:
	@cd api; pylint --load-plugins pylint_flask --disable=R,C *.py

test:
	@cd tests; pytest -vv -c config.ini

install:
	pip3 install -r requirements.txt 

start-api: install
	@cd api; METRICS_PORT=9200 gunicorn -c config.py app:app -w 2 -b 0.0.0.0:8080

all: install lint test