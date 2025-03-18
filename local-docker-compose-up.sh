source "./util.sh"

# --- docker compose up https://docs.docker.com/reference/cli/docker/compose/up/
  echo "docker compose up ..."
  COMPOSE_BAKE=true \
\
docker compose \
		-p tg-channel-aggregator \
		up --build -d

docker image prune -f || error_exit_w

ok_exit_w