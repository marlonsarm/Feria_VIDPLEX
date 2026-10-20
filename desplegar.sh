#!/bin/bash
# Monta o actualiza la feria en el servidor: bash desplegar.sh
cd "$(dirname "$0")"
git pull
if [ ! -f .env ]; then
cat > .env <<EOF
SECRET_KEY=$(openssl rand -hex 32)
DB_HOST=db
DB_PORT=3306
DB_USER=feria
DB_PASSWORD=$(openssl rand -hex 16)
DB_NAME=vidplex
MYSQL_ROOT_PASSWORD=$(openssl rand -hex 16)
SITE_URL=http://192.168.121.104:8090
EOF
chmod 600 .env
fi
docker compose up -d --build
echo "Esperando la base de datos..."
until [ "$(docker inspect -f '{{.State.Health.Status}}' feria-mysql)" = "healthy" ]; do sleep 3; done
if [ -z "$(docker exec feria-mysql sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -N -e "SHOW TABLES" vidplex 2>/dev/null')" ]; then
  docker exec -i feria-mysql sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD" vidplex' < ~/feria_datos.sql && echo "Datos importados"
else
  echo "La base ya tenia datos, no se toco"
fi
docker compose restart web
sleep 4
docker compose ps
echo "Respuesta de la pagina: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:8090)"