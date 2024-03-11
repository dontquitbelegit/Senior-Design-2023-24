#!/bin/bash

expect ./test.sh ; bash ./pickout.sh > pickout_text.txt

python ./createreport.py
