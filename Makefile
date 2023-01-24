.PHONY: deploy

setup:
	brew install sass/sass/sass

build-css:
	sass scss/main.scss phoebesnotebook/static/css/main.css

run-debug:
	flask --app phoebesnotebook:app --debug run 

deploy:
	ansible-playbook -i deploy/hosts deploy/playbook.yml -vvv

check:
	black .
	flake8 phoebesnotebook
	isort .