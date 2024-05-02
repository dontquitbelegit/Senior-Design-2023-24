#!/usr/bin/env python3

from xml.etree import ElementTree
from datetime import datetime
import shutil

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P


def duplicate_template(template_path, new_document_path):
    # Copy the template document to create a new document
    shutil.copy2(template_path, new_document_path)


def parse_mac_and_ips_from_xml(mac_file_path):
    """
    Parses MAC addresses and IPs from the XML file at the given path,
    formatting MAC addresses to match the "manuf_cleaned.txt" style.

    Parameters:
    - xml_file_path (str): The file path to the XML data.

    Returns:
    - List[Dict[str, str]]: A list of dictionaries, each containing 'ip' and 'mac' keys with their respective values.
    """
    # Load and parse the XML file
    tree = ElementTree.parse(mac_file_path)
    root = tree.getroot()

    # Initialize a list to hold the extracted data
    extracted_data = []

    # Iterate through the XML tree to find and extract MAC addresses and IPs
    for host in root.findall('host'):
        # Initialize a dictionary to store data for the current host
        host_data = {}

        # Extract IP address if available, removing parentheses
        ip_element = host.find("ip")
        if ip_element is not None:
            host_data['ip'] = ip_element.text.strip('()')

        # Extract MAC address if available
        mac_element = host.find("mac")
        if mac_element is not None:
            # Format the MAC address to match the "manuf_cleaned.txt" style
            mac_formatted = mac_element.text.lower().replace(':', '')[:6]
            host_data['mac'] = mac_formatted

        # Extract Host name if available
        hostname_element = host.find("hostname")
        if hostname_element is not None:
            host_data['hostname'] = hostname_element.text

        # Extract Services if available
        service_element = host.find("services")
        if service_element is not None:
            host_data['services'] = service_element.text

        # Extract FULL MAC if available
        fullmac_element = host.find("fullmac")
        if fullmac_element is not None:
            host_data['fullmac'] = fullmac_element.text

        # Add the host data to the list if both IP and MAC were found
        if host_data:
            extracted_data.append(host_data)

    return extracted_data


def load_vendor_mapping(vendor_file_path):
    vendor_mapping = {}
    with open(vendor_file_path, 'r') as file:
        for line in file:
            # Split each line by tabs or spaces
            parts = line.split()  # Using split() without an argument to handle any whitespace
            if len(parts) >= 2:
                # The MAC prefix is the first part, vendor name is the remaining parts joined
                mac_prefix, vendor_name = parts[0], " ".join(parts[1:])
                vendor_mapping[mac_prefix.lower()] = vendor_name.strip()
    return vendor_mapping


def find_vendor_by_mac(mac_address, vendor_mapping):
    mac_prefix = mac_address.lower()[:6]
    return vendor_mapping.get(mac_prefix, "Unknown")


def add_vendor_info_to_data(extracted_data, vendor_mapping):
    for data in extracted_data:
        mac_address = data['mac']
        vendor_name = find_vendor_by_mac(mac_address, vendor_mapping)
        data['vendor'] = vendor_name
    return extracted_data


def count_lines_in_xml(mac_file_path):
    with open(mac_file_path, 'r') as file:
        lines = file.readlines()
        return len(lines)


def format_data_for_table(extracted_data):
    """
    Formats the extracted data for insertion into a table. Each item in the returned list
    represents a row, with dictionary keys matching the column headings or identifiers.
    """
    table_data = []
    for item in extracted_data:

        service_count = int(item.get('services', '0'))
        if service_count >= 3:
            services_text = f"Y : {item.get('services', '')}"
        else:
            services_text = f"N : {item.get('services', '')}"

        # Create a dictionary for each row, matching keys to your column identifiers
        row_data = {
            'IP': item.get('ip', ''),
            'MAC': item.get('mac', ''),
            'VENDOR': item.get('vendor', ''),
            'NAME': item.get('hostname', ''),
            'SERVICES': services_text
        }
        table_data.append(row_data)

    # Example for total devices, assuming you just count the entries
    total_devices = {'Total_Devices': len(extracted_data)}
    table_data.append(total_devices)

    return table_data


def insert_data_into_table(odt_path, table_data):
    doc = load(odt_path)
    body = doc.text
    tables = body.getElementsByType(Table)

    if not tables:
        print("No table found in the document.")
        return

    # Assuming the first table is where you want to insert data
    table = tables[1]

    # Assuming the table has a header row already, so we start inserting from the second row
    for data_row in table_data:
        row = TableRow()
        table.addElement(row)
        for key in ['IP', 'MAC', 'VENDOR', 'NAME', 'SERVICES']:
            cell = TableCell()
            row.addElement(cell)
            # Adjust the text to match the data you have; this is a simple direct insertion
            p_element = P(text=data_row.get(key, ''))
            cell.addElement(p_element)

    doc.save(odt_path)


def insert_total_devices_into_table(odt_path, total_devices):
    doc = load(odt_path)
    body = doc.text
    tables = body.getElementsByType(Table)

    # Check if there's at least two tables
    if len(tables) < 2:
        print("Second table for total devices not found in the document.")
        return

    # Target the second table for total devices
    total_devices_table = tables[0]

    # Create a new row for the total devices data
    row = TableRow()
    total_devices_table.addElement(row)

    # Since it's a single column, we add one cell
    cell = TableCell()
    row.addElement(cell)

    # Insert the total devices count
    p_element = P(text=f"Total Devices: {total_devices}")
    cell.addElement(p_element)

    doc.save(odt_path)

def main():
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the current date and time as a string in the format YYYYMMDD_HHMMSS
    formatted_datetime = current_datetime.strftime('%Y%m%d_%H%M%S')
    # filename = f'host_discovery_scan_{formatted_datetime}.xml'

    print(f'Results of Host Discovery Scan can be found in Host_Discovery_{formatted_datetime}.odt')
    # Paths to the XML and vendor files (update these paths as necessary)
    mac_file_path1 = f'/Users/morgansinan/Desktop/host_discovery_scan_temp.xml'
    vendor_file_path = '/Users/morgansinan/Desktop/manuf_cleaned.txt'
    doc_path = '/Users/morgansinan/Desktop/test copy.odt'
    new_doc_path = f'/Users/morgansinan/Desktop/Host_Discovery_{formatted_datetime}.odt'

    # Process the XML and vendor files
    vendor_mapping = load_vendor_mapping(vendor_file_path)
    extracted_data = parse_mac_and_ips_from_xml(mac_file_path1)
    enhanced_data = add_vendor_info_to_data(extracted_data, vendor_mapping)
    line_count = count_lines_in_xml(mac_file_path1) - 3
    total_devices = str(line_count)
    print(total_devices)

    # Duplicate the template file Test.docx
    duplicate_template(doc_path, new_doc_path)

    # Print or use the enhanced data with vendor information
    print(enhanced_data)

    # Format the extracted data for bookmarks and then insert it into the documents table
    table_data = format_data_for_table(enhanced_data)

    insert_data_into_table(new_doc_path, table_data)
    insert_total_devices_into_table(new_doc_path, total_devices)


main()
