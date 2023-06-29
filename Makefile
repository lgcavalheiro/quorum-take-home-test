ready-env:
	python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

run:
	python -m src.main

test:
	python -m coverage run -m unittest -v src/*_test.py && python -m coverage html

