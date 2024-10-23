#!/bin/bash
# This script is used to create volumes for a fresh start
# Has to be run as not root user

CURRENT=`pwd`
BASENAME=`basename "$CURRENT"`
if [ $BASENAME != "scripts" ]
  then echo "Please run from the scripts directory"
  exit
fi

if [ "$EUID" == 0 ]
  then echo "Please run not as root user"
  exit
fi

mkdir ../../shop
mkdir ../../shop/data
mkdir ../../shop/data/dbdata
mkdir ../../shop/data/psdata
