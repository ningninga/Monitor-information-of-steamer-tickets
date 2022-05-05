# Monitor-information-of-steamer-tickets
This project used to monitor the information of steamer ticket.

## Table of Contents

- [Background](#background)
- [Flowchart](#flowchart)
- [Use](#use)
- [API](#api)




## Background
Hi, I am going to introduce my situation first, I want to take a plane from Hongkong to other country ( Because flights from Hong Kong are much cheaper than other flights from mainland China). But due to the COVID-19, there is a few ways to go to Hongkong. One of the most available ways is taking a steamer from Shenzhen to Hongkong, most affordable way as well.  

However, the steamer tickets are limited, I heard that many people paid high prices to buy steamer tickets from scalpers last year, just because they were not able to buy tickets on time. Well, the reason why they were not to buy tickets is that the date of ticket release on the ticketing website is not fixed, so they missed the proper time to buy tickets. This year, I want to monitor the information about the tickets to make sure that I can buy a ticket successfully.  

In order to make myself notice the information, I choose two ways to send data, the first one is sending email to my email address, the second one is sending message via Ding (For more details about how to send message by robot via Ding, please see [here](https://github.com/ningninga/flight_discount_info_push))

## Flowchart

The flowchart of the whole process is shown below.
<div align=center><img src="https://github.com/ningninga/Monitor-information-of-steamer-tickets/blob/main/flowchart1.png" ><img/></div>

## Use
If you want this program to run periodically, you can put the python file into your server and let it run on the server automatically.
- Upload python file into server.
- Create a sh file under the same directory of python file, and write some shell scripts as below into sh file. Dont't forget to change your own path and name of file.
```
#!/bin/bash
cd /home/python_project/jianing/message_flight_push
ps -ef | grep flight_monitor_qn.py |grep -v grep | awk '{print $2}'| xargs kill -9

sleep 1s

nohup python -u flight_monitor_qn.py > flight_monitor_qn.log 2>&1 &
```
- Create crontab timed tasks, for more information about crontab, please see [here](https://www.computerhope.com/unix/ucrontab.htm)
```
crontab -e
```
For me, I make the sever to run the file three times a day, 8am, 12am and 23:50 at night.
```
0 8,0 * * * sh /home/restart_shekou2hongkong.sh
50 23 * * * sh /home/restart_shekou2hongkong.sh
```


## API
https://www.cmskchp.com/sailingsJson







