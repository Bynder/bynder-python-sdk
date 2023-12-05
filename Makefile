.PHONY: test
test: lint unittest

.PHONY: unittest
unittest:
	@rm -f coverage.xml cobertura.xml
	python setup.py test

.PHONY: lint
lint: clean
	@echo ">> Linting"
	python setup.py lint

.PHONY: clean
clean:
	@echo ">> Cleaning"
	@find . -name \.AppleDouble -exec rm -rf {} +
	@rm -rf build dist

.PHONY: dist
dist: clean
	@echo ">> Building"
	@python setup.py bdist_wheel
	@echo "!! Build ready"

.PHONY: listdeps
listdeps:
	@python setup.py listdeps | tail -n 1

.PHONY: testdeps
testdeps:
	@python setup.py testdeps | tail -n 1

.PHONY: typehint
typehint:
	mypy --ignore-missing-imports --follow-imports=skip $(DISTNAME)

# make executeSdkSample sample-file-name=metaproperties.py
.PHONY: executeSdkSample
executeSdkSample:
	docker-compose exec bynder-python-sdk python /app/samples/$(sample-file-name)