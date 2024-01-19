#!/bin/bash
rm /tmp/.X1-lock 2> /dev/null &
/opt/noVNC/utils/novnc_proxy --vnc localhost:$VNC_PORT --listen $NO_VNC_PORT &
# Insecure option is needed to accept connections from the docker host.
# mitmdump -w /app/har/http_proxy.flow -p 7007 & # Comment this out if you are 100% not going to be using HARs!
vncserver $DISPLAY -depth $VNC_COL_DEPTH -geometry $VNC_RESOLUTION -SecurityTypes None -localhost no --I-KNOW-THIS-IS-INSECURE &
celery -A vv8_worker.app worker -Q crawler -l INFO -c $CELERY_CONCURRENCY -Ofair --max-tasks-per-child 1 &
wait