#!/bin/bash
set -e
pip install service_identity
psql -c "CREATE DATABASE kmanga;" -U postgres
exec "$@"
