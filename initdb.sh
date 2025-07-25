#!/bin/bash
set -e

echo ">> Aguardando o MySQL iniciar..."

until mysqladmin ping -h "localhost" --silent; do
    sleep 1
done

echo ">> Criando usuário de aplicação '${DB_USER} no banco '${DB_NAME}'..."

mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" <<-EOSQL
    CREATE USER IF NOT EXISTS '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}';
    GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '${DB_USER}'@'%';
    FLUSH PRIVILEGES;
EOSQL

echo ">> Script de inicialização concluído!"
