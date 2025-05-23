#!/bin/bash

set -e

DOWNLOAD_DIR=$HOME/greenbone-community-container
RELEASE="22.4"

installed() {
    local failed=0
    if [ -z "$2" ]; then
        if ! [ -x "$(command -v "$1")" ]; then
            failed=1
        fi
    else
        local ret=0
        "$@" &> /dev/null || ret=$?
        if [ "$ret" -ne 0 ]; then
            failed=1
        fi
    fi

    if [ $failed -ne 0 ]; then
        echo "$* is not available. See https://greenbone.github.io/docs/latest/$RELEASE/container/#prerequisites."
        exit 1
    fi
}

installed curl
installed docker
installed docker compose

mkdir -p "$DOWNLOAD_DIR" && cd "$DOWNLOAD_DIR"

echo "Downloading docker-compose file..."
curl -f -O https://greenbone.github.io/docs/latest/_static/docker-compose.yml

echo "Pulling Greenbone Community Containers"
docker compose -f "$DOWNLOAD_DIR"/docker-compose.yml pull
echo

echo "Starting Greenbone Community Containers"
docker compose -f "$DOWNLOAD_DIR"/docker-compose.yml up -d
echo

read -r -s -p "Password for admin user: " password
echo
docker compose -f "$DOWNLOAD_DIR"/docker-compose.yml \
    exec -u gvmd gvmd gvmd --user=admin --new-password="$password"

echo
echo "The feed data will now load. This process can take several minutes to hours."
echo "Refer: https://greenbone.github.io/docs/latest/$RELEASE/container/workflows.html#loading-the-feed-changes"
echo

# Display access instructions instead of trying to launch a browser
IP=$(hostname -I | awk '{print $1}')
echo "Access the Greenbone Security Assistant web interface at: http://$IP:9392"
