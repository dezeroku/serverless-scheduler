#!/usr/bin/env bash

set -e

serverless remove-cert

sls delete_domain

serverless client remove --no-confirm

serverless remove
