#!/bin/sh

mkdir demo-python-sample
cd demo-python-sample
cdk init
cdk init --language python sample-app

npm uninstall -g cdk
npm install -g aws-cdk
#setup.py : add aws_kinesis & aws_kinesis_firehose @ 1.74.0

source .venv/bin/activate
pip install -r requirements.txt
cdk synth
cdk deploy
cdk destroy