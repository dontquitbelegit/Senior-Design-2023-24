#!/bin/bash

# Check if an IP address is provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <IP-address>"
    exit 1
fi

# The first argument is the IP address
IP_ADDRESS=$1

# Run nmap with -A option on the provided IP address
echo "Running nmap -A on IP address: $IP_ADDRESS"
nmap -A $IP_ADDRESS > scan.txt
sudo nmap -O $IP_ADDRESS | grep 'OS details:' >> scan.txt

