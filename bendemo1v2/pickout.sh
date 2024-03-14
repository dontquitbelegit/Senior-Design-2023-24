#!/bin/bash

# Define the output log file
output_file="telnet_sessions_output.txt"

# Check for successful connection to port 21
if grep -q "vsFTPd" $output_file; then
    echo "1. Step 1 Passed - First telnet connection to port 21 was successful. A fake username with a :) and password were inputted and the connection was aborted after confirming that a login attempt was made."
else
    echo "1. Inconclusive Step 1 Failed - First telnet connection to port 21 failed. This means that the following connections will not work and the attack has failed. However, the fact that this first connection did not work should signify that the Server is not working as intended. Please check if the machine is off, if FTP is running, or if a firewall is blocking access."
fi

echo "$"

# Check for successful connection to port 6200
if grep -q "6200" $output_file; then
    echo "2. Step 2 Passed - Second telnet connection to port 6200 was successful. The machine is likely vulnerable to this attack as an open connection on this port should normally not happen. However, if another, different, service is running on this port that made the connection, then step 3 will fail."
else
    echo "2. Secure Step 2 Failed - Second telnet connection to port 6200 failed. If the first connection succeeded, but then this one did not, congratulations! The machine is secure against this attack, meaning that either an update has patched this vulnerability or that its otherwise incompatible. The 3rd step will always fail, and if it shows as succeeded, please disregard it and/or send in a bug report!"
fi

echo "$"

# Check if the "id;" command returns you as root
if grep -q "uid=0(root) gid=0(root)" $output_file; then
    echo "3. Step 3 Passed - The 'id;' telnet command returns the user as root. This means that the computer is in imminent danger as the test has fully succeeded and the computer lies open to attack. Please immediately restart the computer to close the open backdoor, update your FTP version, and rerun this command to verify that it has been patched"
else
    echo "3. Secure Step 2 Failed - The 'id;' telnet command did not return the user as root. The attack has failed. It is likely that steps 1 or 2 have also failed. In the event that they both passed, this step should not be showing. If steps 1 and 2 did succeed, and this did not, please update your system regardless just in case or check your firewall rules."
fi
