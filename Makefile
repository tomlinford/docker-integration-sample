test: app_image
	nosetests tests

app_image:
	docker build -f docker/app/Dockerfile -t integration-app .
