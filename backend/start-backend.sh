#!/bin/bash
echo "=== DEPORTEData backend arrancando ==="
echo "  SPARK_MASTER_IP: ${SPARK_MASTER_IP:-no definida}"
echo "  DB_HOST:         ${DB_HOST:-no definida}"
echo "  S3_BUCKET:       ${S3_BUCKET_DATALAKE:-no definida}"
echo "  NOM_USER_ID:      ${NOM_USER_ID:-no definida}"

python -m app.main
