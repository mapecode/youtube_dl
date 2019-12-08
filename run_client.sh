#!/bin/sh

PYTHON=python3

CLIENT_CONFIG=server.config

$PYTHON client.py --Ice.Config=$CLIENT_CONFIG "$1" "$2"
