# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from datetime import datetime
from SendSMS import send_sms
from setting import fromstation, tostation, date_of_leave, select_char, select_t
import random
import time

CHAIR_CN = ['商务座', '特等座', '一等座', '二等座', '高级软卧', '软卧', '动卧', '硬卧', '软座', '硬座', '无座', '其他']
CHAR_TYPE = ['SWZ', 'TZ',  'ZY', 'ZE', 'GR', 'RW', 'SRRB', 'YW', 'RZ', 'YZ', 'WZ', 'QT']
TICKET_IS_NONE = ['无', '--']
login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
tick_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
order_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 60)


def login():
    browser.get(login_url)

    try:
        wait.until(expected_conditions.url_to_be('https://kyfw.12306.cn/otn/view/index.html'))
    except Exception as e:
        print(e)
        return False

    return True


def get_trips():
    browser.get(tick_url)
    # 出发站
    fstation = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'fromStationText')))
    fstation.click()
    fstation.clear()
    fstation.click()
    fstation.send_keys(fromstation+Keys.RETURN)
    # 到达站
    tstation = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'toStationText')))
    tstation.clear()
    tstation.click()
    tstation.send_keys(tostation+Keys.RETURN)
    time.sleep(1)
    # 乘车日期
    browser.find_element_by_id('date_icon_1').click()
    browser.find_element_by_xpath(get_date(date_of_leave)).click()

    pull = 0
    # 一直刷新，直到有票可订
    while True:
        print('{}  第{:05}轮：无票可抢，继续刷新中...'.format(datetime.now(), pull))
        pull += 1
        trains = None
        time.sleep(random.randrange(1, 3))

        # 点击查询按钮
        query_btn = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'query_ticket')))
        try:
            query_btn.click()
        except exceptions.ElementClickInterceptedException:
            print('查询按钮被其他元素遮挡，重试中...')
            continue
        finally:
            time.sleep(1)

        try:
            tick_table = wait.until(expected_conditions.visibility_of_element_located((By.ID, 'queryLeftTable')))
            trains = tick_table.find_elements_by_tag_name('tr')[::2]
        except (exceptions.StaleElementReferenceException, exceptions.TimeoutException):
            print('查询失败， 重试中 ...')
            time.sleep(2)
            continue
        except Exception as e:
            print(e)

        for t in trains:
            train_id = t.get_attribute('id').split('_')[1]
            chairs_code = [x+'_'+train_id for x in CHAR_TYPE]

            train_info = t.find_element_by_tag_name('div')
            # 获取车次
            trips = train_info.find_element_by_class_name('number').text

            if trips not in select_t:
                continue

            # 获取出发站\到达站
            ft_station = train_info.find_element_by_class_name('cdz').text

            # 获取出发时间\到达时间
            lt_times = train_info.find_element_by_class_name('cds').text

            # 获取历时
            duration = train_info.find_element_by_class_name('ls').text

            # 获取票数
            try:
                ticket_num = [t.find_element_by_id(chairs_code[0]).text]
            except exceptions.NoSuchElementException:
                ticket_num = [t.find_element_by_id(chairs_code[1]).text]
            ticket_num += [x for x in map(lambda x: t.find_element_by_id(x).text, chairs_code[2:])]

            for _s_c in select_char:
                # 该类型的座位有票
                c_index = CHAIR_CN.index(_s_c)
                if ticket_num[c_index-1 if c_index > 1 else 0] not in TICKET_IS_NONE:
                    # 预定车票的按键
                    order_btn = t.find_element_by_class_name('btn72')
                    trips_info = [ft_station, lt_times, duration, ticket_num, order_btn]

                    print('{}: {}'.format(trips, trips_info))

                    return trips_info, _s_c


def order_ticket(target_trip, se_chair):
    # 点击预定
    target_trip[-1].click()
    wait.until(expected_conditions.url_to_be(order_url))

    # 勾选乘客
    wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'per-sel')))
    per_sel = browser.find_element_by_class_name('per-sel')
    pers = per_sel.find_elements_by_tag_name('input')
    # print('乘客：', pers[0])
    # print('乘客姓名：', pers[0].text)
    pers[0].click()

    # 选择座位
    target_chair = None
    seat_type = browser.find_element_by_id('seatType_1')
    text = seat_type.text
    seats = text.split()
    print('可选的座位类型：', seats)
    for s in seats:
        if se_chair in s:
            print('选择的座位：', s)
            target_chair = s
            break
    try:
        Select(browser.find_element_by_id('seatType_1')).select_by_visible_text(target_chair)
    except Exception as e:
        print('line 153:   ', e)

    # 订票按钮
    btn = browser.find_element_by_id('submitOrder_id')
    btn.click()
    sumbit = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'qr_submit_id')))
    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'qr_submit_id')))
    print(sumbit.text)
    time.sleep(1)
    sumbit.click()

    try:
        if wait.until(expected_conditions.url_changes(order_url)):
            return True
    except exceptions.TimeoutException:
        print('订单超时')
        return False


def get_date(_date):
    today = datetime.now()
    target_day = datetime.strptime(_date, '%m-%d')
    if target_day.month == today.month:
        xpath_of_day = '/html/body/div[34]/div[1]/div[2]/div[{}]/div'.format(target_day.day)
    else:
        xpath_of_day = '/html/body/div[34]/div[2]/div[2]/div[{}]/div'.format(target_day.day)

    # print(xpath_of_day)

    # el_tm, el_nm = browser.find_elements_by_class_name('cal-cm')
    return xpath_of_day


if __name__ == '__main__':
    if not login():
        quit(0)

    ok = False
    while not ok:
        checi, chair = get_trips()
        print('开始处理有票的情况...')
        if not order_ticket(checi, chair):
            print('订票失败，继续刷新中 ...')
        else:
            ok = True
            send_sms('订票成功，赶紧付款')
