# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import random
import time

# 出发站
fromstation = '深圳'
# 到达站
tostation = '驻马店'
# 乘车日期
# date = '/html/body/div[34]/div[2]/div[2]/div[22]/div'
date = '/html/body/div[34]/div[1]/div[2]/div[30]/div'

# CHAR_TYPE = ['商务座', '特等座', '一等座 ', '二等座', '高级软卧', '软卧', '动卧', '硬卧', '软座', '硬座', '无座', '其他']
CHAR_TYPE = ['SWZ', 'TZ',  'ZY', 'ZE', 'GR', 'RW', 'SRRB', 'YW', 'RZ', 'YZ', 'WZ', 'QT']
login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
tick_url = 'https://kyfw.12306.cn/otn/leftTicket/init'

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 60)


def login():
    browser.get(login_url)
    try:
        wait.until(expected_conditions.url_to_be('https://kyfw.12306.cn/otn/view/index.html'))
    except Exception as e:
        print(e)
        return False

    print('登陆成功')
    return True


def get_tickets():
    browser.get(tick_url)
    # 出发站
    fstation = browser.find_element_by_id('fromStationText')
    fstation.click()
    fstation.clear()
    fstation.click()
    fstation.send_keys(fromstation+Keys.RETURN)
    # 到达站
    tstation = browser.find_element_by_id('toStationText')
    tstation.clear()
    tstation.click()
    tstation.send_keys(tostation+Keys.RETURN)
    time.sleep(1)
    # 乘车日期
    browser.find_element_by_id('date_icon_1').click()
    browser.find_element_by_xpath(date).click()

    has_tickets = False
    checi = []
    pull = 0

    # 一直刷新，直到有票可订
    while not has_tickets:
        checi.clear()
        # 点击查询按钮
        query_btn = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'query_ticket')))
        query_btn.click()
        time.sleep(1)

        # a = browser.find_element_by_id('sear-result')
        # if not a:
        #     print(a)
        #     print('无票，继续刷新中... ...')
        #     continue

        tick_table = browser.find_element_by_id('queryLeftTable')
        trains = tick_table.find_elements_by_tag_name('tr')[::2]
        for t in trains:
            train_id = t.get_attribute('id').split('_')[1]
            chairs_code = [x+'_'+train_id for x in CHAR_TYPE]

            train = []
            train_info = t.find_element_by_tag_name('div')
            # 获取车次
            info = train_info.find_element_by_class_name('number')
            train.append(info.text)

            # 获取出发站\到达站
            info = train_info.find_element_by_class_name('cdz')
            train.append(info.text)

            # 获取出发时间\到达时间
            info = train_info.find_element_by_class_name('cds')
            train.append(info.text)

            # 获取历时
            info = train_info.find_element_by_class_name('ls')
            train.append(info.text)

            # 获取票数
            try:
                train.append(t.find_element_by_id(chairs_code[0]).text)
            except exceptions.NoSuchElementException:
                train.append(t.find_element_by_id(chairs_code[1]).text)
            train += [x for x in map(lambda x: t.find_element_by_id(x).text, chairs_code[2:])]

            # 预定车票的按键
            try:
                info = t.find_element_by_class_name('btn72')
            except exceptions.NoSuchElementException:
                info = None
            train.append(info)

            # 预定按键可用，说明有票
            if train[-1] is not None:
                has_tickets = True

            print(train)

            checi.append(train)

        # 一个页面处理完后依然没有票的情况
        if has_tickets is False:
            st = random.randrange(1, 3)
            print('第{:04}轮：无票可抢，等待{}秒后继续刷新...'.format(pull, st))
            pull += 1
            time.sleep(st)
            continue

        print('开始处理有票的情况...')

    # browser.quit()


if __name__ == '__main__':
    if not login():
        quit(0)

    get_tickets()
