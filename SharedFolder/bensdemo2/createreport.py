import uno
from com.sun.star.connection import NoConnectException
from com.sun.star.uno import Exception as UnoException
from com.sun.star.io import IOException
from datetime import datetime

def insert_text_at_bookmark(doc, bookmark_name, text, textcolor):
    """Insert text at the specified bookmark in the document."""
    bookmarks = doc.getBookmarks()
    bookmark = bookmarks.getByName(bookmark_name)
    text_range = bookmark.getAnchor()
    cursor = text_range.getText().createTextCursorByRange(text_range)
    cursor.setPropertyValue("CharColor", textcolor)  # Set the text color to blue
    cursor.setString(text)

def main():

#########FOR INTEGRATION################

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    templateLocation = "file:///home/kali/Desktop/bensdemo2/Template.odt"
    reportLocation = f"file:///home/kali/Desktop/bensdemo2/Reports/Report_{timestamp}.odt"
    
#########################


    # Connect to the running LibreOffice instance
    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local_context)
    try:
        context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    except NoConnectException:
        print("Failed to connect to LibreOffice. Make sure it's running in listening mode.")
        return
    
    # Access the document
    desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
    doc = desktop.loadComponentFromURL(templateLocation, "_blank", 0, ())
    
    # Load the text from the telnet_sessions_output.txt file
    output_file_path = "./pickout_text2.txt"
    with open(output_file_path, 'r') as file:
        telnet_output = file.read()
        
    #Split the file contents into an array seperated by dollar signs
    telnet_output_array = telnet_output.split("$")  
        
    
    # Insert the "grade" bookmark
    
    if (telnet_output_array[0][7]=="a"):
        insert_text_at_bookmark(doc, "Grade", "Complete", 0x00FF00)
    else:
        insert_text_at_bookmark(doc, "Grade", "Incomplete", 0xFF0000)
    
    insert_text_at_bookmark(doc, "IP", telnet_output_array[0], 0x000000)
    
    insert_text_at_bookmark(doc, "OS", telnet_output_array[1], 0x000000)
    
    insert_text_at_bookmark(doc, "Hostname", telnet_output_array[2], 0x000000)
    
    insert_text_at_bookmark(doc, "Ports", telnet_output_array[3], 0x000000)
    # Save the document (optional, you can also manually save it in LibreOffice)

    new_file_path = reportLocation
    try:
        doc.storeAsURL(new_file_path, ())
        print(f"Document saved as {new_file_path}")
    except IOException as e:
        print(f"Failed to save document: {e.Message}")
    finally:
        doc.close(True)


if __name__ == "__main__":
    main()
