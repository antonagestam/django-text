test:
	python runtests.py

test-coverage:
	coverage run runtests.py

test-coveralls:
	coveralls

dist:
	python setup.py sdist bdist_wheel upload
