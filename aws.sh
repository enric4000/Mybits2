git reset --hard
git fetch --all
git reset --hard origin/develop

sed -i 's/docker compose/docker-compose/g' run.sh
