#!/bin/sh
set -e

REPO_NAME=$1
REPO_URL=$2
COMMIT_SHA=$3

mkdir -p /repositories
git clone "$REPO_URL" "/repositories/$REPO_NAME"
cd "/repositories/$REPO_NAME"
git reset --hard "$COMMIT_SHA"
