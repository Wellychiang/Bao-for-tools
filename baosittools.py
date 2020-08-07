import time
import fortools
from card_id import CardId

b = fortools

# a = b.login('test08', 'a111222')
# b.get_user_score()


def withdraw(user='test08', pwd='a111222', amount=20, funds_pwd='a12345'):
    b.login(user, pwd)
    b.get_user_score()
    card_id = CardId('sit').user(user)
    b.withdraw(user, amount, funds_pwd, card_id)
    time.sleep(1)
    b.get_user_score()
    print(" ", time.asctime())
# withdraw()


# Alipay(支付寶轉卡), WebATM(), Directpay(500),
# 最大3000
def deposit(username='jackson', pwd='a111222', amount=5000, service_type='WebATM', rangee=1):
    b.login(username, pwd)
    for i in range(rangee):
        b.get_user_score()
        b.deposit(amount, service_type)
    time.sleep(1)
    b.get_user_score()
    print(" %s" % time.asctime())

# deposit()


# positive_num是0的話就是旗號+0的意思, 輸入負號也是可以減的
def bet_qq(username='wade01', amount=1700, positive_num=0, rangee=1):
    b.login(username, 'a111222')
    # b.get_cookie_by_webdriver(username)
    for i in range(rangee):
        b.get_user_score()
        b.bet_qq(amount, positive_num)
    time.sleep(1)
    b.get_user_score()
    print(" ", time.asctime())

# bet_qq('test08')


def member_add(hostname='wade01', pwd='a111222', user="test0", init_num=7, plus_num=1):  #user+initNum = test04
    b.login(hostname, pwd)
    b.member_add(user, init_num, plus_num)
# member_add()


def ws(username='wade01', pwd='a111222'):
    b.login(username, pwd)
    b.ws()
# ws()



# b.login('wade01', 'a111222')
# b.deposit(100, 'Alipay')
