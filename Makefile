test:
	python runtests.py

test-coverage:
	coverage run python runtests.py

test-coveralls:
	coveralls
