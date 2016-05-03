all: clean build

clean:
	python setup.py clean
	rm -rf dist build *egg-info *.pyc __pycache__

build:
	python setup.py bdist_egg sdist
