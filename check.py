__author__ = 'Jonny'
__date__ = '2018-03-07'
__location__ = '西安'
# -*- coding: utf-8 -*-

import requests
import station


def check_ticket(request,city_from,city_to,train_date):
    # city_from = input('请输入始发城市：')
    # city_to = input('请输入终点站：')
    # train_date = input('请输入乘车时间（格式：2018-01-01）：')
    station_from_to = station.stat_select(city_from,city_to)

    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?' \
          'leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s' \
          '&leftTicketDTO.to_station=%s&purpose_codes=ADULT'%(train_date,station_from_to[0],station_from_to[1])
    respond = request.get(url=url)
    result = respond.json()
    return result['data']
    # print(result['data'])
''' 4:车次
    5：始发站
    6：终点站
    7：乘车始发站
    8：乘车终点站
    9:乘车发车时间
    10：趁车到站时间
    11：耗时
    12：列车状况（IS_TIME_NOT_BUY,列车停运，无法购票）和票务情况（Y：有票，N：无票）
    13：随机码
    14：发车日期
    15：
    19：是否当日到达，
    22：高级软卧
    24:软卧
    25：软座
    26：
    27：无座
    28：
    29：硬卧
    30：硬座
    31：二等座
    32：一等座
    33:特等商务座
    34：动卧
'''
#票务信息汇总
def ticket_infor(request,flag,city_from,city_to,train_date):
    train_infor = [] #，创建列表，存储列车信息
    ticket = check_ticket(request,city_from,city_to,train_date)
    result_map = ticket['map']
    result_result = ticket['result']
    j = 0
    if flag == 1:
        print('序号'+'\t车次'+'\t 始发站'+'\t终点站'+'\t发车日期'+'\t是否当日到达'+'\t发车时间'+'\t到站时间'+'\t耗时'+
            '\t特等商务座'+'\t一等座'+'\t二等座'+'\t高级软卧'+'\t动卧'+'\t硬卧'+'\t硬座'+'\t无座')
    for i in result_result:
        temp_result = i.split('|')
        train_infor.append(temp_result) #将所有车次信息存入train_infor
        if flag == 1:
            if temp_result[12] !='IS_TIME_NOT_BUY':
                print(j,'\t   ',temp_result[3],'\t',station.sel_station(temp_result[6]),station.sel_station(temp_result[7]),temp_result[13],'\t\t  ',temp_result[18],
                      '\t\t ',temp_result[8],'\t ',temp_result[9],'\t  ',temp_result[10],'\t\t',temp_result[32],'\t\t',temp_result[31],'\t',
                      temp_result[30],'\t\t',temp_result[21],'\t\t',temp_result[33],'\t\t',temp_result[28],'\t\t',temp_result[29],'\t\t',temp_result[36])
            else:
                print(j,'\t',temp_result[3],'列车停运')

            j += 1

    return train_infor
if __name__ == '__main__':
    request = requests.session()

    ticket_infor(request)