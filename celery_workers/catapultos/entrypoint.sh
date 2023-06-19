#!/bin/bash
cd /go/src/github.com/catapult-project/catapult/web_page_replay_go
# go run src/wpr.go record --http_port=8080 --https_port=8081 /app/archive.wprgo
go run src/wpr.go replay --http_port=8080 --https_port=8081 /app/catapultos/archive.wprgo &
wait