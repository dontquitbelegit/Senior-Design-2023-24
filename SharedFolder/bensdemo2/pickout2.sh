#!/bin/bash

# Define the output log file
input_file="pickout_text.txt"
output_file="pickout_text2.txt"

# Use grep with -A 1 to get the line after the match as well
# Then, use awk to check if the next line is empty
pattern1="Hostname and IP"
#bookmark1= grep -A 1 "$pattern1" "$input_file" | tail -n 1
following_line=$(grep -A 1 "$pattern1" "$input_file" | tail -n 1)
if [ -z "$following_line" ]; then
    echo "The IP couldn't be reached"
    echo "Please look above in the Excecutive Summary for troubleshooting"
    echo "As no IP could be resolved, no further information can be shown"
else
    echo "The IP address of the scanned device is: '$following_line'"
fi

echo "$"

f2=$(grep -A 1 "Operating System Information" "$input_file" | tail -n 1)
if [ -z "$f2" ]; then
    echo ""
else
    f2=${f2#????????????}
    echo "The OS of the device is presumed to be: '$f2' "
fi

echo "$"

f3=$(grep -A 0 "|   Computer name:" "$input_file")
if [ -z "$f3" ]; then
    echo "No hostname could be resolved"
    echo "To get the computer name, you'll have to log into the PC manually"
    echo "However, this isnt required for future functionality,"
    echo "but rather, merely as a convenience measure"
else
    f3=${f3#???????????????????}
    echo "The name of the device: '$f3' "
fi

echo "$"

line_number=$(grep -n -m 1 "Open Ports and Services:" "$input_file" | cut -d: -f1)
if [ ! -z "$line_number" ]; then
    echo "Below are the services found running on the computer"
    echo "A large number of services indicate that this is likely your server or some other important device"
    echo "The table is ordered like so: (number)/(tcp or udp) (open/closed/blocked) (service name)"
    echo "The number is what port the service runs on, followed by whether it uses tcp or udp"
    echo "If the service is turned off so to speak or not accepting users, it will be labelled as closed or blocked"
    echo "Lastly, the name of the service is at the end. This name is used in CATS vulnerability assessments"
    echo "If you'd like to learn more about what each service listed does or have questions about certain terms,"
    echo "go to https://techterms.com where user friendly definitions to any of the service names below can be found!"
    echo ""
    echo " Port | State | Service "
    echo ""
    tail -n +$((line_number + 1)) "$input_file"
else
    echo "No services could be found"
    echo "This possibly means that the computer is either a workstation, or a personal device"
    echo "However, this isnt garunteed, and factors like a firewall could be blocking the scan"
    echo "Please re-run the script to verify"
fi

