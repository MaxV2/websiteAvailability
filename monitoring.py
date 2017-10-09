#!/usr/bin/env python

import os      #for clearing the screen 
import time    #for getting the current time and sleeping some time
import requests    #for getting the websites' data
import numpy    #for computing lists max and averages
from collections import deque     #for using efficient queues of data (first in first out)


# Console program to monitor performance and availability of websites
# Websites and check intervals are user defined
# Users can keep the console app running and monitor the websites


### FUNCTIONS ###


def launch_main_menu(): #displays the main menu, the entrance point of the program

    #Initialize dataList with arbitrary example websites:
    dataList=[{
        'URL':                 'http://www.example.com',
        'updateInterval':      2,
        'lastUpdateInterval':  float('inf'),
        'statusCode':          deque([]),
        'responseTime':        deque([]),
        'checkTime':           deque([]),
        'alerts':              []
        },{
        'URL':                 'http://www.stackoverflow.com',
        'updateInterval':      1,
        'lastUpdateInterval':  float('inf'),
        'statusCode':          deque([]),
        'responseTime':        deque([]),
        'checkTime':           deque([]),
        'alerts':              []
        },{
        'URL':                 'https://www.google.com/404',
        'updateInterval':      3,
        'lastUpdateInterval':  float('inf'),
        'statusCode':          deque([]),
        'responseTime':        deque([]),
        'checkTime':           deque([]),
        'alerts':              []
        }]
        
    
    display_title_bar()     #display the program name
    show_URL_list(dataList) #display the existing list of URL
    
    choice = ''
    while choice != '4':    
        choice = get_user_choice()
        
        #Update the screen
        display_title_bar()
        show_URL_list(dataList)
        if choice == '1':        #'Add an URL to the list'
            get_new_URL(dataList)
        elif choice == '2':      #'Clear the list'
            #URLs=[]
            dataList=[]
            display_title_bar()
            show_URL_list(dataList)
        elif choice =='3':       #'Start monitoring the list'
            start_monitoring(dataList)
        elif choice == '4':      #'Quit'
            os.system('cls')
            print("\nThanks for using the Website Availability app.")
        else:
            print("\nPlease enter a number corresponding to those possibilities:\n")




def get_user_choice():   # Displays the main menu and asks for the user choice.
    print("\n[1] Add an URL to the list")
    print("[2] Clear the list")
    print("[3] Start monitoring the list")
    print("[4] Quit")
    return input("What would you like to do? ")




def display_title_bar():  # Clears the terminal screen, and displays a title bar.
    os.system('cls')
    print("\t*******************************************************")
    print("\t***  Website availability & performance monitoring  ***")
    print("\t*******************************************************")





def show_URL_list(dataList):   # Shows the URLs which are already in the URL list.
    print("\nList of URLs to monitor:")
    for data in dataList:
        print("* " + data['URL'] + '      (Check interval:'    + str(data['updateInterval'])  +  's)'  )
    if len(dataList)==0:
        print("{list is empty}")



 
def get_new_URL(dataList):     # Asks the user for a new URL and update interval.

    new_URL = input("\nType in the full URL (eg. http://www.stackoverflow.com)  >")
    #Check if the URL looks valid.
    if not (    new_URL.startswith('http://') or new_URL.startswith('https://')    ):
        print("\nThis URL is not valid. Please start with http:// or https://\n")
        return
    
    check_interval = input("Type in the check interval in seconds for this URL (integer) >")
    if not check_interval.isdigit():
        print("\nPlease type in an integer\n")
        return
    elif int(check_interval) < 1:
        print("\nThe interval has to be at least 1s\n")
        return
        
    #Add the new URL to the dataList.
    dataList.append({
        'URL':                 new_URL,               #The URL (string).
        'updateInterval':      int(check_interval),   #The user-defined time interval between 2 tests in seconds. (int)
        'lastUpdateInterval':  float('inf'),          #The last time interval. Needs to be as close as possible to updateInterval. (float)
        'statusCode':          deque([]),             #The queue of the last status codes from the last tests. (dequeue([int]))
        'responseTime':        deque([]),             #The queue of the last response time from the last tests. (dequeue([float]))
        'checkTime':           deque([]),             #The queue of the exact time of each last tests. (dequeue([float]))
        'alerts':              []                     #The list of all the alerts. ([[  boolean 'is the website up?' , float 'time of alert'], [...] ])
        })
        
    #Clear the screen and display the new URL list.
    display_title_bar()
    show_URL_list(dataList)
    
    


    
def test_website(data):     #Performs the tests on a specific URL. This is the core of the program.
    r = requests.get(data['URL'])
    
    statusCode=r.status_code
    if statusCode==200:   #if status is 'OK'
        responseTime=r.elapsed.total_seconds()
    else:
        responseTime=float('inf')    #Response time is considered infinite.

    data['statusCode'].append(statusCode)
    data['responseTime'].append(responseTime)
    
    if len(data['statusCode'])> 3600/data['updateInterval']:    #if the data queues contain more that 1hour worth of data, clear the oldest value
        data['statusCode'].popleft()
        data['responseTime'].popleft()
        data['checkTime'].popleft()





