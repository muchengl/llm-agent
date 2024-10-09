#!/bin/bash

# Environment Variables

## OpenAI
OPENAI_API_KEY="sk-..."
GMAIL_APP_KEY="..."
EMAIL="...@gmail.com"

# AWS
IP_RANGE="0.0.0.0/24"
AWS_CDK_DEFAULT_ACCOUNT="0123456789"
AWS_CDK_DEFAULT_REGION="us-east-2"

# Function to display help message
function show_help {
    echo "Usage: $0 -d | -e"
    echo "Options:"
    echo "  -d   Deploy using AWS CDK"
    echo "  -e   Set up environment variables"
    echo "  -w   Init WebArena"
}


# Function to set up environment variables
function setup_env_vars {
    echo "Setting up environment variables..."
    export OPENAI_API_KEY="$OPENAI_API_KEY"
    export GMAIL_APP_KEY="$GMAIL_APP_KEY"
    export EMAIL="$EMAIL"

    export IP_RANGE="$IP_RANGE"
    export AWS_CDK_DEFAULT_ACCOUNT="$AWS_CDK_DEFAULT_ACCOUNT"
    export AWS_CDK_DEFAULT_REGION="$AWS_CDK_DEFAULT_REGION"
}

# Function to handle CDK deployment
function deploy_cdk {
    cd aws || exit
    cdk deploy
    cd ..

    # Run additional setup script and fetch the WebArena host
    source ./aws/aws-cli.sh
    export WEBARENA_HOST=$(get_ec2_dns "WebArenaEc2Stack/WebArenaServer")
    echo "WebArena Host: $WEBARENA_HOST"
}

function init_web_arena {
    ./env/start_webarena.sh
}


setup_env_vars

deploy_cdk

init_web_arena