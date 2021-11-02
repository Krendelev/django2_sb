#!/bin/bash

# https://stackoverflow.com/a/3278427
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]
then
    echo -e "\033[32mAlready up to date.\033[0m"
    exit 1
elif [ $REMOTE = $BASE ]
then
    echo -e "\033[31mAhead of origin. Resolve conflict.\033[0m"
    exit 1
fi

git pull --rebase
sudo npm install --dev
sudo npm install -g parcel@latest
parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
source venv/bin/activate
pip install -r requirements.txt
./manage.py collectstatic --noinput
./manage.py migrate
sudo systemctl restart starburger.service

export $(cat .env)
curl -X POST https://api.rollbar.com/api/1/deploy \
                -H "X-ROLLBAR-ACCESS-TOKEN: $ROLLBAR_ACCESS_TOKEN" \
                --form environment="production" \
                --form revision=$REMOTE \
                --form local_username=$USER

echo -e "\n\033[32mSuccess! Let's cook some burgers.\033[0m\n"
