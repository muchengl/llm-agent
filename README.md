# Website LLM Agent Pipeline

## WebArena Environment Setup Pipeline

Modify example_setup.sh and rename it to setup.sh.

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
```shell
export IP_RANGE="0.0.0.0/32" # https://whatismyipaddress.com/
export AWS_CDK_DEFAULT_ACCOUNT="0123456789"
export AWS_CDK_DEFAULT_REGION="us-east-2"

cd aws
cdk bootstrap
cdk deploy

# or
./setup.sh
```

### Init WebArena Environment
```shell
export WEBARENA_HOST="http://ec2-xxxxxx.us-east-2.compute.amazonaws.com:4399"
```

```shell
cd env
./start_webarena.sh

# reset to init status
./reset_webarena.sh

# restart env
./restart_webarena.sh
```

Then manually configure the environment variables

## LLM Agent & Evaluation Pipeline

```shell
pip install -r requirements.txt
playwright install
pip install -e .
```

### Basic Agent 

Prepare Env:
```shell
cd basic_agent 
./prepare.sh

python scripts/generate_test_data.py
```

OpenAI Setup:
```shell
export OPENAI_API_KEY=sk-.....
```

Run Agent:
```shell
python run.py \                                                                       
  --instruction_path agent/prompts/jsons/p_cot_id_actree_2s.json \
  --test_start_idx 11 \
  --test_end_idx 200 \
  --model gpt-4o \
  --result_dir ./result
```

Reset Env:
```shell
cd ..
./env/reset_webarena.sh
```