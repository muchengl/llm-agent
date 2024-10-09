

# Prerequests

Modify example_env.sh and rename to env.sh.

## Setup AWS & WebArenaServer
Init AWS toolchain
```shell
# 1) install aws cli, https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

# 2) set up aws access key and security key
aws configure
```

Deploy WebArena
```
cd aws
cdk bootstrap
cdk deploy
```

## Setup environment
```shell
./env.sh -e
```

## Init WebArena
```shell
cd env
./start_webarena.sh

./reset_webarena.sh

./restart_webarena.sh
```