############# IMPORTANT ############

run.sh will run the exploit, run the grep "pickout", and the report maker with all its proper arguments



you will need to take care of running libre in the background beforehand and closing it after the report is made  
its command is below that I use, paul's might be similar

libreoffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nofirststartwizard --nologo --headless


In the createreport.py file

Lines ~20+ have some variables that you should change to bring it into the program.
So change the locations of the templates and reports to whatever consolidated location makes it 
most convienient for you



ISSUES:
################################ UNO #################################

if the uno package is a problem. run "pip uninstall uno" when you
installed it, it was not the uno package for libre, but another unrelated
one. Get rid of it and it should work but if not keep reading


if you get problems running UNO talking about "base" or shit like that,
OR the python section of my code doesn't run because it can't find the
python path im using:

change the run.sh script to use "/path/to/libreoffice/python createreport.py
instead of what it had currently as that'd be the path for the python
that comes with my LibreOffice installion and might differ from yours 

######################################################################

D
