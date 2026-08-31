.PHONY: seo-before seo-test

seo-before:
	python3 scripts/seo/collect.py

seo-test:
	python3 scripts/seo/test_schema.py
	python3 scripts/seo/test_collect.py
