#!/bin/bash

bash ./nmapsearch.sh $1 ; bash ./pickout.sh ; bash ./pickout2.sh > pickout_text2.txt

python ./createreport.py
