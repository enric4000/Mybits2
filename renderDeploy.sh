docker compose --env-file ./Mybits2/.env build
docker compose --env-file ./Mybits2/.env up -d db
docker compose --env-file ./Mybits2/.env up web