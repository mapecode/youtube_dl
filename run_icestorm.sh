#!/bin/sh
#

CONFIG_FILE=icebox.config

rm -rf IceStorm/
mkdir -p IceStorm/

echo "Running IceBox, press Ctrl-C to end"
icebox --Ice.Config=$CONFIG_FILE
