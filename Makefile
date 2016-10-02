PROJECT_NAME := $(shell python setup.py --name)
PROJECT_VERSION := $(shell python setup.py --version)

SHELL := /bin/bash
BOLD := \033[1m
DIM := \033[2m
RESET := \033[0m

.PHONY: install
install:
	@echo -e "$(BOLD)installing $(PROJECT_NAME) $(RESET)"
	@echo -e -n "$(DIM)"
	@python setup.py install
	@echo -e -n "$(RESET)"

.PHONY: uninstall
uninstall:
	@echo -e "$(BOLD)uninstalling '$(PROJECT_NAME)'$(RESET)"
	-@python setup.py uninstall

.PHONY: lint
lint:
	-@pylint libdesktop/**/*.py \
		--output-format text --reports no \
		--msg-template "{path}:{line:04d}:{obj} {msg} ({msg_id})" \
		| sort | awk \
			'/[RC][0-9]{4}/ {print "\033[2m" $$0 "\033[0m"};\
			 /[EF][0-9]{4}/ {print "\033[1m" $$0 "\033[0m"};\
			 /W[0-9]{4}/ {print};'

.PHONY: doc
doc:
	@cd doc && $(MAKE) html
	@cd ..

.PHONY: dist
dist:
	@python setup.py sdist --formats=zip --dist-dir=dist

.PHONY: upload
upload:
	@echo -e "$(BOLD)uploading $(PROJECT_NAME) $(RESET)"
	@sed -i -e "s/_version = [1-9]*/_version = $(VERSION)/g" setup.py
	@python setup.py sdist upload -r pypi

.PHONY: clean
clean:
	@rm -rf build dist $(PROJECT_NAME).egg-info
	@find -name '*.pyc' -exec 'rm -rf {}' \;
	@find -name '*.pyo' -exec 'rm -rf {}' \;
	@find -name '__pycache__' -exec 'rm -rf {}' \;

.PHONY: todo
todo:
	@find -name '*.py' -exec grep TODO /dev/null {} \; | sed 's/pass  //g'
