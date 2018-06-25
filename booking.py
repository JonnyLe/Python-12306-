__author__ = 'Jonny'
__date__ = '2018-03-07'
__location__ = '西安'
# -*- coding: utf-8 -*-
#因部分参数无法获取，无法进行,目前只能实现西安到济南的K1026次列车在3月22日
import requests
import check

def book(request,city_from,city_to,train_no):
    #train = input('请输入预定的车次:')
    seat_type = input('座位类型:')
    num = int(input('请输入预定票数:'))
    seatType ={'硬座':'1','硬卧':3}

    #获取用户所需车次的信息
    train_infor = check.ticket_infor(request)
    for temp in train_infor:
        temp = temp.split('|')
        if temp[12] != 'IS_TIME_NOT_BUY':
            if temp[3] == train_no:
                break
            else:
                print('没有该趟车次')
        else:
            print('列车停运')

    url_booking = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'

    data = {
        'train_date':'Thu Mar 22 2018 00:00:00 GMT+0800 (中国标准时间)',
        'train_no':'49000K10260I',#参数构成：49000+车次+0+某个大写字母
        'stationTrainCode':train_no,  # 列车车次
        'seatType':seatType['seat_type'], #座位类型 硬座：1,硬卧：3
        'fromStationTelecode':temp[6],#始发站
        'toStationTelecode':temp[7],  #终点站
        'leftTicket':'aE%2F7%2FZvzmTXLrp8Vr74BzpmgIKac2zAUrNSQNLLLKdm1aYCEhjuYGlGiS0s%3D',#参数需替换
        'purpose_codes':'00',
        'train_location':'KA',#需进行参数替换
        '_json_att':'',
        'REPEAT_SUBMIT_TOKEN':'38d1cea21ad90eb8fca837cbaf4361e6'#此参数可以从前一个访问网页中获取
    }
    respond = request.post(url=url_booking,data=data)



if __name__ == '__main__':
    request = requests.session()
    book(request)
