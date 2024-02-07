CC=podman

all: flower celery_workers backend vv8_backend_database

flower:
	cd flower; $CC build . -t registry.k3s.kapravelos.com/insecure_flower:latest --platform=linux/amd64; $CC push registry.k3s.kapravelos.com/insecure_flower:latest
celery_workers:
	cd celery_workers; $CC build -f vv8_worker.dockerfile -t registry.k3s.kapravelos.com/vv8_crawler_worker:latest --platform=linux/amd64; $CC push registry.k3s.kapravelos.com/vv8_crawler_worker:latest; $CC build -f log_parser.dockerfile -t registry.k3s.kapravelos.com/log-parser-worker:latest --platform=linux/amd64; $CC push registry.k3s.kapravelos.com/log-parser-worker:latest
backend:
	cd backend; $CC build . -t registry.k3s.kapravelos.com/vv8_backend:latest --platform=linux/amd64; $CC push registry.k3s.kapravelos.com/vv8_backend:latest
vv8_backend_database:
	cd vv8_backend_database; $CC build . -t registry.k3s.kapravelos.com/vv8_database:latest --platform=linux/amd64; $CC push registry.k3s.kapravelos.com/vv8_database:latest 
	
