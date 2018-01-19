clean:
	find . -name __pycache__ -type d | xargs rm -rf
	find . -name "*.pyc" | xargs rm -rf

docker: docker_web docker_worker

docker_web: clean
	docker build -t web:latest -f docker/web .

docker_worker: clean
	docker build -t worker:latest -f docker/worker .
