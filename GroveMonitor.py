import serial
import time
import datetime
import smtplib
import csv





Networking=False
pollingInterval = 1 #polling interval in seconds

def main():
    if Networking==True:
        #signs into gmail for SMTP purposes
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()    
        server.login("****@gmail.com", "****") #To Do: Parameterize login credentials
        message="\n Full Diagnostics dump from sensor data:\n"
    
    firstBlocked=False #ORP probe is outputting before everything else so to format data correctly, the first serial read should be ignored.    
    port = serial.Serial("COM5",38400,timeout=None) #initialize serial port and variables related to recording data into CSV
    count=0
    loopNumber=200  
    numSensors=6
    continuousMode=True
    
    
    dataHandle = open('SensorData.csv', mode='a+') #open a handle to the csv data will be written to and initialize writer
    dataWriter = csv.writer(dataHandle)
    data=['']
    
    while (True): #Data read loop from sensor array (via serial port). Sequentially reads in from the 
        data[0]=str(datetime.datetime.now())
        while (count < loopNumber):
            count+=1
            lineRead=port.readline()
            print lineRead
            if firstBlocked == False:
                firstBlocked = True
            else:
                data.append(lineRead)
                if len(data)==numSensors+1:
                    for entry in xrange(0,len(data)):
                        data[entry]=data[entry].replace("\r\n"," ")                
                    dataWriter.writerow(data)
                    data=[]
                    data.append(str(datetime.datetime.now()))
            time.sleep(pollingInterval)
        
        if continuousMode: #In continuous mode, the program will constantly Reopen the data handle in order to commit changes to the document, otherwise it will prompt the user for a command statement.
            if(count ==loopNumber):
                dataHandle.close()
                count=0
                if Networking ==True:
                    with open('SensorData.csv') as dat:
                        lines = dat.readlines()
                    
                    for entry in lines:
                        message+=entry
                    server.sendmail("****s@gmail.com", "****@gmail.com", message)
                    message = "\n Full Diagnostics dump from sensor data:\n"
                dataHandle=open('SensorData.csv', mode='a+')
                dataWriter = csv.writer(dataHandle)
                
                
        else:
            cmndString = raw_input("Please enter a command type: ")
            if (cmndString=="drakon"):
                
                drakonString = raw_input("Please enter a drakon command: ")            
                if (drakonString== "quit"): 
                    raise SystemExit(0)
                elif (drakonString=="continuous"):
                    continuousMode=True
                
                elif (drakonString=="cancel"):
                    cancelled=True
                elif (drakonString =="save"):
                    dataHandle.close()
                    saveInput=raw_input("Type continue to reopen the data handle: ")
                    if (saveInput=="continue" or saveInput== "Continue"):
                        dataHandle=open('SensorData.csv', mode= 'a+')
                        dataWriter = csv.writer(dataHandle)
                        
                    else:
                        raise SystemExit(0)
                    count=0
            else:    
                port.write(cmndString)        
                count=0;
            
if __name__ == "__main__":
    main()