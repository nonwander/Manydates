#!/bin/bash

if [ -f ./secretkey.txt ]; then
    echo "Secret key is already exists!"
    exit 0
fi

DJANGO_SECRET_KEY=$(python - <<EOF
import secrets
print(secrets.token_urlsafe())
EOF
)

echo "$DJANGO_SECRET_KEY" > ./secretkey.txt
chmod 400 ./secretkey.txt
unset DJANGO_SECRET_KEY