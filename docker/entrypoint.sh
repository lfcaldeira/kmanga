#!/bin/bash
set -e
cd /kmanga
pip install -r requirements.txt
exec "$@"
