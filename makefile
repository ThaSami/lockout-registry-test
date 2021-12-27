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

start-api:
	#sets PYTHONPATH to directory above, would do differently in production
	cd api && PYTHONPATH=".." python3 app.py

all: install lint test