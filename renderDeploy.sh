#!/usr/bin/env bash

# Build the Docker images
docker compose --env-file ./Mybits2/.env build

# Start the database service
docker compose --env-file ./Mybits2/.env up -d db

# Start the web service
docker compose --env-file ./Mybits2/.env up web