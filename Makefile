PYTHON=python
TESTS_DIR=tests
TESTS=$(wildcard $(TESTS_DIR)/*.py)

.PHONY: tests

tests:
	@echo Running tests...
	@passed=0; \
	total=0; \
	for test in $(TESTS); do \
		echo "Running test: $$test"; \
		if $(PYTHON) $$test; then \
			passed=$$((passed+1)); \
		fi; \
		total=$$((total+1)); \
	done; \
	echo "Passed $$passed out of $$total tests";
