.PHONY: build build-all test clean

build:
	python3 tools/threegs_build.py docs/world_core.3gs --out build/world_core

build-all: build

test:
	python3 -m unittest discover -s tests -p 'test_*.py'

clean:
	rm -rf build
