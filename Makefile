docker:
	# echo "I don't have this"
	cd flower
	docker build . -t registry.k3s.kapravelos.com/insecure_flower:latest --platform=linux/amd64
	docker push registry.k3s.kapravelos.com/insecure_flower:latest
	cd ../celery_workers
	docker build -f vv8_worker.dockerfile -t registry.k3s.kapravelos.com/vv8_crawler_worker:latest --platform=linux/amd64
	docker push registry.k3s.kapravelos.com/vv8_crawler_worker:latest
	docker build -f log_parser.dockerfile -t registry.k3s.kapravelos.com/log-parser-worker:latest --platform=linux/amd64
	docker push registry.k3s.kapravelos.com/log-parser-worker:latest
	cd ../backend
	docker build . -t registry.k3s.kapravelos.com/vv8_backend:latest --platform=linux/amd64
	docker push registry.k3s.kapravelos.com/vv8_backend:latest 
podman:
	cd flower; podman build . -t registry.k3s.kapravelos.com/insecure_flower:latest --platform=linux/amd64; podman push registry.k3s.kapravelos.com/insecure_flower:latest
	cd celery_workers; podman build -f vv8_worker.dockerfile -t registry.k3s.kapravelos.com/vv8_crawler_worker:latest --platform=linux/amd64; podman push registry.k3s.kapravelos.com/vv8_crawler_worker:latest; podman build -f log_parser.dockerfile -t registry.k3s.kapravelos.com/log-parser-worker:latest --platform=linux/amd64; podman push registry.k3s.kapravelos.com/log-parser-worker:latest
	cd backend; podman build . -t registry.k3s.kapravelos.com/vv8_backend:latest --platform=linux/amd64; podman push registry.k3s.kapravelos.com/vv8_backend:latest 
