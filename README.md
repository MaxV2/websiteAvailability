# Website availability & performance monitoring
Coding assignment.

## How to launch the console program

1. Install the libraries if needed (os, time, requests, numpy, collections)
1. Run the programm from your console

## How to use the program

You can delete the initial URL list.

You can add new URLs to the list (starting with http:// or https://), with their corresponding 'check interval' in seconds (enter an int that is >= 1).

You can then start monitoring the list.

## How it works

If you set the 'check interval' of a URL to 3 seconds, then the program will test the URL about every 3 seconds. There may be a little delay of a few tenth of second, since the program cannot multithread and cannot test two URLs at once.

For each URL on the list:
* 'Last check time' is the time and date of the last test performed on the URL
* 'Check interval' is the number of seconds between the last two tests of the URL (should be quite close to what the user instructed, depending on the response time of the other websites).
* 'Status code' is the last http status code returned by the website (see https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)
* 'Availability 2min' is the proportion of '200 response code' (ie 'OK response code') among all the tests performed in the last 2min before the 'Last check time'.
* 'Availability 10min' is the same, for the last 10min.
* 'Availability 1hour' is the same, for the last hour.
* 'Response time avrg' is the average response time of all the test performed in the time interval.
* 'Response time max' is the maximum response time of all the test performed in the time interval.

## Warnings
* If for example the program has been running for only 5min, then for instance 'Availability 10min' and 'Availability 1hour' will be equal.
* If you have entered more than three URLs on the main menu, then the data on the console might not fit your screen.
* If there is a response code that isn't 200 in the last 10 min then the response time is considered infinite, and 'Response time 10min avrg' will also be infinite.


## How to test the program

One way to test the alert system is to use http://www.stackoverflow.com as an URL, and to set a 'check interval' of one second. After about two minutes, the website will temporarily block your IP adress, resulting with a 'Website is down' alert.

You can also use one of your own website and manually put it online and offline to test the program.
