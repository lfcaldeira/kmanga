#!/bin/bash
set -e
cd /kmanga
pip install -r requirements.txt
pip install service_identity
wget http://kindlegen.s3.amazonaws.com/kindlegen_linux_2.6_i386_v2_9.tar.gz
tar -xzvf kindlegen_linux_2.6_i386_v2_9.tar.gz -C /kmanga/kmanga
mv /kmanga/kmanga/kindlegen /kmanga/kmanga/bin
exec "$@"
