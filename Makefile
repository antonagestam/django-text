test:
	python runtests.py

test-coverage:
	coverage run runtests.py

test-coveralls:
	coveralls
