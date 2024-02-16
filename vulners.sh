#!/bin/bash
#soffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --nodefault

nmap_output=$(nmap -sV --script=vulners scanme.nmap.org)

current_datetime=$(date +"%Y_%m_%d_%H:%M:%S")

filename="nmap_results_${current_datetime}.txt"

# Save results to the file
echo "$nmap_output" > temp_nmap_results.txt

# Process each line containing CVEs and remove duplicates
grep -oP "CVE-[0-9]{4}-[0-9]{4,7}.*" temp_nmap_results.txt | sort | uniq | while read -r line; do
    # Extract CVE
    cve=$(echo "$line" | grep -oP "CVE-[0-9]{4}-[0-9]{4,7}")
    
    # Extract CVSS score
    cvss=$(echo "$line" | grep -oP "[0-9]\.[0-9]")

    # Extract URL (assuming it's the last element in the line)
    url=$(echo "$line" | grep -oP "http[^\s]*")

    # Append to the file with each element on a new line
    echo -e "$cve\nCVSS Score: $cvss\nURL: $url\n" >> "$filename"
done

rm temp_nmap_results.txt

#python_script_path="/home/kali/rpmaker.py"

#python "$python_script_path"



