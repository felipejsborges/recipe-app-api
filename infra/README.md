export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""

CHDIR=setup
CHDIR=deploy

docker compose -f ./infra/docker-compose.yml run --rm terraform -chdir=$CHDIR init

docker compose -f ./infra/docker-compose.yml run --rm terraform -chdir=$CHDIR fmt

docker compose -f ./infra/docker-compose.yml run --rm terraform -chdir=$CHDIR validate

docker compose -f ./infra/docker-compose.yml run --rm terraform -chdir=$CHDIR plan

docker compose -f ./infra/docker-compose.yml run --rm terraform -chdir=$CHDIR apply

docker compose -f ./infra/docker-compose.yml run --rm terraform -chdir=$CHDIR output

docker compose -f ./infra/docker-compose.yml run --rm terraform -chdir=$CHDIR output my_sensitive_output
