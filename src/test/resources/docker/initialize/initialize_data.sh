#!/bin/sh
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

####################### Splunk server data


wget --http-user=admin --http-password=admin --auth-no-challenge \
     --header="Accept: application/json" \
     --header="Content-type: application/json" \
     --post-file=$SCRIPTPATH/data/server-configs.json \
    http://localhost:5516/repository/cis -O /dev/null
