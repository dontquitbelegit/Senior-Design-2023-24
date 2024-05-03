#MAC Lookup and Replacement.py
#Define the path to the files
file_a_path = 'MyNetwork.csv'
file_b_path = 'Discovery.csv'
#file_a_path = 'filea.txt'
#file_b_path = 'fileb.txt'

# Read the contents of file A and store them in a dictionary for easy lookup
file_a_contents = {}
with open(file_a_path, 'r') as file:
    for line in file:
        ip, mac, name = line.strip().split(',')
        file_a_contents[mac] = {'ip': ip, 'name': name}

# Open file B and process each line
with open(file_b_path, 'r') as file:
    for line in file:
        ip_b, mac_b, name_b = line.strip().split(',')
        # If the MAC address exists in file A, update the IP
        if mac_b in file_a_contents:
            file_a_contents[mac_b]['ip'] = ip_b
        else:
            # If the MAC address is not found, add the new entry
            file_a_contents[mac_b] = {'ip': ip_b, 'name': name_b}

# Write the updated contents back to file A
with open(file_a_path, 'w') as file:
    for mac, details in file_a_contents.items():
        file.write(f"{details['ip']},{mac},{details['name']}\n")