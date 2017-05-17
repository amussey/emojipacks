SHELL := /bin/bash
MAKEFILE_RULES := $(shell cat Makefile | grep "^[A-Za-z]" | awk '{print $$1}' | sed "s/://g" | sort -u)
PYTHON_ENV := ./env
PYTHON_BIN := $(PYTHON_ENV)/bin
PYTHON_REQS := ./requirements.txt

# Required binaries
BOWER := $(shell command -v bower 2> /dev/null)
NPM := $(shell command -v npm 2> /dev/null)
PYTHON27 := $(shell command -v python2.7 2> /dev/null)
PYTHON3 := $(shell command -v python3 2> /dev/null)
PIP := $(shell command -v pip 2> /dev/null)
CHROMEDRIVER := $(shell command -v chromedriver 2> /dev/null)
PHANTOMJS := $(shell command -v phantomjs 2> /dev/null)

.DEFAULT_GOAL := help


default: help


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


#=======================================
# External dependencies
#=======================================


npm:  ## Check if NPM is installed
ifndef NPM
	$(error "npm does not appear to be installed.  Please install Node.JS and NPM and try again.")
endif

# Install Emojipacks on your machine.
install: npm node_modules
	@npm link
	@echo
	@echo "\x1B[97m  emojipacks \x1B[90m·\x1B[39m Successfully installed Emojipack!"
	@echo "\x1B[97m             \x1B[90m·\x1B[39m Run \`emojipacks\` to get started."
	@echo


#=======================================
# External dependencies
#=======================================

node_modules:  ## Install node modules with npm.
node_modules: npm package.json
	@npm install
	@touch node_modules

#
# Phonies.
#

.PHONY: npm
.PHONY: clean
.PHONY: debug
.PHONY: run
.PHONY: server


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
