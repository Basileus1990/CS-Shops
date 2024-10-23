#!/bin/bash
# This script is used to remove all data from volumes for a fresh start
# Has to be run as a root user

CURRENT=`pwd`
BASENAME=`basename "$CURRENT"`
if [ $BASENAME != "scripts" ]
  then echo "Please run from the scripts directory"
  exit
fi

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

rm -rf ../../shop/data
