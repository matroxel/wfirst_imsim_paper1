#!/bin/bash
tar -xvf wfirst_stack.tar.gz
FILE=run.tar
if [ -f "$FILE" ]; then
    tar -xvf run.tar --strip-components=4
fi
source setup.sh
mkdir truth
mkdir images
mkdir stamps
mkdir ngmix
mkdir meds
python wfirst_imsim/wfirst_imsim/simulate.py3 $1 $2 $3 $4 $5
if [ -f "$FILE" ]; then
    rm truth/*truth_gal.fits
fi

