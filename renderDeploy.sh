sudo docker compose --env-file ./Mybits2/.env build
sudo docker compose --env-file ./Mybits2/.env up -d db
sudo docker compose --env-file ./Mybits2/.env up web