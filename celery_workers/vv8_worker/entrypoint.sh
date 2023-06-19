#!/bin/bash
rm /tmp/.X1-lock 2> /dev/null &
/opt/noVNC/utils/launch.sh --vnc localhost:$VNC_PORT --listen $NO_VNC_PORT &
# Insecure option is needed to accept connections from the docker host.
vncserver $DISPLAY -depth $VNC_COL_DEPTH -geometry $VNC_RESOLUTION -SecurityTypes None -localhost no --I-KNOW-THIS-IS-INSECURE &
# go run src/wpr.go replay --http_port=8080 --https_port=8081 /tmp/archive.wprgo
celery -A vv8_worker.app worker -Q crawler -l INFO -c $CELERY_CONCURRENCY &
wait