def update_monitoring_screen(dataList):   #Computes the stats, then updates the console screen with the last data.
    #clear the screen and display title.
    display_title_bar()
    
    #display the data for each URL
    for data in dataList:
        
        if len(data['checkTime'])>0:   # 'If there has been at least one test on the URl'
            
            statusCode=data['statusCode'][-1]   #get the last status code
            elementsNb=len(data['checkTime'])   #get the number of data values ('checkTime', 'statusCode' and 'responseTime' each have the same length)
            checkTime=time.asctime( time.localtime(data['checkTime'][-1]) ) #time of the last test written in a user-readable way
            
            #Let's calculate rank10min, which is the number of values measured in the last 600 seconds:
            rank10min= int( 600/data['updateInterval'] +1 )
            if rank10min > elementsNb:
                rank10min = elementsNb
                
            #Let's calculate rank2min, which is the number of values measured in the last 120 seconds:
            rank2min= int( 120/data['updateInterval'] +1 )
            if rank2min > elementsNb:
                rank2min = elementsNb
            
            #Count the percentage of 200s ('statusOK') in the last 2min:
            availability2min= list(data['statusCode']) [ elementsNb - rank2min:   ].count(200)  / rank2min *100
            
            #Count the percentage of 200s in the last 10min:
            availability10min= list(data['statusCode']) [ elementsNb - rank10min:   ].count(200)  / rank10min *100
            
            #Count the percentage of 200s in the whole list (last 1 hour):
            availability1hour=data['statusCode'].count(200)      / elementsNb *100      
            
            #Let's compute the response time stats:
            responseTime=data['responseTime'][-1]  #last response time
            responseTime10minAvg = round(numpy.average(list(data['responseTime'])[elementsNb - rank10min:]),6) #Average the last 10min worth of data.
            responseTime1hourAvg = round(numpy.average(data['responseTime']),6)                                #Average the last hour, ie. the whole list
            responseTime10minMax = round(numpy.max(list(data['responseTime'])[elementsNb -rank10min:]),6)      #Get the max of the last 10 min
            responseTime1hourMax = round(numpy.max(data['responseTime']),6)                                    #Get the max of the last hour
            
            #Create alerts if needed:
            if availability2min<80 and (len(data['alerts'])==0 or data['alerts'][-1][0]==True):              #If wesbite is down AND last alert was positive or null
                data['alerts'].append([False, data['checkTime'][-1]])                                           #Website is down alert
            elif availability2min>80 and (len(data['alerts'])!=0 and data['alerts'][-1][0]==False):          #If website is up AND last alert was a negative one
                data['alerts'].append([True, data['checkTime'][-1]])                                            #Website is up alert
            
        else:   # 'If there has not been any test on the URl yet'
            statusCode='NA'
            availability10min='NA'
            availability2min='NA'
            availability1hour='NA'
            checkTime='NA'
            responseTime='NA'
            responseTime10minAvg = 'NA'
            responseTime1hourAvg = 'NA'
            responseTime10minMax = 'NA'
            responseTime1hourMax = 'NA'
            
            
        #Print the data
        print ('  ___________________________________________________________________________')
        print (' |')
        print (' | URL:                    '+str(data['URL']))
        print (' | Last check time:        '+str(checkTime))
        print (' | Check interval:         '+str(round(data['lastUpdateInterval'],3))   + ' s')
        print (' | Status code:            '+str(statusCode) )
        print (' | Availability    2min:   '+str(availability2min)  + '%')
        print (' |                10min:   '+str(availability10min)  + '%')
        print (' |                1hour:   '+str(availability1hour)  + '%')
        print (' | Response time:          '+str(responseTime)           + ' s')
        print (' |           10min avrg:   '+str(responseTime10minAvg)   + ' s')
        print (' |           1hour avrg:   '+str(responseTime1hourAvg)   + ' s')
        print (' |           10min  max:   '+str(responseTime10minMax)   + ' s')
        print (' |           1hour  max:   '+str(responseTime1hourMax)   + ' s')
        
        #Print the alerts if any
        if len(data['alerts'])!= 0:
            print('')
            for alert in data['alerts']:
                if alert[0]==False:   #False means website is down, True means it's up.
                    print(' |  /!\ /!\ WEBSITE IS DOWN /!\ /!\  Availability below 80%.  (' + time.asctime( time.localtime(alert[1]) ) + ')')
                else:
                    print(' |          Availability resumed.                             (' + time.asctime( time.localtime(alert[1]) ) + ')')
        
        print(' |___________________________________________________________________________')




def start_monitoring(dataList):   #Main loop of the monitoring part of the program

    timeToNextUpdate=[-1]*len(dataList)    #contains the time (float) remaining before next test has to be performed on each URL
    lastUpdateTime=[-1]*len(dataList)      #contains the time (float) of last test on each URL

    
    while True:   #Never stops. Program has to be ended by closing the console.

        for i in range(len(dataList)):  #For each URL
        
            if timeToNextUpdate[i]<0: # "if URL i needs to be updated"
                testTime=time.time()  # Remember current time
                dataList[i]['checkTime'].append(testTime)   #Add current time to the end of the 'checkTime' list of this URL
               
            
                test_website(dataList[i])   #Test the URL. This is the main part of the program.
                
                if lastUpdateTime[i] != -1:                                                 #'if this is not the first test to the URL'
                    dataList[i]['lastUpdateInterval']=testTime-lastUpdateTime[i]            #remember time interval since last test
                
                lastUpdateTime[i]=testTime                                                  #update the time of the test that just happened
                
                update_monitoring_screen(dataList)                                          #update the console screen with the new data

        
        #compute the time left before each next update, and calculate the minimum of these values
        for i in range(len(timeToNextUpdate)):
            timeToNextUpdate[i]=dataList[i]['updateInterval']-(time.time()-lastUpdateTime[i])
        sleepTime=min(timeToNextUpdate)
        
        #sleep for a while if nothing has to be done now
        if sleepTime>0:
            time.sleep(sleepTime)






### MAIN PROGRAM ###
launch_main_menu()   #Start the program.

