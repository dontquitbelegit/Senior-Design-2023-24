make sure to run as root because sudo is needed for the OS scan.
Might work without it idk

similar rules apply like the first demo with the whole libre office command for report generation
libreoffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nofirststartwizard --nologo --headless

createreport is also layed out in the same manner so if you'd like to change template or report names and file paths do so

I use pickout and pickout2 bash scripts to filter twice the infromation I'd like to put in the final report, 
as pickout2 can also add some nice info for the user in the report and I didnt want pickout.sh to be too large in case 
edits to reporting text was needed. It also made testing and development easier when its in small consecutive chuncks 
with each doing a different task as run.sh will string them all together anyway for the GUI and pass the IP into nmapsearch.sh
