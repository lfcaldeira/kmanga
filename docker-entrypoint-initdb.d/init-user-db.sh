#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER kmanga WITH encrypted password 'kmanga' ;
    CREATE DATABASE kmanga;
    GRANT ALL PRIVILEGES ON DATABASE kmanga TO kmanga;
EOSQL
