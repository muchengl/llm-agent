# LLM Agent Research Pipeline

## Environment Setup Pipeline

Modify example_env.sh and rename it to env.sh.

### Setup AWS & WebArenaServer
Init AWS toolchain
```shell
# 1) install aws cli, https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

# 2) set up aws access key and security key
aws configure
# set aws_access_key_id
# set aws_secret_access_key
```

Deploy WebArena Server
```
cd aws
cdk bootstrap
cdk deploy
```

### Setup Environment variables
```shell
./env.sh -e
```

### Init WebArena Environment
```shell
cd env
./start_webarena.sh

# reset to init status
./reset_webarena.sh

# restart env
./restart_webarena.sh
```

## Evaluation Pipeline