DOCKER_EXE		= docker exec -i
DOCKER_EXE_TTY	= docker exec -it
DCO_EXE			= docker-compose
PYTHON			= ${DOCKER_EXE_TTY} cmdbot_web_1 python

up:
	${DCO_EXE} up -d
up_bot:
	${DCO_EXE} up -d web
stop:
	${DCO_EXE} stop
update build:
	${DCO_EXE} build
init:
	${PYTHON} init.py
watch:
	${DOCKER_EXE_TTY} cmdbot_web_1 pem watch
migrate:
	${DOCKER_EXE_TTY} cmdbot_web_1 pem migrate

bash ssh:
	${DOCKER_EXE_TTY} cmdbot_web_1 bash