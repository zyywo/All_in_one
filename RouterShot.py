#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import json
import time
import logging

logging.basicConfig(format='%(asctime)s %(message)s',filename='RouterShot.log',filemode='w',level=logging.INFO,datefmt='%Y/%m/%d %H:%M:%S')


class SaveScreenShot():
    def __init__(self,_config,_webdriver='Firefox'):
        try:
            config = _config
            self.base_dir = config['base_dir']

            local_time = time.localtime()
            year_dir = self.base_dir + '/{}年'.format(local_time.tm_year)
            mon_dir = '{0}/{1:02}月'.format(year_dir, local_time.tm_mon)
            self.day_dir = '{0}/{1:02}号'.format(mon_dir, local_time.tm_mday)

            if os.path.isdir(self.day_dir) is False:
                os.makedirs(self.day_dir)

            if _webdriver is 'Edge':
                self.driver = webdriver.Edge()
            elif _webdriver is 'Chrome':
                self.driver = webdriver.Chrome()
            elif _webdriver is 'Safari':
                self.driver = webdriver.Safari()
            else:
                self.driver = webdriver.Firefox( timeout=30 )
            self.driver.maximize_window()
            self.data = []
            self.message = '此警告生成的时间为：'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        except Exception as e:
            logging.error(e)

    def loginrouter(self, ip,_username,_password):
        try:
            url = 'http://' + ip
            self.driver.get(url)
            time.sleep(1)

            self.driver.find_element_by_id('username').send_keys(_username)
            self.driver.find_element_by_id('password').send_keys(_password)
            self.driver.find_element_by_id('OKBTN').click()
            time.sleep(3)
            self.driver.save_screenshot(self.day_dir + '/' + ip + '.png')

            time.sleep(1)

            self.version = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/form/table[1]/tbody/tr/td[1]/div/div[2]/table/tbody/tr[1]/td[2]').text

            self.link_number = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/form/table[1]/tbody/tr/td[2]/div/div[2]/table/tbody/tr[2]/td[2]/a').text

            self.host_number = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/form/table[1]/tbody/tr/td[2]/div/div[2]/table/tbody/tr[2]/td[1]/a').text

            self.this_is_list = self.driver.find_elements_by_tag_name('tspan')

            self.data.append(ip)
            self.data.append(self.version)
            self.data.append(self.host_number)
            self.data.append(self.link_number)
            self.data.append(self.this_is_list[1].text)
            self.data.append(self.this_is_list[6].text)
        except Exception as e:
            logging.error(e)

    def sendalert(self):
        try:
            for i in range(0,len(self.data),6):
                self.message = self.message+\
                               '\n--------------------------------------------------\n'+\
                               '路由器IP：'+self.data[i]+'\n'+\
                               '路由器版本：'+self.data[i+1]+'\n'+\
                               '主机数：'+self.data[i+2]+'\n'+\
                               '网络连接数：'+self.data[i+3]+'\n'+\
                               'CPU使用率：'+self.data[i+4]+'\n'+\
                               '内存使用率：'+self.data[i+5]
            mail = Mail()
            mail.send(self.message)
            # print(self.message)
        except Exception as e:
            logging.error(e)

    def quit(self):
        self.driver.quit()


class Mail():
    def __init__(self,_port=25):
        config = readconfig()
        self.from_addr = str(config['mail_from'])
        self.password = str(config['mail_password'])
        self.to_addr = str(config['mail_to'])
        self.server = str(config['mail_server'])
        self.port = _port

        self.mail_server = smtplib.SMTP(self.server, self.port)

        try:
            self.mail_server.login(self.from_addr,self.password)
        except Exception as e:
            print('zzz error in:Class Mail: __init__(): ',e)
            logging.error(e)

    def send(self,_message):
        msg = MIMEText(str(_message), 'plain', 'utf-8')
        msg['To'] = formataddr((Header('主人', 'utf-8').encode(), self.to_addr))
        msg['Subject'] = Header('{} 路由器预警通知'.format(time.strftime('%Y年%m月%d日 %H:%M:%S',time.localtime())), 'utf-8')
        try:
            self.mail_server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
            self.mail_server.quit()
        except Exception as e:
            print('login:', e)
            logging.error(e)


def readconfig():
    try:
        with open('config.json','r') as config:
            j = json.load(config)
            return j
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':

    a = SaveScreenShot(readconfig())
    routers = readconfig()['routers']
    for router in routers:
        a.loginrouter(router['ip'],router['username'],router['password'])

    a.sendalert()
    a.quit()

    print('end')