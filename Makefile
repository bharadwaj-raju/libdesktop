PROJECT_NAME := $(shell python setup.py --name)
PROJECT_VERSION := $(shell python setup.py --version)
PORT := 9980


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
	@echo -e "$(BOLD)making html docs for $(PROJECT_NAME) $(RESET)"
	@cd doc && $(MAKE) html
	@echo -e "$(BOLD)serving html docs at port $(PORT) $(RESET)"
	@cd doc/build/html && sh -c "python3 -m http.server $(PORT) 2>/dev/null >/dev/null & disown"
	@echo -e "$(BOLD)copying html to gh-pages"
	@git checkout gh-pages && git checkout master doc/build/html && mv -f doc/build/html/* ./ && rm -rf doc/ && git checkout master

.PHONY: test
test:
	@cd tests/ && py.test -s
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
	@rm -rf build
	@rm -rf dist

.PHONY: todo
todo:
	@find -name '*.py' -exec perl -lne 'print $$1 if /TODO: (.*)/' {} \; | uniq | sed -e 's/^/- /g'

.PHONY: new-release
new-release:
	@sed -i setup.py -e 's/_version = .*/_version = $(NEW_VERSION)/g'
	@python setup.py sdist upload -r pypi
	@sed -i doc/source/conf.py -e "s/version = .*/version = '$(NEW_VERSION)'/g"
	@git add .
	@git commit
	@git tag -a v$(NEW_VERSION) -m "$(RELEASE_MESSAGE)"
	@git push
