PROJECT_NAME := $(shell python setup.py --name)
PROJECT_VERSION := $(shell python setup.py --version)

SHELL := /bin/bash
BOLD := \033[1m
DIM := \033[2m
RESET := \033[0m

.PHONY: all
all: uninstall install clean

.PHONY: install
install:
	@echo -e "$(BOLD)installing $(PROJECT_NAME) $(PROJECT_VERSION)$(RESET)"
	@echo -e -n "$(DIM)"
	@python setup.py install
	@echo -e -n "$(RESET)"

.PHONY: uninstall
uninstall:
	@echo -e "$(BOLD)uninstalling '$(PROJECT_NAME)'$(RESET)"
	-@python setup.py uninstall

.PHONY: lint
lint:
	@echo -e "$(BOLD)analyzing code for $(PROJECT_NAME) $(PROJECT_VERSION)$(RESET)"
	-@pylint libdesktop/**/*.py \
		--output-format text --reports no \
		--msg-template "{path}:{line:04d}:{obj} {msg} ({msg_id})" \
		| sort | awk \
			'/[RC][0-9]{4}/ {print "\033[2m" $$0 "\033[0m"};\
			 /[EF][0-9]{4}/ {print "\033[1m" $$0 "\033[0m"};\
			 /W[0-9]{4}/ {print};'

.PHONY: doc
doc:
	@echo -e "$(BOLD)building documentation for $(PROJECT_NAME) $(PROJECT_VERSION)$(RESET)"
	@echo -e -n "$(DIM)"
	@cd doc && $(MAKE) html
	@cd ..
	@echo -e -n "$(RESET)"

.PHONY: dist
dist:
	@echo -e "$(BOLD)packaging $(PROJECT_NAME) $(PROJECT_VERSION)$(RESET)"
	@echo -e -n "$(DIM)"
	@python setup.py sdist --formats=zip --dist-dir=dist
	@echo -e -n "$(RESET)"

.PHONY: upload
upload:
	@echo -e "$(BOLD)uploading $(PROJECT_NAME) $(PROJECT_VERSION)$(RESET)"
	@echo -e -n "$(DIM)"
	@sed -i -e "s/_version = [1-9]*/_version = $(VERSION)/g" setup.py
	@python setup.py sdist upload -r pypi
	@echo -e -n "$(RESET)"

.PHONY: clean
clean:
	@echo -e "$(BOLD)cleaning $(PROJECT_NAME) $(PROJECT_VERSION) repository$(RESET)"
	@rm -rf build dist $(PROJECT_NAME).egg-info
	@find -name '*.pyc' -exec 'rm -rf {}' \;
	@find -name '*.pyo' -exec 'rm -rf {}' \;
	@find -name '__pycache__' -exec 'rm -rf {}' \;


