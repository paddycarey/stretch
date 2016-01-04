#!/bin/bash
set -e

docker run -ti \
    -e SHPKPR_APPLICATION=stretch-example-web-service \
    -e SHPKPR_MARATHON_URL=$1 \
    -v "`pwd`":/usr/deploy \
    shopkeep/shpkpr:v0.1.0a7 \
    shpkpr deploy -t /usr/deploy/deploy.json
