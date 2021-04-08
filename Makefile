
.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

update: ## Update the local repo
	@git pull

al-test: update ## Alvaro, corre esto	
	C:/Python27/ArcGISx6410.8/python.exe ./intentando.py


