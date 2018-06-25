__author__ = 'Jonny'
__date__ = '2018-03-07'
__location__ = '西安'
# -*- coding: utf-8 -*-

#实际操作发现，在登录12306账户的过程中服务器会首先验证用户提交的验证码是否正确，之后才回去验证账户是否存在，是否是合法账户
import requests
import user

#确保是同一个浏览器的操作，不然会引起后面验证码无法提交到最初请求的信息中
# request = requests.session()


def login(request):
    check_URL = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    login_URL = 'https://kyfw.12306.cn/passport/web/login'
    respond = request.get('https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.188056268494885')
    bitImg = respond.content
    with open('conf.png','wb') as f:
        f.write(bitImg)
    zuobiao = input('请输入验证码坐标：')
    #提交验证码数据包
    data ={
        'answer':zuobiao,
        'login_site':'E',
        'rand': 'sjrand'
    }
    respond = request.post(url=check_URL,data=data)
    print(respond.text)
    #提交用户名数据包
    data = {
        'username':user.user,
        'password':user.password,
        'appid':'otn'
    }
    respond = request.post(url= login_URL,data=data)
    print(respond.text)
    return respond.json()['result_code']
if __name__ == '__main__':
    request = requests.session()
    login(request)
