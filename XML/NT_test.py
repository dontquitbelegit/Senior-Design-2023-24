import shutil
from xml.etree import ElementTree
from datetime import datetime
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
import subprocess


def duplicate_template(template_path, new_document_path):
    shutil.copy2(template_path, new_document_path)


def count_packets_with_tshark(pcap_file):
    try:
        # Building the command as a string to be run in the shell
        command = f"tshark -r '{pcap_file}' -T fields -e frame.number | wc -l"

        # Executing the command
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)

        # Returning the output as an integer
        return str(int(result.stdout.strip()))  # Strip to remove any extra newlines or spaces
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None  # Return None or an appropriate error value
    except ValueError:
        print("Could not convert output to integer")
        return None  # Return None or an appropriate error value


def parse_xml_data(xml_file_path, element_structure):
    tree = ElementTree.parse(xml_file_path)
    root = tree.getroot()
    data = []
    for entry in root.findall(element_structure['path']):
        data_item = {}
        for key, value in element_structure['elements'].items():
            element = entry.find(value)
            data_item[key] = element.text if element is not None else 'N/A'  # Using 'N/A' for missing elements
        data.append(data_item)
    return data


def insert_data_into_table(odt_path, xml_data, xml_type):
    doc = load(odt_path)
    inserted_bookmarks = []

    all_bookmarks = [node.data for table in doc.getElementsByType(Table) for row in table.getElementsByType(TableRow)
                     for cell in row.getElementsByType(TableCell) for p_element in cell.getElementsByType(P) for node in
                     p_element.childNodes if node.nodeType == node.TEXT_NODE]
    print("Available bookmarks in the document:", set(all_bookmarks))  # Debug: List all bookmarks found

    # Loop through all table cells in the document
    for table in doc.getElementsByType(Table):
        for row in table.getElementsByType(TableRow):
            for cell in row.getElementsByType(TableCell):
                for p_element in cell.getElementsByType(P):
                    text_nodes = [node.data for node in p_element.childNodes if node.nodeType == node.TEXT_NODE]
                    # Determine which XML data type we are working with and insert appropriately
                    for data_item in xml_data:
                        if xml_type == 'dns_total':
                            if 'DNS Matches' in text_nodes:
                                new_text = data_item['Matches']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('DNS Matches')
                        elif xml_type == 'http_total':
                            if 'HTTP Matches' in text_nodes:
                                new_text = data_item['Matches']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('HTTP Matches')
                        elif xml_type == 'top_ips':
                            if 'IPs' in text_nodes:
                                new_text = data_item['Address']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('Address')
                            if 'Data' in text_nodes:
                                new_text = '-' + data_item['DataBytes']
                                new_p = P(text=new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('DataBytes')
                        elif xml_type == 'unusual_protocols':
                            if 'Protocol' in text_nodes:
                                new_text = data_item['Protocol']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('Protocol')
                            if 'Source Port' in text_nodes:
                                new_text = data_item['SourcePort']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('Source Port')
                            if 'Destination Port' in text_nodes:
                                new_text = data_item['DestinationPort']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('Destination Port')
                            if 'Packets' in text_nodes:
                                new_text = data_item['Packets']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('Packets')
                        elif xml_type == 'failed_connections':
                            if 'IP' in text_nodes:
                                new_text = data_item['IP']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('IP')
                            if 'Reset Count' in text_nodes:
                                new_text = data_item['ResetCount']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('Reset Count')
                        elif xml_type == 'suspicious_payloads':
                            if 'Source IP' in text_nodes:
                                new_text = data_item['SourceIP']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('Source IP')
                            if 'Destination IP' in text_nodes:
                                new_text = data_item['DestinationIP']
                                new_p = P(text=new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('Destination IP')
                            if 'Payload' in text_nodes:
                                new_text = data_item['Payload']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('Payload')
                        elif xml_type == 'arp_traffic':
                            if 'MAC Address' in text_nodes:
                                new_text = data_item['MAC']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('MAC Address')
                            if 'IP' in text_nodes and 'IP' not in inserted_bookmarks:  # Avoiding duplication with fc
                                new_text = data_item['IP']
                                new_p = P(text=new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('IP')
                            if 'Count' in text_nodes:
                                new_text = data_item['Count']
                                new_p = P(text='-' + new_text)
                                cell.addElement(new_p)
                                inserted_bookmarks.append('Count')

    doc.save(odt_path)
    return inserted_bookmarks


def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()


def replace_placeholder_in_odt(odt_path, placeholder, replacement_string):
    doc = load(odt_path)
    found_and_replaced = False

    for p_element in doc.getElementsByType(P):
        # Extracting text from P element
        current_text = ''.join(node.data for node in p_element.childNodes if node.nodeType == node.TEXT_NODE)
        if placeholder in current_text:
            new_text = current_text.replace(placeholder, replacement_string)
            # Clear the paragraph and set new text
            for node in p_element.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    node.data = new_text  # Directly modify the text data of the node
            found_and_replaced = True

    if found_and_replaced:
        doc.save(odt_path)
    return found_and_replaced


def main():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y%m%d_%H%M%S')
    template_path = '/Users/morgansinan/Desktop/NetworkTraffic_Template.odt'
    new_document_path = f'/Users/morgansinan/Desktop/Updated_NetworkTraffic_Report_{formatted_datetime}.odt'
    pcap_file_path = '/Users/morgansinan/Desktop/XML/captured_traffic.pcapng'
    duplicate_template(template_path, new_document_path)

    # Dictionary to map XML types to files and their structure for parsing
    xml_files = {
        'top_ips': ('/Users/morgansinan/Desktop/XML/top_ips.xml', './IP',
                    {'Address': 'Address', 'DataBytes': 'DataBytes'}),
        'unusual_protocols': ('/Users/morgansinan/Desktop/XML/unusual_protocols.xml', './ProtocolEntry',
                              {'Protocol': 'Protocol', 'SourcePort': 'SourcePort', 'DestinationPort': 'DestinationPort', 'Packets': 'Packets'}),
        'failed_connections': ('/Users/morgansinan/Desktop/XML/failed_connections.xml', './Connection',
                               {'IP': 'IP', 'ResetCount': 'ResetCount'}),
        'suspicious_payloads': ('/Users/morgansinan/Desktop/XML/suspicious_payloads.xml', './Payload',
                                {'SourceIP': 'SourceIP', 'DestinationIP': 'DestinationIP', 'Payload': 'Payload'}),
        'arp_traffic': ('/Users/morgansinan/Desktop/XML/arp_traffic.xml', './ARPEntry',
                        {'MAC': 'MAC', 'IP': 'IP', 'Count': 'Count'}),
        'dns_total': ('/Users/morgansinan/Desktop/XML/dns_total.xml', './DNSQueries',
                      {'Total': 'Total', 'Matches': 'Matches'}),
        'http_total': ('/Users/morgansinan/Desktop/XML/http_total.xml', './HTTPQueries',
                       {'Total': 'Total', 'Matches': 'Matches'})
    }

    packet_count = count_packets_with_tshark(pcap_file_path)
    replace_placeholder_in_odt(new_document_path, 'TotalPackets', packet_count)

    # Placeholder and file mappings
    placeholders_files = {
        'DNSQ': '/Users/morgansinan/Desktop/XML/dns_total.txt',
        'HTTPQ': '/Users/morgansinan/Desktop/XML/http_total.txt',
    }

    # Replace each placeholder with content from its corresponding file
    for placeholder, file_path in placeholders_files.items():
        replacement_string = read_text_from_file(file_path)
        if replace_placeholder_in_odt(new_document_path, placeholder, replacement_string):
            print(f"Placeholder '{placeholder}' has been replaced in the document.")
        else:
            print(f"No instances of '{placeholder}' found in the document.")

    # Iterate over each XML file and corresponding data structure
    for xml_type, (xml_path, element_path, elements) in xml_files.items():
        xml_data = parse_xml_data(xml_path, {'path': element_path, 'elements': elements})
        inserted_bookmarks = insert_data_into_table(new_document_path, xml_data, xml_type)
        print(f"Data from '{xml_type}' inserted into bookmarks: {inserted_bookmarks}")

    print(f"ODT document has been updated and saved as {new_document_path}")


if __name__ == "__main__":
    main()
