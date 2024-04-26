#!/bin/bash

# Pre scan step: Recieve the duration amount from the user.
echo "Select the duration for the network traffic scan:"
echo "1) 1 hour"
echo "2) 6 hours"
echo "3) 12 hours"
echo "4) 1 day"
echo "5) 1.5 days"
echo "6) 2 days"
read -p "Enter your choice (1-6): " duration_choice

case $duration_choice in
    1) duration_seconds=$((1 * 1)) ;;  # 1 hour
    2) duration_seconds=$((6 * 3600)) ;;  # 6 hours
    3) duration_seconds=$((12 * 3600)) ;; # 12 hours
    4) duration_seconds=$((24 * 3600)) ;; # 1 day
    5) duration_seconds=$((36 * 3600)) ;; # 1.5 days
    6) duration_seconds=$((48 * 3600)) ;; # 2 days
    *) echo "Invalid selection. Exiting."; exit 1 ;;
esac

echo "Starting network traffic capture for $duration_seconds seconds."

# Step 1: Capture all packets from the Wi-Fi interface (en0) for 120 seconds
#CHANGE en0 to wlan0 for linux devices if not working
#sudo tshark -i en0 -a duration:$duration_seconds -w /Users/morgansinan/Desktop/captured_traffic.pcapng
#& TSHARK_PID=$!

(tshark -r "captured_traffic_3.pcapng" -T fields -e frame.number | wc -l) > total.txt

# Step 2: Extract DNS queries
tshark -r captured_traffic_3.pcapng -Y "dns.qry.name" -T fields -e dns.qry.name > /Users/morgansinan/Desktop/XML/dns.txt

# Step 3: Extract HTTP requests
tshark -r captured_traffic_3.pcapng -Y "http.request.full_uri" -T fields -e http.request.full_uri > /Users/morgansinan/Desktop/XML/http.txt

# Step 4: Count DNS and HTTP queries and add them to the corresponding XML
{
    echo '<?xml version="1.0" encoding="UTF-8"?>'
    echo '<DNSQueries>'
    (wc -l < dns.txt) > /Users/morgansinan/Desktop/XML/dns_total.txt
    total_dns=$(wc -l < dns.txt)
    echo "<Total>$total_dns</Total>"
    matches=$(grep -Ff malicious_domains_list.txt dns.txt)
    if [ -z "$matches" ]; then
        echo '<Matches>None found</Matches>'
    else
        echo '<Matches>'
        echo "$matches" | awk '{print "<Match>" $0 "</Match>"}'
        echo '</Matches>'
    fi
    echo '</DNSQueries>'
} > /Users/morgansinan/Desktop/XML/dns_total.xml

{
    echo '<?xml version="1.0" encoding="UTF-8"?>'
    echo '<HTTPQueries>'
    (wc -l < http.txt) > /Users/morgansinan/Desktop/XML/http_total.txt
    total_http=$(wc -l < http.txt)
    echo "<Total>$total_http</Total>"
    matches=$(grep -Ff malicious_domains_list.txt http.txt)
    if [ -z "$matches" ]; then
        echo '<Matches>None found</Matches>'
    else
        echo '<Matches>'
        echo "$matches" | awk '{print "<Match>" $0 "</Match>"}'
        echo '</Matches>'
    fi
    echo '</HTTPQueries>'
} > /Users/morgansinan/Desktop/XML/http_total.xml

# ADVANCED TRAFFIC ANALYSIS

# Step 6: Script to Detect High Volumes of Traffic
echo "Top 10 IP Endpoints by Data Volume"
echo "----------------------------------"
tshark -r captured_traffic_3.pcapng -T fields -e ip.src -e ip.dst -e frame.len \
    | awk '{ip[$1]+=$3; ip[$2]+=$3} END {for (i in ip) {print i, ip[i]}}' \
    | sort -nrk 2 | head -10 \
    | awk 'BEGIN{print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<TopIPs>"}; {print "<IP><Address>" $1 "</Address><DataBytes>" $2 "</DataBytes></IP>"}; END{print "</TopIPs>"}' > /Users/morgansinan/Desktop/XML/top_ips.xml

# Step 7: Script to Identify Unusual Protocols and Non-standard Port Usage
echo "Unusual Protocol Usage and Non-standard Ports"
echo "---------------------------------------------"
tshark -r captured_traffic_3.pcapng -q -z conv,ip \
    | grep -vE "443|80|22|25" \
    | sort -k 5 -nr | head -10 \
    | awk 'BEGIN{print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<UnusualProtocolUsage>"}; {print "<ProtocolEntry><Protocol>" $1 "</Protocol><SourcePort>" $3 "</SourcePort><DestinationPort>" $4 "</DestinationPort><Packets>" $5 "</Packets></ProtocolEntry>"} END{print "</UnusualProtocolUsage>"}' > /Users/morgansinan/Desktop/XML/unusual_protocols.xml

#Step 8: Script to Detect Repeated Failed Connection Attempts
echo "Repeated Failed Connection Attempts"
echo "------------------------------------"
tshark -r captured_traffic_3.pcapng -Y "tcp.flags.reset==1" -T fields -e ip.src \
    | sort | uniq -c | sort -nr | head -10 \
    | awk 'BEGIN{print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<FailedConnections>"}; {print "<Connection><IP>" $2 "</IP><ResetCount>" $1 "</ResetCount></Connection>"} END{print "</FailedConnections>"}' > /Users/morgansinan/Desktop/XML/failed_connections.xml

# Step 9: Script for Data Payload Inspection
echo "Suspicious Data Payloads"
echo "------------------------"
tshark -r captured_traffic_3.pcapng -Y 'data' -T fields -e ip.src -e ip.dst -e data.data \
    | head -20 \
    | awk 'BEGIN{print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<SuspiciousDataPayloads>"}; {print "<Payload><SourceIP>" $1 "</SourceIP><DestinationIP>" $2 "</DestinationIP><Data>" $3 "</Data></Payload>"} END{print "</SuspiciousDataPayloads>"}' > /Users/morgansinan/Desktop/XML/suspicious_payloads.xml

# Step 10: Script for ARP Traffic and Spoofing Detection
echo "ARP Traffic Analysis"
echo "---------------------"
tshark -r captured_traffic_3.pcapng -Y "arp" -T fields -e arp.src.hw_mac -e arp.src.proto_ipv4 \
    | sort | uniq -c | sort -nr \
    | head -10 \
    | awk 'BEGIN{print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ARPTraffic>"}; {if($1 > 1) print "<ARPEntry><MAC>" $2 "</MAC><IP>" $3 "</IP><Count>" $1 "</Count></ARPEntry>"} END{print "</ARPTraffic>"}' > /Users/morgansinan/Desktop/XML/arp_traffic.xml

# Assuming the Bash and Python scripts are in the same directory
python3 NT_test.py "/Users/morgansinan/Desktop/XML/NT_test.py"