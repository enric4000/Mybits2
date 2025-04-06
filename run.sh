echo "
=============================
Building containers
=============================
"
sudo docker compose --env-file ./Mybits2/.env build


# Si el parámetro es "run", levanta la base de datos y el contenedor web
if [ "$1" == "run" ]; then
    echo "
    =============================
    Deploying db container
    ============================="
    sudo docker compose --env-file ./Mybits2/.env up -d db

    echo "
    =============================
    Waiting for db to start
    ============================="
    sleep 15

    echo "
    =============================
    Deploying web container
    ============================="
    sudo docker compose --env-file ./Mybits2/.env up -d web


# Si el parámetro es "db", levanta solo la base de datos y ejecuta psql
elif [ "$1" == "db" ]; then
    echo "
    =============================
    Deploying db container
    ============================="
    sudo docker compose --env-file ./Mybits2/.env up -d db


# Si el parámetro es "tests", levanta la base de datos, el contenedor web y corre los tests
elif [ "$1" == "test" ]; then
    echo "
    =============================
    Deploying db container
    ============================="
    sudo docker compose --env-file ./Mybits2/.env up -d db

    echo "
    =============================
    Waiting for db to start
    ============================="
    sleep 15

    echo "
    =============================
    Deploying web container
    ============================="
    sudo docker compose --env-file ./Mybits2/.env up -d web

    echo "
    =============================
    Waiting for web to start
    ============================="
    sleep 15

    # Ejecutamos el contenedor de test
    sudo docker compose --env-file ./Mybits2/.env up test

    if [ $? -eq 0 ]; then
        echo "---------------------------Tests passed---------------------------"
    else
        echo "
        ========================================
        =            Tests FAILED              =
        ========================================"
    fi

#Si el parámetro es clean, limpiamos los datos de docker
elif [ "$1" == "clean" ]; then
    echo "
    ===============================================
    Cleaning data, this make take a few minutes...
    ==============================================="

    # Limpiamos los datos de docker
    sudo docker compose --env-file ./Mybits2/.env down --remove-orphans && sudo docker system prune


else
    echo "
    Uso incorrecto del script. Usa 'run', 'db', 'test' o 'clean' como parámetro.


    run: Levanta la base de datos y el contenedor web.
    db: Levanta solo la base de datos y ejecuta psql para poder modificarla.
    test: Levanta la base de datos, el contenedor web y ejecuta los tests.
    clean: Limpia los datos de docker residuales
    
    Recuerda comrpobar si has actualizado las aplicacions de Django en el settings.py y el docker-compose.yml antes de ejecutar el run!
    Si las actualizas, recuerda que igual debes limpiar la base de datos si hay cambios imposibles para el ORM en los modelos existentes.
    Puedes usar este script con db para hacerlo.
    "
    exit 1
fi
