#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import logging
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from pyquery import PyQuery as pq
import xlsxwriter

index_url = 'https://www.cmskchp.com/sailingsJson'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'www.cmskchp.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
}

# this data is request body
data = {
    'siteResJson': """{"userType":"LTP001","startSite":"SK","endSite":"HKA",
    "toDate":"2022-08-31","toDate2":"08月31日","toWeek":"周三","backDate":"","backDate2":"","backWeek":"",
    "endSiteName":"香港机场","startSiteName":"深圳蛇口","sailingType":"0","lineId":"SK-HKA",
    "airportTime":null,"lineType":null,"toTime":"",
    "flightCode":"QR","flightName":"卡塔爾航空","flightNo":"QR817","flightId":"58","flightDate":"2022-08-31",
    "flightHours":"19","flightMinute":"10","chanId":"1","isSeckill":false,"isSeckills":false,"nightFlight":0,"batchNo":null,"hsyLineId":null,"memberId":null}"""
}


def on_start():
    newest_time = NewestTime()
    for _ in range(3):
        try:
            with requests.Session() as req:
                html = req.post(index_url, headers=headers, data=data, timeout=10)
            json_obj = html.json()
            totalRemianTicket = 0
            ticket_info = ''
            if 'status' in json_obj and json_obj['status']:
                message = json_obj['message']
                # Gain the information which is needed in the attachment
                data_list = []
                for i in range(len(message)):
                    print(message[0])
                    totalRemianTicket += int(message[i]['totalRemainVolume'])
                    putong_price = int(message[i]['seatList'][0]['priceList'][0]['price'])
                    toudeng_price = int(message[i]['seatList'][1]['priceList'][0]['price'])
                    tedeng_price = int(message[i]['seatList'][2]['priceList'][0]['price'])
                    go_time = message[i]['goTime']
                    totalRemainVolume = message[i]['totalRemainVolume']
                    putong_num = message[i]['seatList'][0]['num']
                    toudeng_num = message[i]['seatList'][1]['num']
                    teudeng_num = message[i]['seatList'][2]['num']
                    ticket_info += f"Departure time：{go_time}，Total seats: {totalRemainVolume}" \
                                   f"Normal seats: {putong_num}，Price:{putong_price}CNY；" \
                                   f"VIP seats: {toudeng_num}，Price: {toudeng_price}CNY，" \
                                   f"VVIP seats: {teudeng_num}，Price: {tedeng_price}CNY\n"
                    data_list.append([go_time, totalRemainVolume, putong_num, putong_price, toudeng_num, toudeng_price,
                                      teudeng_num, tedeng_price])

                create_excel(totalRemianTicket, data_list)

                send_message_ticket_info = '8.31 There are {} seats in total\n'.format(totalRemianTicket) + ticket_info
                if len(message) != 0 and newest_time == '2022-08-31':
                    send_email(['983176666@qq.com'], '【URGENT MESSAGE】8.31 There are available tickets from Shekou to Hongkong！！', 'https://www.cmskchp.com/sailings\n' + send_message_ticket_info)
                    robot_msg = '【URGENT MESSAGE】8.31 There are available tickets from Shekou to Hongkong！！https://www.cmskchp.com/sailings'
                else:
                    send_email(['983176666@qq.com'], '【Daily Message】8.31 There is no available tickets', 'Please be more patient!!\n' + send_message_ticket_info)
                    robot_msg = '【Daily Message】8.31 There is no available tickets, the biggest available date is【{}】\n'.format(newest_time)
                robot_message(robot_msg + send_message_ticket_info)

            break
        except Exception as e:
            logging.error('ERROR: {}'.format(e))


def send_email(mail_receivers, subject_content, body_content):
    """
    :param mail_receivers: email address list, like ["123", "456"]
    :param subject_content: subject of email
    :param body_content: content of email
    :return:
    """
    try:
        # SMTP server, I use 163 here, and you can change this based on your email server
        mail_host = "smtp.163.com"
        # the email address of sender
        mail_sender = "*******"
        # Mailbox authorization code. NOTE: It is NOT the password of your email,
        # and how to get the mailbox authorization code, please google it
        mail_license = "********"

        mm = MIMEMultipart('related')

        # Set the name of the sender
        mm["From"] = "Notification from Shekou to Hongkong"
        # Set the email address of receivers
        mm["To"] = ','.join(mail_receivers)
        # Set the subject of the email
        mm["Subject"] = Header(subject_content, 'utf-8')

        # Set the content of email, Parameter 1: content of email, Parameter 2：text format, Parameter 3: encoding method
        message_text = MIMEText(body_content, "plain", "utf-8")
        # Add a text object to the MIMEMultipart object
        mm.attach(message_text)

        # Create an attachment
        atta = MIMEText(open('ticket.xlsx', 'rb').read(), 'base64', 'utf-8')
        # Set the information of the attachment
        atta["Content-Disposition"] = 'attachment; filename="ticket.xlsx"'
        # Put the attachment into the email
        mm.attach(atta)

        # NOTE: if  you just want to run this project on your own computer, not on the server,
        # you can use the code which are commented below
        # # Create SMTP object
        # stp = smtplib.SMTP()
        # # Set the domain name and port of the sender's mailbox, and the port address is 25
        # stp.connect(mail_host, 25)


        # Create SMTP object, as for ALi Cloud, the port is 465
        stp = smtplib.SMTP_SSL(host=mail_host, port=465)

        # set_debuglevel(1) can print out all the information about the interaction with the SMTP server
        stp.set_debuglevel(1)
        # Login mailbox, parameter 1: email address, parameter 2: mailbox authorization code
        stp.login(mail_sender, mail_license)
        # Send email, parameter 1: the email address of sender, parameter 2: the email address of receivers,
        # parameter 3: modify the content format to string
        stp.sendmail(mail_sender, mail_receivers, mm.as_string())
        logging.info("SUCCESS")
        # Close SMTP object
        stp.quit()
    except Exception as e:
        return False


