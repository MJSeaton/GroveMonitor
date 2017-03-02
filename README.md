# GroveMonitor
Simple control software written in Python designed to log data from a sensor array incorporating Atlas Scientific probes and an Arduino. Writes to CSV and emails a specified account using a gmail account if Networking is enabled. 

##

Usage: No input- variables in code define loop lenth. 

networking - Boolean - defines whether or not emails are sent from the script.


loopNumber - An int that controls the number of loop iterations before a flush or Control prompt is triggered.


numSensors - Allows for different sensor arrays with differing numbers of inputs to be interact with this script.

continuousMode - Boolean - defines whether or not the code is in continuous mode, in which it will run indefinitely on a fixed update   schedule. If False, the user will be periodically prompted for input to save, change mode, or quite the program.
