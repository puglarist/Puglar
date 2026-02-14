.PHONY: build clean

build:
	python3 build_catalog.py

clean:
	rm -f catalog.json CATALOG.md
