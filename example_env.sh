#!/bin/bash

# Environment Variables

## OpenAI
OPENAI_API_KEY="sk-proj-...."

# GMAIL
GMAIL_APP_KEY="..."
EMAIL=""

# AWS
IP_RANGE="165.95.0.0/16"
AWS_CDK_DEFAULT_ACCOUNT=""
AWS_CDK_DEFAULT_REGION="us-east-2"

# Function to display help message
function show_help {
    echo "Usage: $0 -d | -e"
    echo "Options:"
    echo "  -d   Deploy using AWS CDK"
    echo "  -e   Set up environment variables"
}

# Function to handle CDK deployment
function deploy_cdk {
    cd aws || exit
    cdk deploy
}

# Function to set up environment variables
function setup_env_vars {
    export OPENAI_API_KEY="$OPENAI_API_KEY"
    export GMAIL_APP_KEY="$GMAIL_APP_KEY"
    export EMAIL="$EMAIL"
    export IP_RANGE="$IP_RANGE"
    export AWS_CDK_DEFAULT_ACCOUNT="$AWS_CDK_DEFAULT_ACCOUNT"
    export AWS_CDK_DEFAULT_REGION="$AWS_CDK_DEFAULT_REGION"

    # Run additional setup script and fetch the WebArena host
    source aws-cli.sh
    export WEBARENA_HOST=$(get_ec2_dns "Ec2Stack/WebArenaServer")
    echo "WebArena Host: $WEBARENA_HOST"
}

function init_web_arena {
    echo ./env/start
}

# Parse command-line arguments
while getopts "deh" option; do
    case $option in
        d)  deploy_cdk ;;
        e)  setup_env_vars ;;
        init) init_web_arena ;;
        h)  show_help ;;
        *)  show_help ;;
    esac
done

# If no arguments were passed, display help
if [ $# -eq 0 ]; then
    show_help
fi
