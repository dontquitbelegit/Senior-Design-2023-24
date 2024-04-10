#!/bin/bash


expect ./test.sh $1 ; bash ./pickout.sh > pickout_text.txt

python ./createreport.py
