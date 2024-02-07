ENGINE=podman

flower_image:
	cd flower; $(ENGINE) build . -t registry.k3s.kapravelos.com/insecure_flower:latest --platform=linux/amd64; $(ENGINE) push registry.k3s.kapravelos.com/insecure_flower:latest
celery_workers_image:
	cd celery_workers; $(ENGINE) build -f vv8_worker.dockerfile -t registry.k3s.kapravelos.com/vv8_crawler_worker:latest --platform=linux/amd64; $(ENGINE) push registry.k3s.kapravelos.com/vv8_crawler_worker:latest; $(ENGINE) build -f log_parser.dockerfile -t registry.k3s.kapravelos.com/log-parser-worker:latest --platform=linux/amd64; $(ENGINE) push registry.k3s.kapravelos.com/log-parser-worker:latest
backend_image:
	cd backend; $(ENGINE) build . -t registry.k3s.kapravelos.com/vv8_backend:latest --platform=linux/amd64; $(ENGINE) push registry.k3s.kapravelos.com/vv8_backend:latest
vv8_backend_database_image:
	cd vv8_backend_database; $(ENGINE) build . -t registry.k3s.kapravelos.com/vv8_database:latest --platform=linux/amd64; $(ENGINE) push registry.k3s.kapravelos.com/vv8_database:latest 

all: flower_image celery_workers_image backend_image vv8_backend_database_image