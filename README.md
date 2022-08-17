# Monitor-information-of-steamer-tickets
This project is used to monitor the information of steamer ticket.

## Table of Contents

- [Background](#background)
- [Flowchart](#flowchart)
- [Use](#use)
- [API](#api)
- [Version](#version)




## Background
### V2.0(For all users)
Hi, this time I just want to make more and more people be able to use this function, so I planned to improve the function based on the first version, design a webpage and run it on my server, so it is totally ok if you do not have your own server, it means that you can still receive the email as you want.
### V1.0 (For developers)
Hi, I am going to introduce my situation first, I want to take a plane from Hongkong to other country ( Because flights from Hong Kong are much cheaper than other flights from mainland China). But due to the COVID-19, there is a few ways to go to Hongkong. One of the most available ways is taking a steamer from Shenzhen to Hongkong, most affordable way as well.  

However, the steamer tickets are limited, I heard that many people paid high prices to buy steamer tickets from scalpers last year, just because they were not able to buy tickets on time. Well, the reason why they were not to buy tickets is that the date of ticket release on the ticketing website is not fixed, so they missed the proper time to buy tickets. This year, I want to monitor the information about the tickets to make sure that I can buy a ticket successfully.  

In order to make myself notice the information, I choose two ways to send data, the first one is sending email to my email address, the second one is sending message via Ding (For more details about how to send message by robot via Ding, please see [here](https://github.com/ningninga/flight_discount_info_push))


## Flowchart

### V2.0 
The flowchart for v2.0 is shown below.  
<div align=center><img src="https://github.com/ningninga/Monitor-information-of-steamer-tickets/blob/main/flowchartv2.0.png" ><img/></div>


### V1.0 
The flowchart of the whole process is shown below.
<div align=center><img src="https://github.com/ningninga/Monitor-information-of-steamer-tickets/blob/main/flowchart1.png" ><img/></div>



## Use

### V2.0
In order to make it easier to use, I launch this project to the Internet. So you can easily access it via: jjn.4zcf.com(http://jjn.4zcf.com)).   

Please input some necessary fields under the directions, and then click Submit button. If the date that you choose doesn’t have any available tickets, you will receive a confirmation email to ensure that your email address is able to receive notification emails, not make the emails into junk mail.
### V1.0
If you want this program to run periodically, you can put the python file into your server and let it run on the server automatically.
- Upload python file into server.
- Create a sh file under the same directory of python file, and write some shell scripts as below into sh file. Dont't forget to change your own path and name of file.
```
#!/bin/bash
cd *******
ps -ef | grep shekou2hongkong.py |grep -v grep | awk '{print $2}'| xargs kill -9

sleep 1s

nohup python -u shekou2hongkong.py > shekou2hongkong.log 2>&1 &
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

## Version
### For 2.0:
I noticed that the reason why some students are not able to buy steamer tickets from Shekou to Hongkong is that a small number of tickets were sold out in a very short period. Meanwhile, students do not know when will someone else refunds the ticket. So it is very hard for them to grab tickets on time.    
As a consequence of that, students have to pay even 10 times more than usual to get a ticket to make sure the success of their travel.  
In order to make more students buy tickets successfully with a normal price, and even other people who want receive the information of specifical ticket. I have planned to design a webpage and let users input the date and some other relevant information about the ticket, if there is any change in the ticket, they can receive a notification on time.
### For 1.0:
In version 1.0, the main function is monitoring and sending email. Frankly speaking, if you have your own server, so that you can run this python code on your server periodically. Because of that, the main function makes sence and works well.







