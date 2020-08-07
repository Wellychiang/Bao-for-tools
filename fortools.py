import pytest
import requests
import json
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from conftest import s



# s = requests.session()
sit = "http://sit.frontside.web.gt.owms.ark88.local:7878/E7/MerchantFrontSide"
uat = "https://web.6j71.com/"


def get_cookie_by_webdriver(username):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    b = webdriver.Chrome(chrome_options=chrome_options)

    url = "http://sit.frontside.web.gt.owms.ark88.local:7878/E7"
    b.get(url)
    b.find_element_by_xpath("//*[@placeholder='帐号']").send_keys(username)
    b.find_element_by_xpath("//*[@placeholder='密码']").send_keys('a111222')
    b.find_element_by_xpath("//*[@class='btn_default darker_color']").click()
    a = b.get_cookies()
    cookie = [item['name'] + "=" + item['value'] for item in a]
    cook = '; '.join(item for item in cookie)
    return cook


def login(username, pwd):  # 登入

    url = "%s/Account/Login" % sit
    # url = 'http://web.e77game.com/GT/MerchantFrontSide/Account/Login'
    rr = s.get(url)
    # print(rr.cookies)
    global cookie
    try:
        cookies = re.findall("Cookie (.*) for", str(rr.cookies))
        cookie = cookies[0]
    except Exception as e:
        print(e)
    # print(cookie)
    # url = 'http://web.e77game.com/GT/MerchantFrontSide/Account/Login'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie
    }

    token = re.findall('<input name="__RequestVerificationToken" type="hidden" value="(.*)" />', rr.text)

    data = {
        "__RequestVerificationToken": token,
        "UserName": username,
        "UserPwd": pwd
    }

    try:
        r = s.post(url, headers=headers, data=data, allow_redirects=False)
        updateCookie = r.headers["Set-Cookie"]
        print("\n", r.status_code)

    except Exception:
        print('錯啦')
        return r.text

    else:
        url2 = "http://sit.frontside.web.gt.owms.ark88.local:7878/E7"
        headers2 = {"Cookie": "%s" % updateCookie}
        r2 = s.get(url2, headers=headers2)
        print("", r2.status_code)
        return r2.text


def member_add(user, init_num,  arrive_num):  # 新增下線
    # login(username)
    url = sit+"/Member/MemberAdd"
    # url = 'http://web.e77game.com/GT/MerchantFrontSide/Member/MemberAdd'
    headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               }
    for i in range(arrive_num):
        init_num += 1
        data = {
            "Account": "%s%s" %(user, init_num),
            "Password": "a111222",
            "RebatePro": 0.040
            }
        r = s.post(url, headers=headers, data=data)
        print(r.json(), "\n%s%s" % (user, init_num))


def deposit(amount, service_type):  # 充值
    # cookie = get_cookie_by_webdriver()
    url = sit+"/Financial/ChargeInfo"
    # s = requests.session()
    headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                # "Cookie": cook
                }
    data = {
        "Amount": "%s" % amount,
        "ServiceType": "%s" % service_type
            }
    r = s.post(url, headers=headers, data=data)
    logging.debug('123')
    try:
        print(r.json())
    except Exception:
        if '请检查您的网路状态' in r.text:
            raise ValueError('Current response: 請檢查您的網路狀態')
        print(r.text)


def withdraw(username, amount, funds_pwd, card_id):  # 提現
    Score = get_user_score()
    url = sit+"/Financial/Withdraw"
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               # "Cookie": cook
               }

    data = {"CardId": card_id,
            "AvailableScore": Score['aScore'],
            "UserName": "%s" % username,
            "Amount": "%s" % amount,
            "MoneyPassword": funds_pwd}

    r = s.post(url, headers=headers, data=data)

    print(" Withdraw: ", r.json(), r.status_code)
    msg = r.json()['msg']
    a = {'msg': msg}
    return a


def bet_qq(amount, positive_num):   # 下注騰訊分分彩

    url = sit+"/Lottery/Plays"
    bet_url = sit+"/Lottery/Lotteries/27/IssueNo"

    bet = s.get(bet_url)
    chi_hao = int(bet.json()['innerResult']['nextIssueNo'])
    print(chi_hao)

    headers = {"Content-Type": "application/json;charset=UTF-8"}
    data = {
        "betAmount": amount,
        "betCount": 1,
        "currencyUnit": 1,
        "drawNumber": '5',
        "issueNo": "%s" % (chi_hao+positive_num),
        "lotteryId": 27,
        "odds": 3.653,
        "playTypeId": 5,
        "playTypeRadioId": 17,
        "ratio": 1,
        "rebate": 0,
        "totalBetAmount": amount,
        "userType": 1
        }
    load = json.dumps(data)
    r = s.post(url, headers=headers, data=load)
    print(data)
    print(' betQQ: ', r.json())
    return r.json()


def get_user_score():

    url = sit+"/Home/GetUserScore"
    # headers = {
    #     "Cookie": cook
    # }
    r = s.post(url)
    print(" UserScore: ", r.json())
    a = {'aScore': r.json()['result']['aScore']}
    return a


def ws():
    url = "ws://192.168.4.76:15674/ws"
    headers = {
        "Connection": "Upgrade",
        "Host": "192.168.4.76:15674",
        "Origin": "http://sit.frontside.web.gt.owms.ark88.local:7878",
        "Pragma": "no-cache",
        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
        "Sec-WebSocket-Key": "anj/SYSorhhg6IXT7rw2kw==",
        "Sec-WebSocket-Version": '13',
        "Upgrade": "websocket"
    }
    r = s.get(url, headers=headers)


# withdraw('wade02', 100, 'a12345')