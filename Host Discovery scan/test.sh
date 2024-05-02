#!/bin/bash

# Define the path for the XML file
xml_file="/Users/morgansinan/Desktop/host_discovery_scan_temp.xml"
#filename3="/Users/morgansinan/Desktop/arp_ip.txt" # This file will be used for Nmap scanning
echo -n > /Users/morgansinan/Desktop/arp_ip.txt

# Start the XML document
echo '<?xml version="1.0" encoding="UTF-8"?>' > "$xml_file"
echo '<arp_scan>' >> "$xml_file"

# Run arp to discover hosts and extract IPs and MACs
arp -a | while read -r entry; do
    # Extract IP address, removing parentheses
    ip=$(echo "$entry" | awk '{print $2}' | tr -d '()')
    # Extract MAC address, ensuring we get the complete address
    mac=$(echo "$entry" | awk '{print $4}')

    # Initialize the host entry with IP and MAC
    host_entry="<host><ip>($ip)</ip><mac>$mac</mac><fullmac>$mac</fullmac>"

    # Perform the Nmap scan on every IP and capture the output
    scan_output=$(nmap -Pn -sV --version-all "$ip")

    # Extract the hostname from the scan output, defaulting to "N/A" if not found
     hostname_extracted=$(echo "$scan_output" | grep 'Nmap scan report for' | head -1 | cut -d ' ' -f 5-)
    if [[ -z "$hostname_extracted" ]] || [[ "$hostname_extracted" == "$ip" ]]; then
        hostname_extracted="N/A"
    else
        # Remove the IP address if it's appended to the hostname in the nmap output
        hostname_extracted=$(echo "$hostname_extracted" | sed -E 's/ \([0-9\.]+\)$//')
    fi


    # Count the number of detected services
    services_count=$(echo "$scan_output" | grep '/tcp' | wc -l | xargs)
    if [ -z "$services_count" ] || [ "$services_count" -eq 0 ]; then
        services_count=0
    fi

    # If services were detected, append hostname and service count to the host entry
    if [ "$services_count" -ge 0 ]; then
        host_entry+="<hostname>$hostname_extracted</hostname><services>$services_count</services>"
    fi

    # Finalize the host entry and append it to the XML file
    host_entry+="</host>"
    echo "$host_entry" >> "$xml_file"
done

# Close the XML document
echo '</arp_scan>' >> "$xml_file"

echo "ARP and Nmap scanning complete. Results saved to $xml_file."

# Assuming the Bash and Python scripts are in the same directory
python3 HD_rpmakerV2.py "/Users/morgansinan/Desktop/HD_rpmakerV2.py"