def robot_message(value):
    """
    This function aim at sending daily flight information by your own Dingding robot.
    Do not forget to add your own robot into a group first!
    Please input your own Dingding phone number into phone and Webhook into robot_url below,

    In the settings of this robot, please input 'flight' in 'custom keywords' part so that you can receive the message.
    :param value: The message that you want to send.
    :return:
    """
    phone = '13514301351'
    message_data = {
        "msgtype": "text",
        "text": {
            "content": "Steamer tickets information is coming, {},@{}".format(value,phone)
        },
        "at": {
            "atMobiles": [
                "{}".format(phone)
            ],
            "isAtAll": False
        }
    }
    try:
        robot_url = 'https://oapi.dingtalk.com/robot/send?access_token=185b6151324390db703d50799235dc3837e460620aa5c0e65b01b62c61c6ca05'
        requests.post(url=robot_url, json=message_data)
        logging.info("Dingding robot: {}".format(value))
    except Exception as e:
        logging.error("Failed to send meaage by robot: {}, content: {}".format(e, value))


def NewestTime():
    try:
        date_header ={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'www.cmskchp.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
            'cookie': 'SESSION=280f5804d75b1984ea9bf275be6063ebed0970e9; __jsluid_s=c3427f335bc1bbf288670595e42c21df; cloudwise_client_id=9f1eb843-a179-5392-98dd-e90365f2a644; Hm_lvt_ff5de527230aab039c7144d5cf7bfe0b=1649316239; redirect_path=%2FpersonCenter; SECKEY_ABVK=Y4GwRpC0JU8LuHG/IrXreo/0q8yG0iiB7Y64c9GW88I%3D; BMAP_SECKEY=YR3MOdWl40tflgpjM052cljuZtS7D5jNfNgnwUihYVqKAYlS7pGnQSi2sPVztC-Dy0d2y_1MD9-35g9Aipv5Du0m2tl5eyrmB4vmVDL2FhzeU6N3CVCBP6J84PTIfCpcc9m4fN7fAPn6dCv6bgeFN3HjX5bahmEBHXYVTe98fJvi2WNqJRm6lHdfHX5a320_; page_uri=/sailings; Hm_lpvt_ff5de527230aab039c7144d5cf7bfe0b=1649426615; session_graphic_code=43c55b085e7fad89b5a4751fd67ca29d494d183879b61fce77221354c4569c312142ff548c8d3c3f64995605585e833c; siteResJson=%7B%22userType%22%3A%22LTP001%22%2C%22sailingType%22%3A%220%22%2C%22toDate%22%3A%222022-04-16%22%2C%22startSiteName%22%3A%22%E6%B7%B1%E5%9C%B3%E8%9B%87%E5%8F%A3%22%2C%22endSiteName%22%3A%22%E9%A6%99%E6%B8%AF%E6%9C%BA%E5%9C%BA%22%2C%22backDate%22%3A%22%22%2C%22lineId%22%3A%22SK-HKA%22%2C%22startSite%22%3A%22SK%22%2C%22endSite%22%3A%22HKA%22%2C%22toTime%22%3A%22%22%2C%22flightName%22%3A%22%E5%8D%A1%E5%A1%94%E7%88%BE%E8%88%AA%E7%A9%BA%22%2C%22flightId%22%3A%2258%22%2C%22flightCode%22%3A%22QR%22%2C%22flightDate%22%3A%222022-04-16%22%2C%22flightHours%22%3A%2219%22%2C%22flightMinute%22%3A%2210%22%2C%22flightNo%22%3A%22QR817%22%7D; CW_Start=1649426632177'
        }
        url = 'https://www.cmskchp.com/sailings'
        with requests.Session() as req:  # Use with to close connections and recycle garbage after automatic requests
            html = req.get(url, headers=date_header, timeout=10)
        html_content = pq(html.text)
        time_list = html_content('ul#timeList')
        newDate = time_list('li:last-child').attr('data-time')
        return newDate
    except Exception as e:
        robot_message('The date control does not get the date you expect')
        return ''


def create_excel(totalTicket, data_list):
    """
    Create excel
    :param totalTicket:
    :param data_list:
    :return:
    """
    workbook = xlsxwriter.Workbook('ticket.xlsx')
    worksheet = workbook.add_worksheet('ticket_info')
    merge_format = workbook.add_format({
        'bold':     True,
        'border':   6,
        'align':    'center',# Horizontal centering
        'valign':   'vcenter',# Vertical centering
        'fg_color': '#D7E4BC',# Color filling
    })
    merge_format_title = workbook.add_format({
        'bold':     True,
        'align':    'center',# Horizontal centering
        'valign':   'vcenter',# Vertical centering
        'fg_color': '#85888b',# Color filling
    })
    merge_format_cell = workbook.add_format({
        'align':    'center',# Horizontal centering
        'valign':   'vcenter',# Vertical centering
    })
    worksheet.merge_range('A1:H1', '8.31 ticket information is shown below,total seats : {}'.format(totalTicket), merge_format)
    title = ['Departure Time', 'RemainTickets', 'Normal', 'Price', 'VIP', 'Price', 'VVIP', 'Price']  # Set the head of the exal
    worksheet.write_row('A2', title, cell_format=merge_format_title)  # input head from A2
    start_number = 3
    for index, data in enumerate(data_list):
        worksheet.write_row('A{}'.format(start_number + index), data, cell_format=merge_format_cell)
    workbook.close()


if __name__ == '__main__':
    on_start()
