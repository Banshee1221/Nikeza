#!/bin/bash

TIMEOUT=6
COUNT=0
while [ ! -f /var/lib/cloud/instance/boot-finished ]
do
  if [ "$COUNT" -gt "$TIMEOUT" ]
  then
    echo "timeout"
    exit
  fi
  sleep 2
  ((COUNT+=2))
done
ERR=$(cat /var/lib/cloud/data/result.json | jq ".v1 .errors")
if [ "$ERR" != "[]" ]
then
  echo "cloud-init did not succeed"
  exit
fi

#DATA FOLDER CREATION

#DATA PULLING

#DO STUFF

#DATA STORAGE

#DONE