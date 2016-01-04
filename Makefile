.PHONY: build run test

ifdef LOG_LEVEL
LOG_LEVEL_FLAG=-e "LOG_LEVEL=$(LOG_LEVEL)"
endif

ifdef MARATHON_URL
MARATHON_URL_FLAG=-e "MARATHON_URL=$(MARATHON_URL)"
endif

ifdef SLEEP_SECONDS
SLEEP_SECONDS_FLAG=-e "SLEEP_SECONDS=$(SLEEP_SECONDS)"
endif

ifdef LOCAL_DEBUG
LOCAL_DEBUG_FLAG=-e "LOCAL_DEBUG=$(LOCAL_DEBUG)"
endif

VERSION=$(shell git describe --always --dirty --tags)
IMAGE_VERSION=$(shell echo "paddycarey/stretch:$(VERSION)")

build:
	docker build -t $(IMAGE_VERSION) .

run: build
	docker run -ti $(LOCAL_DEBUG_FLAG) $(LOG_LEVEL_FLAG) $(MARATHON_URL_FLAG) $(SLEEP_SECONDS_FLAG) $(IMAGE_VERSION)

test: build
	docker run -ti $(IMAGE_VERSION) py.test --pep8 --flakes --mccabe --cov=bin --cov=stretch --cov-report=term-missing
