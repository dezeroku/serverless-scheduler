#!/usr/bin/env bash

set -e

serverless remove

sls delete_domain

serverless remove-cert
