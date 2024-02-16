
import uno
import unohelper
import glob
import os
from datetime import datetime


def extract_and_sort_vulnerabilities(lines):
    vulnerabilities = []
    for i in range(0, len(lines), 5):
        if lines[i].startswith('CVE-'):
            cve = lines[i].strip()
            try:
                cvss_score_str = lines[i + 2].split(':')[1].strip()
                cvss_score = float(cvss_score_str)
            except ValueError:
                print(f"Error converting CVSS score to float: {lines[i + 2]}")
                continue
            url = lines[i + 3].split(':', 1)[1].strip()
            vulnerabilities.append({'cve': cve, 'cvss_score': cvss_score, 'url': url})

    vulnerabilities.sort(key=lambda x: x['cvss_score'], reverse=True)
    return vulnerabilities


def read_cve_descriptions(description_file_path):
    cve_descriptions = {}
    try:
        with open(description_file_path, "r") as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(' ', 1)
                    if len(parts) == 2:
                        cve, description = parts
                        cve_descriptions[cve] = description
    except IOError:
        print(f"Error: Unable to read file {description_file_path}")
        return {}
    return cve_descriptions


def insert_into_bookmark(doc, bookmark_name, text):
    try:
        bookmarks = doc.getBookmarks()
        if bookmarks.hasByName(bookmark_name):
            bookmark = bookmarks.getByName(bookmark_name)
            text_range = bookmark.getAnchor()
            text_range.setString(text)
            print(f"Inserted '{text}' into bookmark '{bookmark_name}'.")
        else:
            print(f"Bookmark '{bookmark_name}' not found.")
    except Exception as e:
        print(f"Error while inserting into bookmark '{bookmark_name}': {e}")

    except Exception as e:
        print(f"Error: Unable to insert into bookmark {bookmark_name}. {e}")

def categorize_by_severity(cvss_score):
    if cvss_score >= 9.0:
        return 'Critical'
    elif cvss_score >= 7.0:
        return 'High'
    elif cvss_score >= 4.0:
        return 'Medium'
    else:
        return 'Low'

def main():
    directory = "/home/kali"
    cve_description_file_path = "/home/kali/cve_description.txt"
    cve_descriptions = read_cve_descriptions(cve_description_file_path)

    files = glob.glob(os.path.join(directory, "nmap_results_*.txt"))
    latest_file = max(files, key=os.path.getctime) if files else None

    if latest_file:
        try:
            local_context = uno.getComponentContext()
            resolver = local_context.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", local_context)
            smgr = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ServiceManager")
            remote_context = smgr.getPropertyValue("DefaultContext")
            desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", remote_context)

            doc = desktop.loadComponentFromURL("file:///home/kali/Documents/test.odt", "_blank", 0, ())

            with open(latest_file, "r") as file:
                lines = file.readlines()
            sorted_vulnerabilities = extract_and_sort_vulnerabilities(lines)

            for i, vulnerability in enumerate(sorted_vulnerabilities):
                cve = vulnerability['cve']
                if cve in cve_descriptions:
                    insert_into_bookmark(doc, f"CVE{i+1}", cve)

                    print(f"Inserting description for {cve}")
                    insert_into_bookmark(doc, f"CVE_Desc_{i+1}", cve_descriptions[cve])
                else:

                    print(f"Description for {cve} not found.")


            total_cves = len(set(v['cve'] for v in sorted_vulnerabilities))
            severity_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
            for vulnerability in sorted_vulnerabilities:
                category = categorize_by_severity(vulnerability['cvss_score'])
                severity_counts[category] += 1


            insert_into_bookmark(doc, "Total_CVEs", str(total_cves))
            for severity, count in severity_counts.items():
                insert_into_bookmark(doc, f"{severity}_Vulnerabilities", str(count))




            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"document_{current_time}.odt"
            new_file_path = "file:///home/kali/Documents/" + new_file_name
            doc.storeAsURL(new_file_path, ())
            doc.dispose()
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No nmap results files found.")


if __name__ == "__main__":
    main()
