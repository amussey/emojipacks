# SHELL := /bin/bash
MAKEFILE_RULES := $(shell cat Makefile | grep "^[A-Za-z]" | awk '{print $$1}' | sed "s/://g" | sort -u)
PYTHON_ENV := ./env
PYTHON_BIN := $(PYTHON_ENV)/bin
PYTHON_REQS := ./requirements.txt
YAML_CONFIG := env.yml

# Required binaries
BOWER := $(shell command -v bower 2> /dev/null)
GRUNT := $(shell command -v grunt 2> /dev/null)
NPM := $(shell command -v npm 2> /dev/null)
PYTHON27 := $(shell command -v python2.7 2> /dev/null)
PYTHON3 := $(shell command -v python3 2> /dev/null)
PIP := $(shell command -v pip 2> /dev/null)
CHROMEDRIVER := $(shell command -v chromedriver 2> /dev/null)
PHANTOMJS := $(shell command -v phantomjs 2> /dev/null)


.DEFAULT_GOAL := help


default: help


$(YAML_CONFIG):
	touch $(YAML_CONFIG)



#=======================================
# External dependencies
#=======================================

env: virtualenv

.PHONY: virtualenv
virtualenv:  ## Set up the Python
virtualenv: python3 pip
	test -e $(PYTHON_BIN)/activate || virtualenv -p $(PYTHON3) $(PYTHON_ENV)
	$(PYTHON_BIN)/pip install -qr $(PYTHON_REQS)

write-virtualenv:  ## Update and rewrite the requirements.txt file.
	$(PYTHON_BIN)/pip freeze | grep -v appdirs > $(PYTHON_REQS)

python3:
ifndef PYTHON3
	$(error "python3.X does not appear to be installed. Please install it and try again.")
endif

pip:
ifndef PIP
	$(error "I require pip but it's not installed. Aborting.")
endif

npm:  ## Check if NPM is installed
ifndef NPM
	$(error "npm does not appear to be installed.  Please install Node.JS and NPM and try again.")
endif

grunt:  ## Check if grunt is installed
grunt: npm
ifndef GRUNT
	npm install -g grunt-cli
endif

node_modules:  ## Install node modules with npm.
node_modules: npm package.json
	@npm install
	@touch node_modules

#=======================================
# Runners
#=======================================

run: virtualenv
	$(PYTHON_BIN)/ipython3 emojipacks.py

shell: virtualenv
	$(PYTHON_BIN)/ipython3


#=======================================
# Linters
#=======================================

yaml-lint:  ## Lint and validate the YAML files.
yaml-lint: grunt
	grunt default

py-lint:  ## Lint and validate the Python files.
py-lint: virtualenv
	$(PYTHON_BIN)/flake8 emojipacks.py emojipacks/*.py test/*.py

lint:  ## Lint and validate the YAML and Python files.
lint: yaml-lint py-lint


#=======================================
# Miscellaneous
#=======================================

.PHONY: help
help:  ## This help dialog.
	@echo -e "You can run the following commands from this$(MAKEFILE_LIST):\n"
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//'`) ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$'#' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf "  %-27s %s\n" $$help_command $$help_info ; \
	done
