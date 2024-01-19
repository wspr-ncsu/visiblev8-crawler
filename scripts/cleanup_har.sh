#!/usr/bin/env bash
# Shut down the crawler
docker compose down
# Get the latest HAR file from /har and move it to /har_archives
mv /har/http_proxy.flow /har_archives/http_proxy_$(date +%s).flow
# restart the crawler
docker compose up -d