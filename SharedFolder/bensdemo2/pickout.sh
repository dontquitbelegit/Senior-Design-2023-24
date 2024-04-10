#!/bin/bash

# The path to the input file containing the scan results.
INPUT_FILE="./scan.txt"
# The path to the output file where the extracted information will be saved.
OUTPUT_FILE="./pickout_text.txt"

# Extracting hostname and IP address
echo "Hostname and IP:" > "$OUTPUT_FILE"
grep "Nmap scan report for" "$INPUT_FILE" | awk '{print $5, $6}' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Extracting OS information
echo "Operating System Information:" >> "$OUTPUT_FILE"
grep -A 1 'OS details:' "$INPUT_FILE" | tail -n 1 >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Extracting additional details such as SMB OS Discovery
echo "SMB OS Discovery:" >> "$OUTPUT_FILE"
sed -n '/smb-os-discovery:/,/^$/p' "$INPUT_FILE" >> "$OUTPUT_FILE"

echo "Extraction complete. Details saved to $OUTPUT_FILE"

# Extracting open ports, their state, and the service running on them
echo "Open Ports and Services:" >> "$OUTPUT_FILE"
grep "/tcp" "$INPUT_FILE" | awk '{print $1, $2, $3}' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
