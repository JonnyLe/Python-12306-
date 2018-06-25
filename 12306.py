__author__ = 'Jonny'
__date__ = '2018-03-07'
__location__ = '西安'
# -*- coding: utf-8 -*-

import time
import login
import check
import requests
import station
import booking


#---------------------------- 登录账户--------------------------------------------------
def logIn(request):
    state = 1
    while(state != 0):
        print('请登录：')
        state = login.login(request)


#----------------------------检测余票-------------------------------------------------
def checkStandbyTicket(request,city_from,city_to,train_date):
    result= check.ticket_infor(request,1,city_from,city_to,train_date)
    train_no = input('请输入需订车次：')
    print('#######################################################################################')
    count = 0
    #循环检测余票
    while True:
        count += 1
        print('小J玩命查询中(%s)........'%count)
        if count % 100 == 0:
            autoCheck = input('是否继续自动查询,或切换车次：（Y/N/Z105）')
            if (autoCheck == 'N' or autoCheck == 'n' ):
                print('已终止自动查询！')
                return None
            if (autoCheck != 'N' or autoCheck != 'n' or autoCheck != 'Y' or autoCheck != 'y'):
                train_no = autoCheck
        time.sleep(2) #延时2秒，避免重复查询过快
        for tempData in result:
            if tempData[3] == train_no and tempData[11] =='Y':
                print('（注意：若无坐席类型后无余座或为‘无’均表示无剩余席位！）\n', '车次：', tempData[3], '\t始发站：', station.sel_station(tempData[6]),
                      '\t终点站：',station.sel_station(tempData[7]), '\n乘车日期：',tempData[13], '\t是否当日到达：', tempData[18],
                      '\t发车时间：', tempData[8], '\t到站时间：', tempData[9], '\t耗时：', tempData[10], '\n特等商务座：', tempData[32], '\t一等座：',
                      tempData[31], '\t二等座：',tempData[30], '\n高级软卧：', tempData[21], '\t动卧：', tempData[33], '\t硬卧：', tempData[28], '\t硬座：',
                      tempData[29], '\t无座：', tempData[36])
                break
            if tempData[3] == train_no and tempData[11] =='IS_TIME_NOT_BUY':
                print('无该车次信息或停运!')
                break
            if tempData[3] == train_no and tempData[11] =='N':
                result = check.ticket_infor(request,0,city_from,city_to,train_date)
                break

        if tempData[11] == 'Y':
            return train_no


if __name__ =='__main__':
    # 确保是同一个浏览器的操作
    request = requests.session()
    # ---------------------------输入趁车信息-------------------------------------------------
    city_from = input('请输入始发城市：')
    city_to = input('请输入终点站：')
    train_date = input('请输入乘车时间（格式：2018-01-01）：')

    # ----------------------------检测余票-------------------------------------------------
    while True:
        train_no = checkStandbyTicket(request, city_from, city_to, train_date)
        if train_no !=None:
            print('是否登录购票：')
            if input('是否登录购票：(Y/N)') == 'Y' or 'y':
                # ---------------------------- 登录账户--------------------------------------------------
                logIn(request)

                # ---------------------------- 车票下单（由于某些参数问题，暂时无法实现所有车站自动预定）--------------------------------------------------
                booking(request, city_from, city_to, train_no)
        else:
            if input('是否退出：(Y/N)') == 'Y' or 'y':
                print('谢谢使用12306爬虫订票系统！')
                break







