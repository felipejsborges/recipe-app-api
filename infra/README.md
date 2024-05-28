ensure you are in the ./infra folder in the cli

export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""

CHDIR=setup
CHDIR=deploy

docker compose run --rm terraform -chdir=$CHDIR init

docker compose run --rm terraform -chdir=$CHDIR fmt

docker compose run --rm terraform -chdir=$CHDIR validate

docker compose run --rm terraform -chdir=$CHDIR plan

docker compose run --rm terraform -chdir=$CHDIR apply

docker compose run --rm terraform -chdir=$CHDIR output

docker compose run --rm terraform -chdir=$CHDIR output my_sensitive_output

