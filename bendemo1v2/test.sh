#!/usr/bin/expect -f

# Define the output file
set output_file "telnet_sessions_output.txt"

set file [open $output_file "w"]
close $file

# Open file for writing
#set file [open $output_file "w"]
log_file -a $output_file

# First telnet session
spawn telnet 10.0.2.4 21
expect ")"
send "user CATSbackdoorvsftptest:)\r"
expect "password."
send "pass CATSpasstest\r"
sleep 3
#expect "ftp>"
send "\035\r"  ;# ASCII code for '^]'
sleep 3
#expect "telnet>"
send "quit\r"
expect eof

# Capture output of first session
#set output $expect_out(buffer)
#puts $file $output

# Wait for 5 seconds
sleep 5

# Second telnet session
spawn telnet 10.0.2.4 6200
expect "login:"
send "id;\r"
expect eof

# Capture output of second session
#set output $expect_out(buffer)
#puts $file $output

# Close the file
#close $file
